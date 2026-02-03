#!/bin/bash
set -e

# iOS Test Automator - Quick Install Script
# Usage: curl -fsSL https://raw.githubusercontent.com/yourusername/iOS-test-automator/main/install.sh | bash

VERSION="${IOS_TEST_AUTOMATOR_VERSION:-1.0.0}"
INSTALL_DIR="${IOS_TEST_AUTOMATOR_DIR:-$HOME/.ios-test-automator}"
BIN_DIR="/usr/local/bin"
REPO_URL="https://github.com/yourusername/iOS-test-automator"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  iOS Test Automator Installer${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_info() { echo -e "${YELLOW}ℹ️  $1${NC}"; }

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."

    # Check macOS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This tool requires macOS"
        exit 1
    fi

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        print_info "Install with: brew install python@3.11"
        exit 1
    fi

    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is required but not installed"
        exit 1
    fi

    # Check Xcode
    if ! command -v xcodebuild &> /dev/null; then
        print_error "Xcode is required but not installed"
        print_info "Install Xcode from the Mac App Store"
        exit 1
    fi

    print_success "Prerequisites check passed"
}

# Download and install
install_ios_test_automator() {
    print_info "Installing iOS Test Automator v${VERSION}..."

    # Create install directory
    mkdir -p "$INSTALL_DIR"

    # Download tarball
    print_info "Downloading from GitHub..."
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    curl -L "${REPO_URL}/archive/refs/tags/v${VERSION}.tar.gz" -o ios-test-automator.tar.gz

    # Extract
    print_info "Extracting..."
    tar -xzf ios-test-automator.tar.gz -C "$INSTALL_DIR" --strip-components=1

    # Install Python dependencies
    print_info "Installing Python dependencies (this may take a few minutes)..."

    cd "$INSTALL_DIR/python-backend"
    pip3 install -r requirements.txt --quiet

    cd "$INSTALL_DIR/python-rag"
    pip3 install -r requirements.txt --quiet

    cd "$INSTALL_DIR/streamlit-ui"
    pip3 install -r requirements.txt --quiet

    print_success "Dependencies installed"

    # Create CLI symlink
    print_info "Creating CLI command..."
    if [ -w "$BIN_DIR" ]; then
        ln -sf "$INSTALL_DIR/scripts/ios-test-automator" "$BIN_DIR/ios-test-automator"
        print_success "CLI command created: ios-test-automator"
    else
        print_info "Creating CLI command (requires sudo)..."
        sudo ln -sf "$INSTALL_DIR/scripts/ios-test-automator" "$BIN_DIR/ios-test-automator"
    fi

    # Initialize configuration
    print_info "Initializing configuration..."
    "$INSTALL_DIR/scripts/ios-test-automator" init

    # Cleanup
    rm -rf "$TEMP_DIR"

    print_success "Installation complete!"
}

# Main installation
main() {
    print_header
    echo ""

    check_prerequisites
    echo ""

    install_ios_test_automator
    echo ""

    print_header
    print_success "iOS Test Automator is ready to use!"
    echo ""
    print_info "Next steps:"
    echo "   1. Add your Anthropic API key:"
    echo "      ${GREEN}ios-test-automator config${NC}"
    echo ""
    echo "   2. Index your iOS application:"
    echo "      ${GREEN}ios-test-automator rag ingest --app-dir /path/to/your/app${NC}"
    echo ""
    echo "   3. Start the backend:"
    echo "      ${GREEN}ios-test-automator server${NC}"
    echo ""
    echo "   4. Launch the UI (in new terminal):"
    echo "      ${GREEN}ios-test-automator ui${NC}"
    echo ""
    echo "   5. Open in browser: ${BLUE}http://localhost:8501${NC}"
    echo ""
    print_info "For help: ${GREEN}ios-test-automator help${NC}"
    echo ""
}

main
