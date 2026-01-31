#!/usr/bin/env python3
"""
ios_rag_mvp.py

MVP iOS (Swift-only) RAG builder for UI test generation.

It:
- Takes an iOS app directory as input
- Indexes all .swift files (excluding common vendor/build dirs)
- Extracts chunks for:
  - SwiftUI Views: `struct X: View { ... }`
  - UIKit screens: `class X: UIViewController { ... }`
  - Accessibility identifiers: `.accessibilityIdentifier("...")` and `.accessibilityIdentifier = "..."`
  - Buttons: `Button("...")` (SwiftUI)
  - Navigation calls: push/present + SwiftUI navigationDestination/sheet/fullScreenCover
- Stores chunks into a vector DB (Chroma persisted to disk)
- Audits missing accessibility identifiers (best-effort heuristic) and can fail-fast

Install:
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt

Build index:
  python ios_rag_mvp.py ingest --app-dir /path/to/ios --persist ./rag_store --collection ios_app

Fail-fast if missing accessibility identifiers are likely:
  python ios_rag_mvp.py ingest --app-dir /path/to/ios --persist ./rag_store --collection ios_app --fail-if-missing-ids

Query (quick retrieval smoke test):
  python ios_rag_mvp.py query --persist ./rag_store --collection ios_app --q "login invalid password" --k 8

Notes:
- Parsing is regex + brace matching (MVP). For production, replace with SwiftSyntax.
- Accessibility ID audit is heuristic; it flags likely issues early.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Iterable

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def meta_list_to_str(items, limit=200) -> str:
    if not items:
        return ""
    items = items[:limit]
    return "|".join(str(x) for x in items)



# -----------------------------
# Configuration
# -----------------------------

DEFAULT_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

EXCLUDE_DIRS = {
    ".git",
    "Pods",
    "Carthage",
    "DerivedData",
    ".build",
    ".swiftpm",
    "Build",
    ".xcodeproj",
    ".xcworkspace",
}

SWIFT_SUFFIX = ".swift"

# SwiftUI View blocks
SWIFTUI_VIEW_START_RE = re.compile(
    r"(?m)^\s*(public|internal|private|fileprivate|open)?\s*struct\s+([A-Za-z_]\w*)\s*:\s*View\s*\{"
)

# UIKit ViewController blocks
UIKIT_VC_START_RE = re.compile(
    r"(?m)^\s*(public|internal|private|fileprivate|open)?\s*(final\s+)?class\s+([A-Za-z_]\w*)\s*:\s*([^{\n]*\bUIViewController\b[^{\n]*)\s*\{"
)

# Accessibility identifiers
SWIFTUI_A11Y_ID_RE = re.compile(r'\.accessibilityIdentifier\(\s*"([^"]+)"\s*\)')
UIKIT_A11Y_ID_RE = re.compile(r'\.accessibilityIdentifier\s*=\s*"([^"]+)"')

# SwiftUI Buttons
SWIFTUI_BUTTON_RE = re.compile(r'Button\(\s*"([^"]+)"\s*\)')

# Navigation patterns (best-effort)
NAV_PATTERNS = [
    re.compile(r"\bnavigationController\?\.\s*pushViewController\s*\(", re.MULTILINE),
    re.compile(r"\bpushViewController\s*\(", re.MULTILINE),
    re.compile(r"\bpresent\s*\(", re.MULTILINE),
    re.compile(r"\bNavigationStack\b", re.MULTILINE),
    re.compile(r"\bnavigationDestination\s*\(", re.MULTILINE),
    re.compile(r"\bsheet\s*\(", re.MULTILINE),
    re.compile(r"\bfullScreenCover\s*\(", re.MULTILINE),
]

# Simple "interactive element" patterns for audit
SWIFTUI_INTERACTIVE_RE = re.compile(
    r"\b(Button|TextField|SecureField|Toggle|Picker)\b", re.MULTILINE
)
UIKIT_INTERACTIVE_RE = re.compile(
    r"\b(UIButton|UITextField|UISwitch|UISegmentedControl|UITableView|UICollectionView)\b",
    re.MULTILINE,
)


# -----------------------------
# Utilities
# -----------------------------

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def normalize_path(p: Path, root: Path) -> str:
    try:
        return str(p.relative_to(root)).replace("\\", "/")
    except Exception:
        return str(p).replace("\\", "/")

def iter_swift_files(root: Path) -> Iterable[Path]:
    for dirpath, dirs, files in os.walk(root):
        # prune excludes
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for f in files:
            if f.endswith(SWIFT_SUFFIX):
                yield Path(dirpath) / f

def find_matching_brace(text: str, open_index: int) -> int:
    """
    MVP brace matcher. Not perfect with braces inside strings/comments.
    """
    depth = 0
    i = open_index
    n = len(text)
    while i < n:
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return n - 1

def safe_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


# -----------------------------
# Chunking
# -----------------------------

@dataclass
class Chunk:
    text: str
    meta: Dict[str, object]

def extract_blocks(text: str, start_re: re.Pattern, name_group: int, kind: str) -> List[Tuple[str, str]]:
    """
    Returns list of (name, block_text)
    """
    blocks: List[Tuple[str, str]] = []
    for m in start_re.finditer(text):
        name = m.group(name_group)
        brace_open = text.find("{", m.end() - 1)
        if brace_open == -1:
            continue
        end = find_matching_brace(text, brace_open)
        block = text[m.start(): end + 1].strip()
        blocks.append((name, block))
    return blocks

def build_chunks_for_file(file_text: str, rel_path: str) -> List[Chunk]:
    chunks: List[Chunk] = []

    # SwiftUI View blocks
    for view_name, block in extract_blocks(file_text, SWIFTUI_VIEW_START_RE, name_group=2, kind="swiftui_view"):
        a11y_ids = sorted(set(SWIFTUI_A11Y_ID_RE.findall(block)))
        buttons = sorted(set(SWIFTUI_BUTTON_RE.findall(block)))
        nav_hits = sum(1 for pat in NAV_PATTERNS if pat.search(block))
        meta = {
            "kind": "swiftui_view",
            "path": rel_path,
            "screen": view_name,
            "symbol": view_name,
            "accessibility_ids": meta_list_to_str(a11y_ids),
            "accessibility_id_count": len(a11y_ids),
            "buttons": meta_list_to_str(buttons[:50]),
            "button_count": len(buttons),
            "navigation_signals": nav_hits,
        }
        chunks.append(Chunk(text=block, meta=meta))

        # Screen card (compact summary chunk)
        card = {
            "type": "SCREEN_CARD",
            "ui": "SwiftUI",
            "screen": view_name,
            "path": rel_path,
            "buttons": buttons[:50],
            "accessibility_ids": a11y_ids[:200],
            "has_navigation_signals": bool(nav_hits),
        }
        chunks.append(Chunk(text=safe_json(card), meta={**meta, "kind": "screen_card"}))

    # UIKit ViewController blocks
    for cls_name, block in extract_blocks(file_text, UIKIT_VC_START_RE, name_group=3, kind="uikit_viewcontroller"):
        a11y_ids = sorted(set(UIKIT_A11Y_ID_RE.findall(block)))
        nav_hits = sum(1 for pat in NAV_PATTERNS if pat.search(block))
        meta = {
            "kind": "uikit_viewcontroller",
            "path": rel_path,
            "screen": cls_name,
            "symbol": cls_name,
            "accessibility_ids": meta_list_to_str(a11y_ids),
            "accessibility_id_count": len(a11y_ids),
            "navigation_signals": nav_hits,
        }
        chunks.append(Chunk(text=block, meta=meta))

        card = {
            "type": "SCREEN_CARD",
            "ui": "UIKit",
            "screen": cls_name,
            "path": rel_path,
            "accessibility_ids": a11y_ids[:200],
            "has_navigation_signals": bool(nav_hits),
        }
        chunks.append(Chunk(text=safe_json(card), meta={**meta, "kind": "screen_card"}))

    # Accessibility map chunk per file (helps retrieval by ID)
    file_ids = sorted(set(SWIFTUI_A11Y_ID_RE.findall(file_text)) | set(UIKIT_A11Y_ID_RE.findall(file_text)))
    if file_ids:
        amap = "ACCESSIBILITY_IDS\npath: " + rel_path + "\n" + "\n".join(file_ids)
        chunks.append(Chunk(
            text=amap,
            meta={
                "kind": "accessibility_map",
                "path": rel_path,
                "accessibility_ids": meta_list_to_str(file_ids),
                "accessibility_id_count": len(file_ids),
            }
        ))

    # Navigation map chunk per file (simple signal chunk)
    nav_lines = []
    for line in file_text.splitlines():
        if any(p.search(line) for p in NAV_PATTERNS):
            nav_lines.append(line.strip())
            if len(nav_lines) >= 60:
                break
    if nav_lines:
        nav_chunk = "NAVIGATION_SIGNALS\npath: " + rel_path + "\n" + "\n".join(nav_lines)
        chunks.append(Chunk(text=nav_chunk, meta={"kind": "navigation_signals", "path": rel_path}))

    # Fallback: if no chunks were found, store a smaller raw slice
    if not chunks:
        raw = file_text.strip()
        if raw:
            raw = raw[:4000]
            chunks.append(Chunk(text=raw, meta={"kind": "swift_raw", "path": rel_path}))

    return chunks


# -----------------------------
# Accessibility audit (heuristic)
# -----------------------------

@dataclass
class AuditFinding:
    path: str
    screen: str
    ui: str
    interactive_count: int
    accessibility_id_count: int

def audit_accessibility(chunks: List[Chunk]) -> Tuple[List[AuditFinding], Dict[str, object]]:
    """
    Heuristic:
    - For each screen block (SwiftUI View or UIViewController),
      count interactive elements and accessibility IDs found inside the block.
    - Flag screens that have interactive elements but 0 accessibility IDs.
    """
    findings: List[AuditFinding] = []

    for ch in chunks:
        if ch.meta.get("kind") == "swiftui_view":
            block = ch.text
            interactive = len(SWIFTUI_INTERACTIVE_RE.findall(block))
            ids = len(SWIFTUI_A11Y_ID_RE.findall(block))
            if interactive > 0 and ids == 0:
                findings.append(AuditFinding(
                    path=str(ch.meta.get("path")),
                    screen=str(ch.meta.get("screen")),
                    ui="SwiftUI",
                    interactive_count=interactive,
                    accessibility_id_count=ids,
                ))

        if ch.meta.get("kind") == "uikit_viewcontroller":
            block = ch.text
            interactive = len(UIKIT_INTERACTIVE_RE.findall(block))
            ids = len(UIKIT_A11Y_ID_RE.findall(block))
            if interactive > 0 and ids == 0:
                findings.append(AuditFinding(
                    path=str(ch.meta.get("path")),
                    screen=str(ch.meta.get("screen")),
                    ui="UIKit",
                    interactive_count=interactive,
                    accessibility_id_count=ids,
                ))

    summary = {
        "flagged_screens": len(findings),
        "note": "Heuristic audit: interactive elements exist but no accessibility identifiers were detected inside the screen block.",
    }
    return findings, summary


# -----------------------------
# Vector store (Chroma)
# -----------------------------

def build_vectorstore(persist_dir: str, collection: str, embed_model: str) -> Chroma:
    embeddings = HuggingFaceEmbeddings(model_name=embed_model)
    vs = Chroma(
        collection_name=collection,
        embedding_function=embeddings,
        persist_directory=persist_dir,
    )
    return vs

def upsert_documents(vs: Chroma, docs: List[Document]) -> None:
    # Use deterministic IDs so re-ingest is stable
    ids = [sha1(d.page_content + safe_json(d.metadata)) for d in docs]
    vs.add_documents(documents=docs, ids=ids)
    vs.persist()


# -----------------------------
# CLI commands
# -----------------------------

def cmd_ingest(args: argparse.Namespace) -> int:
    app_dir = Path(args.app_dir).expanduser().resolve()
    if not app_dir.exists() or not app_dir.is_dir():
        print(f"ERROR: app-dir not found or not a directory: {app_dir}", file=sys.stderr)
        return 2

    all_chunks: List[Chunk] = []
    swift_files = list(iter_swift_files(app_dir))
    if not swift_files:
        print("ERROR: no .swift files found under app-dir", file=sys.stderr)
        return 2

    for p in swift_files:
        rel = normalize_path(p, app_dir)
        text = read_text(p)
        if not text.strip():
            continue
        all_chunks.extend(build_chunks_for_file(text, rel))

    # Audit for accessibility IDs
    findings, summary = audit_accessibility(all_chunks)

    # Always write an audit summary chunk into the DB (useful at retrieval time)
    audit_doc = Document(
        page_content=safe_json({
            "type": "ACCESSIBILITY_AUDIT",
            "summary": summary,
            "flagged": [f.__dict__ for f in findings[:200]],
            "total_flagged": len(findings),
        }),
        metadata={"kind": "accessibility_audit", "path": "_audit_"},
    )

    if args.fail_if_missing_ids and len(findings) > 0:
        print("ACCESSIBILITY AUDIT FAILED (missing IDs detected).")
        print(safe_json({
            "flagged_screens": len(findings),
            "examples": [f.__dict__ for f in findings[:20]],
            "action": "Add .accessibilityIdentifier(...) to interactive elements on these screens before generating UI tests.",
        }))
        return 3

    # Convert chunks to Documents
    docs: List[Document] = [audit_doc]
    for ch in all_chunks:
        docs.append(Document(page_content=ch.text, metadata=ch.meta))

    vs = build_vectorstore(args.persist, args.collection, args.embed_model)
    upsert_documents(vs, docs)

    print(safe_json({
        "status": "ok",
        "indexed_swift_files": len(swift_files),
        "documents_upserted": len(docs),
        "persist_dir": args.persist,
        "collection": args.collection,
        "accessibility_audit": {
            "flagged_screens": len(findings),
            "note": summary["note"],
        },
    }))
    return 0

def cmd_query(args: argparse.Namespace) -> int:
    vs = build_vectorstore(args.persist, args.collection, args.embed_model)
    docs = vs.similarity_search(args.q, k=args.k)

    out = []
    for d in docs:
        out.append({
            "kind": d.metadata.get("kind"),
            "path": d.metadata.get("path"),
            "screen": d.metadata.get("screen") or d.metadata.get("symbol"),
            "snippet": (d.page_content[:400] + ("..." if len(d.page_content) > 400 else "")),
        })
    print(safe_json({"q": args.q, "k": args.k, "results": out}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ingest = sub.add_parser("ingest")
    p_ingest.add_argument("--app-dir", required=True, help="Path to iOS app directory (Swift project)")
    p_ingest.add_argument("--persist", required=True, help="Chroma persist directory")
    p_ingest.add_argument("--collection", default="ios_app", help="Chroma collection name")
    p_ingest.add_argument("--embed-model", default=DEFAULT_EMBED_MODEL, help="Embedding model name")
    p_ingest.add_argument("--fail-if-missing-ids", action="store_true", help="Fail if heuristic audit finds screens with interactive elements but zero accessibility IDs")
    p_ingest.set_defaults(func=cmd_ingest)

    p_query = sub.add_parser("query")
    p_query.add_argument("--persist", required=True, help="Chroma persist directory")
    p_query.add_argument("--collection", default="ios_app", help="Chroma collection name")
    p_query.add_argument("--embed-model", default=DEFAULT_EMBED_MODEL, help="Embedding model name")
    p_query.add_argument("--q", required=True, help="Query text (e.g. 'login invalid password')")
    p_query.add_argument("--k", type=int, default=8, help="Top-k results")
    p_query.set_defaults(func=cmd_query)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
