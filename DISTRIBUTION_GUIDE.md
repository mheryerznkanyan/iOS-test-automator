# iOS Test Automator - Distribution Guide

Complete guide for packaging and distributing iOS Test Automator via Homebrew, direct download, and other methods.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Homebrew Distribution](#homebrew-distribution)
3. [Direct Download](#direct-download)
4. [Docker Distribution](#docker-distribution)
5. [PyPI Distribution](#pypi-distribution)
6. [CI/CD Integration](#cicd-integration)

---

## Prerequisites

### For Maintainers

- macOS with Homebrew installed
- GitHub account with repo access
- Python 3.11+
- Git and GitHub CLI (`gh`)
- Xcode 15.0+ (for testing)

### For Users

- macOS 14.0+
- Xcode 15.0+
- Homebrew (for brew installation)
- Valid Anthropic API key

---

## Homebrew Distribution

### Quick Setup

```bash
# 1. Create tap repository
gh repo create yourusername/homebrew-tap --public

# 2. Package the release
./scripts/package.sh 1.0.0

# 3. Create GitHub release
gh release create v1.0.0 dist/ios-test-automator-1.0.0.tar.gz \
  --notes-file dist/RELEASE_NOTES_1.0.0.md

# 4. Copy formula to tap
cp Formula/ios-test-automator.rb ../homebrew-tap/Formula/
cd ../homebrew-tap
git add Formula/ios-test-automator.rb
git commit -m "Add iOS Test Automator v1.0.0"
git push

# 5. Users can now install
brew tap yourusername/tap
brew install ios-test-automator
```

### Detailed Steps

See [HOMEBREW_TAP_SETUP.md](HOMEBREW_TAP_SETUP.md) for complete instructions.

### User Installation

Once published, users install with:

```bash
# One-time tap setup
brew tap yourusername/tap

# Install
brew install ios-test-automator

# Initialize
ios-test-automator init

# Add API key
nano ~/.ios-test-automator/.env

# Start using
ios-test-automator server
```

---

## Direct Download

### Creating Downloadable Packages

For users who don't use Homebrew:

#### Option 1: Pre-built Binary Package

Create a standalone installer:

```bash
# Create installer package
./scripts/create-installer.sh 1.0.0

# This creates:
# - dist/ios-test-automator-1.0.0-installer.pkg
# - dist/ios-test-automator-1.0.0-installer.dmg
```

Create [scripts/create-installer.sh](scripts/create-installer.sh):

```bash
#!/bin/bash
VERSION="${1:-1.0.0}"

# Build the package first
./scripts/package.sh "$VERSION"

# Create installer package with pkgbuild
pkgbuild --root "build/ios-test-automator-$VERSION" \
  --identifier "com.yourusername.ios-test-automator" \
  --version "$VERSION" \
  --install-location "/usr/local/ios-test-automator" \
  "dist/ios-test-automator-$VERSION-installer.pkg"

# Create DMG for easy distribution
hdiutil create -volname "iOS Test Automator $VERSION" \
  -srcfolder "dist/ios-test-automator-$VERSION-installer.pkg" \
  -ov -format UDZO \
  "dist/ios-test-automator-$VERSION-installer.dmg"

echo "✅ Installer created: dist/ios-test-automator-$VERSION-installer.dmg"
```

#### Option 2: Shell Script Installer

Create [install.sh](install.sh):

```bash
#!/bin/bash
set -e

VERSION="1.0.0"
INSTALL_DIR="$HOME/.ios-test-automator"

echo "🚀 Installing iOS Test Automator v$VERSION"

# Download and extract
echo "📥 Downloading..."
curl -L "https://github.com/yourusername/iOS-test-automator/archive/refs/tags/v$VERSION.tar.gz" \
  -o "/tmp/ios-test-automator.tar.gz"

# Extract
echo "📦 Extracting..."
mkdir -p "$INSTALL_DIR"
tar -xzf "/tmp/ios-test-automator.tar.gz" -C "$INSTALL_DIR" --strip-components=1

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd "$INSTALL_DIR/python-backend"
pip3 install -r requirements.txt

cd "$INSTALL_DIR/python-rag"
pip3 install -r requirements.txt

cd "$INSTALL_DIR/streamlit-ui"
pip3 install -r requirements.txt

# Create CLI symlink
echo "🔗 Creating CLI symlink..."
sudo ln -sf "$INSTALL_DIR/scripts/ios-test-automator" /usr/local/bin/ios-test-automator

# Initialize
echo "⚙️  Initializing..."
cp "$INSTALL_DIR/.env.example" "$INSTALL_DIR/.env"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Add your API key: nano $INSTALL_DIR/.env"
echo "  2. Start backend: ios-test-automator server"
echo "  3. Launch UI: ios-test-automator ui"
```

Users can install with:

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/iOS-test-automator/main/install.sh | bash
```

---

## Docker Distribution

### Publishing to Docker Hub

```bash
# Build and tag
docker build -t yourusername/ios-test-automator:1.0.0 -f docker/Dockerfile .
docker tag yourusername/ios-test-automator:1.0.0 yourusername/ios-test-automator:latest

# Push to Docker Hub
docker login
docker push yourusername/ios-test-automator:1.0.0
docker push yourusername/ios-test-automator:latest
```

### User Installation

Users can run with Docker:

```bash
# Pull image
docker pull yourusername/ios-test-automator:latest

# Run with docker-compose
curl -O https://raw.githubusercontent.com/yourusername/iOS-test-automator/main/docker-compose.yml
docker-compose up -d
```

---

## PyPI Distribution

For Python-first distribution:

### Setup

Create [setup.py](setup.py):

```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ios-test-automator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered iOS test automation with RAG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/iOS-test-automator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.115.0",
        "uvicorn>=0.30.0",
        "langchain-anthropic>=0.3.5",
        "chromadb>=0.5.23",
        "sentence-transformers>=3.0.1",
        "streamlit>=1.32.0",
    ],
    entry_points={
        "console_scripts": [
            "ios-test-automator=ios_test_automator.cli:main",
        ],
    },
    include_package_data=True,
)
```

### Publish to PyPI

```bash
# Build
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

### User Installation

```bash
pip install ios-test-automator
ios-test-automator init
```

---

## CI/CD Integration

### GitHub Actions for Automated Releases

The included `.github/workflows/release.yml` automates:

1. Building packages when you push a tag
2. Creating GitHub releases
3. Uploading distribution files
4. Updating Homebrew formula
5. Testing installation

### Usage

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# GitHub Actions will:
# 1. Build the package
# 2. Create release
# 3. Update formula
# 4. Test installation
```

### Manual Release Checklist

If not using automation:

- [ ] Update version in all files
- [ ] Update CHANGELOG.md
- [ ] Run tests: `pytest python-backend/tests/`
- [ ] Package: `./scripts/package.sh 1.0.0`
- [ ] Create tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create release: `gh release create v1.0.0 dist/*.tar.gz`
- [ ] Update Homebrew formula
- [ ] Test installation
- [ ] Announce on socials/docs

---

## Distribution Channels Summary

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Homebrew** | Mac developers | Easy updates, familiar tool | Mac-only, requires tap |
| **Direct Download** | Non-brew users | No dependencies | Manual updates |
| **Docker** | Cross-platform, CI/CD | Consistent environment | Larger download, simulator issues |
| **PyPI** | Python developers | pip-friendly | Python-ecosystem focused |
| **Shell Installer** | Quick setup | One-line install | Less control |

## Recommended Approach

For maximum reach:

1. **Primary**: Homebrew (best Mac experience)
2. **Secondary**: Direct download (installer.dmg)
3. **Alternative**: Docker (for CI/CD use)
4. **Optional**: PyPI (for Python-first users)

---

## Marketing Your Distribution

### 1. GitHub Repository

- Clear README with installation badges
- Animated GIF demo
- Quickstart guide
- Badges for: ![Version](https://img.shields.io/github/v/release/yourusername/iOS-test-automator)

### 2. Documentation Site

Use GitHub Pages:

```bash
# Create docs site
mkdir docs
echo "# iOS Test Automator" > docs/index.md
echo "theme: jekyll-theme-cayman" > docs/_config.yml

# Enable GitHub Pages in repo settings
```

### 3. Package Managers

- List on [Homebrew Formulae](https://formulae.brew.sh/)
- Add to [awesome-ios](https://github.com/vsouza/awesome-ios)
- Submit to iOS testing tool lists

### 4. Social Channels

- Dev.to article
- Medium post
- Twitter/X announcement
- Product Hunt launch

---

## Version Management

Use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backwards compatible
- **PATCH**: Bug fixes

Example timeline:
- v1.0.0 - Initial release
- v1.0.1 - Bug fix
- v1.1.0 - Add new feature
- v2.0.0 - Breaking API change

---

## Support & Maintenance

Set up:
- GitHub Discussions for Q&A
- Issue templates
- Contributing guide
- Code of conduct

Monitor:
- GitHub issues
- Homebrew analytics (if in core)
- PyPI download stats
- User feedback

---

## Quick Reference

```bash
# Create new release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Package
./scripts/package.sh 1.0.0

# Test locally
brew install --build-from-source Formula/ios-test-automator.rb

# Create GitHub release
gh release create v1.0.0 dist/*.tar.gz --notes-file dist/RELEASE_NOTES_1.0.0.md

# Update tap
cd homebrew-tap
cp ../iOS-test-automator/Formula/ios-test-automator.rb Formula/
git add Formula/ios-test-automator.rb
git commit -m "Update to v1.0.0"
git push
```

---

**Ready to distribute? Follow the steps above and make your tool available to the world!** 🚀
