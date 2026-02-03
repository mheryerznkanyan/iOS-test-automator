# Homebrew Formula for iOS Test Automator
class IosTestAutomator < Formula
  include Language::Python::Virtualenv

  desc "AI-powered iOS test automation tool with RAG-enhanced test generation"
  homepage "https://github.com/yourusername/iOS-test-automator"
  url "https://github.com/yourusername/iOS-test-automator/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256"
  license "MIT"
  head "https://github.com/yourusername/iOS-test-automator.git", branch: "main"

  depends_on "python@3.11"
  depends_on :macos
  depends_on xcode: ["15.0", :build]

  # Python dependencies
  resource "fastapi" do
    url "https://files.pythonhosted.org/packages/source/f/fastapi/fastapi-0.115.8.tar.gz"
    sha256 "REPLACE_WITH_SHA256"
  end

  resource "uvicorn" do
    url "https://files.pythonhosted.org/packages/source/u/uvicorn/uvicorn-0.30.6.tar.gz"
    sha256 "REPLACE_WITH_SHA256"
  end

  resource "langchain-anthropic" do
    url "https://files.pythonhosted.org/packages/source/l/langchain-anthropic/langchain_anthropic-0.3.5.tar.gz"
    sha256 "REPLACE_WITH_SHA256"
  end

  resource "chromadb" do
    url "https://files.pythonhosted.org/packages/source/c/chromadb/chromadb-0.5.23.tar.gz"
    sha256 "REPLACE_WITH_SHA256"
  end

  resource "sentence-transformers" do
    url "https://files.pythonhosted.org/packages/source/s/sentence-transformers/sentence_transformers-3.0.1.tar.gz"
    sha256 "REPLACE_WITH_SHA256"
  end

  resource "streamlit" do
    url "https://files.pythonhosted.org/packages/source/s/streamlit/streamlit-1.32.0.tar.gz"
    sha256 "REPLACE_WITH_SHA256"
  end

  def install
    # Create virtualenv
    virtualenv_install_with_resources

    # Install the application
    libexec.install Dir["*"]

    # Create CLI wrapper script
    (bin/"ios-test-automator").write <<~EOS
      #!/bin/bash
      export IOS_TEST_AUTOMATOR_HOME="#{libexec}"
      export PYTHONPATH="#{libexec}:$PYTHONPATH"

      case "$1" in
        server|backend)
          cd "#{libexec}/python-backend" && "#{libexec}/bin/python" main.py "${@:2}"
          ;;
        ui|streamlit)
          cd "#{libexec}/streamlit-ui" && "#{libexec}/bin/streamlit" run app.py "${@:2}"
          ;;
        rag)
          cd "#{libexec}/python-rag" && "#{libexec}/bin/python" ios_rag_mvp.py "${@:2}"
          ;;
        init)
          "#{libexec}/bin/ios-test-automator-init"
          ;;
        *)
          echo "iOS Test Automator v#{version}"
          echo ""
          echo "Usage: ios-test-automator <command> [options]"
          echo ""
          echo "Commands:"
          echo "  server     Start the FastAPI backend server"
          echo "  ui         Launch the Streamlit web interface"
          echo "  rag        Manage RAG vector store"
          echo "  init       Initialize configuration and API keys"
          echo ""
          echo "Examples:"
          echo "  ios-test-automator server              # Start backend on http://localhost:8000"
          echo "  ios-test-automator ui                  # Launch UI on http://localhost:8501"
          echo "  ios-test-automator rag ingest --help   # See RAG indexing options"
          ;;
      esac
    EOS

    # Create init script
    (bin/"ios-test-automator-init").write <<~EOS
      #!/bin/bash

      echo "🚀 iOS Test Automator - Initialization"
      echo ""

      # Create config directory
      CONFIG_DIR="$HOME/.ios-test-automator"
      mkdir -p "$CONFIG_DIR"

      # Create .env file if it doesn't exist
      if [ ! -f "$CONFIG_DIR/.env" ]; then
        cat > "$CONFIG_DIR/.env" << 'EOF'
# iOS Test Automator Configuration
# Generated on $(date)

# Anthropic API Key (required)
ANTHROPIC_API_KEY=sk-ant-...

# Backend Configuration
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# RAG Configuration
RAG_PERSIST_DIR=$HOME/.ios-test-automator/rag_store
RAG_COLLECTION=ios_app
RAG_TOP_K=10

# Streamlit Configuration
STREAMLIT_PORT=8501

# Simulator Configuration (will be auto-detected)
# SIMULATOR_ID=auto
# SIMULATOR_NAME=iPhone 17
EOF
        echo "✅ Created config file at: $CONFIG_DIR/.env"
        echo ""
        echo "⚠️  IMPORTANT: Edit the config file and add your ANTHROPIC_API_KEY:"
        echo "   nano $CONFIG_DIR/.env"
      else
        echo "✅ Config file already exists at: $CONFIG_DIR/.env"
      fi

      # Create RAG store directory
      mkdir -p "$CONFIG_DIR/rag_store"
      mkdir -p "$CONFIG_DIR/recordings"

      echo ""
      echo "📦 Directory structure created:"
      echo "   - Config: $CONFIG_DIR/.env"
      echo "   - RAG Store: $CONFIG_DIR/rag_store"
      echo "   - Recordings: $CONFIG_DIR/recordings"
      echo ""
      echo "🎯 Next steps:"
      echo "   1. Add your API key: nano $CONFIG_DIR/.env"
      echo "   2. Index your iOS app: ios-test-automator rag ingest --app-dir /path/to/your/app"
      echo "   3. Start the backend: ios-test-automator server"
      echo "   4. Open the UI: ios-test-automator ui"
      echo ""
    EOS

    chmod 0755, bin/"ios-test-automator"
    chmod 0755, bin/"ios-test-automator-init"
  end

  def caveats
    <<~EOS
      🎉 iOS Test Automator has been installed!

      Before using:
      1. Initialize the configuration:
         ios-test-automator init

      2. Add your Anthropic API key to:
         ~/.ios-test-automator/.env

      3. Index your iOS application:
         ios-test-automator rag ingest --app-dir /path/to/your/ios/app

      Quick start:
      1. Start backend:  ios-test-automator server
      2. Launch UI:      ios-test-automator ui (in new terminal)
      3. Open browser:   http://localhost:8501

      Documentation: https://github.com/yourusername/iOS-test-automator
      Issues: https://github.com/yourusername/iOS-test-automator/issues
    EOS
  end

  test do
    # Test the CLI
    system bin/"ios-test-automator", "--help"

    # Test Python installation
    system libexec/"bin/python", "-c", "import fastapi; import langchain_anthropic; import chromadb"
  end
end
