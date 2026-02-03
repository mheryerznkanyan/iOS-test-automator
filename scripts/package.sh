#!/bin/bash
set -e

# iOS Test Automator - Packaging Script for Homebrew Release
# This script creates a distributable tarball for Homebrew

VERSION="${1:-1.0.0}"
PACKAGE_NAME="ios-test-automator-${VERSION}"
BUILD_DIR="build"
DIST_DIR="dist"

echo "📦 Packaging iOS Test Automator v${VERSION}"
echo ""

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf "$BUILD_DIR" "$DIST_DIR"
mkdir -p "$BUILD_DIR/$PACKAGE_NAME"
mkdir -p "$DIST_DIR"

# Copy application files
echo "📋 Copying application files..."

# Python backend
echo "  - Python backend"
cp -r python-backend "$BUILD_DIR/$PACKAGE_NAME/"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/python-backend/venv"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/python-backend/__pycache__"
rm -f "$BUILD_DIR/$PACKAGE_NAME/python-backend/.env"
rm -f "$BUILD_DIR/$PACKAGE_NAME/python-backend/*.log"

# Python RAG
echo "  - RAG system"
cp -r python-rag "$BUILD_DIR/$PACKAGE_NAME/"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/python-rag/.venv"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/python-rag/rag_store"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/python-rag/__pycache__"

# Streamlit UI
echo "  - Streamlit UI"
cp -r streamlit-ui "$BUILD_DIR/$PACKAGE_NAME/"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/streamlit-ui/venv"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/streamlit-ui/recordings"

# iOS sample app (optional - for examples)
echo "  - iOS sample app"
mkdir -p "$BUILD_DIR/$PACKAGE_NAME/examples"
cp -r ios-app/src/SampleApp "$BUILD_DIR/$PACKAGE_NAME/examples/"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/examples/SampleApp/DerivedData"
rm -rf "$BUILD_DIR/$PACKAGE_NAME/examples/SampleApp/.build"

# Documentation
echo "  - Documentation"
cp README.md "$BUILD_DIR/$PACKAGE_NAME/" || touch "$BUILD_DIR/$PACKAGE_NAME/README.md"
cp QUICK_START.md "$BUILD_DIR/$PACKAGE_NAME/" 2>/dev/null || true
cp FULL_PIPELINE_GUIDE.md "$BUILD_DIR/$PACKAGE_NAME/" 2>/dev/null || true
cp RAG_INTEGRATION.md "$BUILD_DIR/$PACKAGE_NAME/" 2>/dev/null || true
cp LICENSE "$BUILD_DIR/$PACKAGE_NAME/" 2>/dev/null || echo "MIT" > "$BUILD_DIR/$PACKAGE_NAME/LICENSE"

# Create version file
echo "$VERSION" > "$BUILD_DIR/$PACKAGE_NAME/VERSION"

# Create .env.example
cat > "$BUILD_DIR/$PACKAGE_NAME/.env.example" << 'EOF'
# iOS Test Automator Configuration

# Anthropic API Key (required)
ANTHROPIC_API_KEY=sk-ant-...

# Backend Configuration
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# RAG Configuration
RAG_PERSIST_DIR=~/.ios-test-automator/rag_store
RAG_COLLECTION=ios_app
RAG_TOP_K=10

# Streamlit Configuration
STREAMLIT_PORT=8501
EOF

# Create installation README
cat > "$BUILD_DIR/$PACKAGE_NAME/INSTALL.md" << 'EOF'
# iOS Test Automator - Installation

## Homebrew (Recommended)

```bash
brew tap yourusername/tap
brew install ios-test-automator
ios-test-automator init
```

## Manual Installation

1. Extract this archive
2. Install Python dependencies:
   ```bash
   cd python-backend && pip install -r requirements.txt
   cd ../python-rag && pip install -r requirements.txt
   cd ../streamlit-ui && pip install -r requirements.txt
   ```
3. Set up environment:
   ```bash
   cp .env.example python-backend/.env
   # Edit python-backend/.env and add your ANTHROPIC_API_KEY
   ```
4. Start the backend:
   ```bash
   cd python-backend && python main.py
   ```
5. Launch UI (in new terminal):
   ```bash
   cd streamlit-ui && streamlit run app.py
   ```

## Next Steps

See QUICK_START.md for usage instructions.
EOF

# Create tarball
echo "🗜️  Creating tarball..."
cd "$BUILD_DIR"
tar -czf "../$DIST_DIR/${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"
cd ..

# Calculate SHA256
echo "🔐 Calculating SHA256..."
SHA256=$(shasum -a 256 "$DIST_DIR/${PACKAGE_NAME}.tar.gz" | cut -d' ' -f1)

# Create release notes
cat > "$DIST_DIR/RELEASE_NOTES_${VERSION}.md" << EOF
# iOS Test Automator v${VERSION}

## 📦 Installation

### Homebrew
\`\`\`bash
brew tap yourusername/tap
brew install ios-test-automator
\`\`\`

### Manual
Download and extract \`${PACKAGE_NAME}.tar.gz\`, then see INSTALL.md

## 📊 Package Info

- **Version**: ${VERSION}
- **Size**: $(du -h "$DIST_DIR/${PACKAGE_NAME}.tar.gz" | cut -f1)
- **SHA256**: \`${SHA256}\`

## ✨ Features

- AI-powered iOS test generation using Claude Sonnet 4.5
- RAG-enhanced codebase context retrieval
- Natural language test descriptions
- Automatic test execution with video recording
- Beautiful Streamlit web interface

## 📝 Changelog

See CHANGELOG.md for detailed changes.
EOF

# Create SHA256 file
echo "$SHA256" > "$DIST_DIR/${PACKAGE_NAME}.tar.gz.sha256"

# Print summary
echo ""
echo "✅ Package created successfully!"
echo ""
echo "📦 Package: $DIST_DIR/${PACKAGE_NAME}.tar.gz"
echo "📏 Size: $(du -h "$DIST_DIR/${PACKAGE_NAME}.tar.gz" | cut -f1)"
echo "🔐 SHA256: $SHA256"
echo ""
echo "📋 Next steps:"
echo "   1. Test the package:"
echo "      cd $BUILD_DIR/$PACKAGE_NAME && cat INSTALL.md"
echo ""
echo "   2. Update Formula/ios-test-automator.rb with:"
echo "      url: https://github.com/yourusername/iOS-test-automator/archive/refs/tags/v${VERSION}.tar.gz"
echo "      sha256: \"$SHA256\""
echo ""
echo "   3. Create GitHub release:"
echo "      gh release create v${VERSION} $DIST_DIR/${PACKAGE_NAME}.tar.gz --notes-file $DIST_DIR/RELEASE_NOTES_${VERSION}.md"
echo ""
