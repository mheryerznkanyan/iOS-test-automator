# iOS Test Automator - Quick Reference Card

Keep this handy for quick access to common commands and workflows.

---

## 🚀 Quick Start (First Time)

```bash
# 1. Install
brew install yourusername/tap/ios-test-automator

# 2. Initialize
ios-test-automator init

# 3. Configure API key
ios-test-automator config
# Add: ANTHROPIC_API_KEY=sk-ant-...

# 4. Index your app
ios-test-automator rag ingest --app-dir ~/Projects/MyApp/Sources

# 5. Start backend (Terminal 1)
ios-test-automator server

# 6. Start UI (Terminal 2)
ios-test-automator ui

# 7. Open browser
open http://localhost:8501
```

---

## 📱 Daily Usage

```bash
# Check status
ios-test-automator status

# Start backend
ios-test-automator server

# Start UI (new terminal)
ios-test-automator ui

# Open UI in browser
open http://localhost:8501
```

---

## 🔧 Common Commands

| Command | What it does |
|---------|-------------|
| `ios-test-automator init` | Initialize config files |
| `ios-test-automator server` | Start backend API |
| `ios-test-automator ui` | Start web interface |
| `ios-test-automator config` | Edit configuration |
| `ios-test-automator status` | Check system health |
| `ios-test-automator version` | Show version |
| `ios-test-automator help` | Show help |

---

## 📊 RAG Commands

| Command | What it does |
|---------|-------------|
| `ios-test-automator rag ingest --app-dir /path` | Index your iOS app |
| `ios-test-automator rag query "login button"` | Search for elements |
| `ios-test-automator rag stats` | Show index statistics |

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Web UI | http://localhost:8501 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 📁 File Locations

| What | Where |
|------|-------|
| Config | `~/.ios-test-automator/.env` |
| RAG Store | `~/.ios-test-automator/rag_store` |
| Recordings | `~/.ios-test-automator/recordings` |

---

## ✍️ Writing Test Descriptions

### Good Examples

```
✅ Test login with email test@example.com and password password123,
   tap login button, verify home screen appears

✅ Test navigation: tap Settings tab, tap Profile button,
   verify profile screen shows user email

✅ Test form validation: enter invalid email "notanemail",
   tap submit, verify error message "Invalid email" appears

✅ Test logout: tap logout button, verify return to login screen
```

### Structure

```
[Action] what to do, [Verify] what to check
```

### Keywords

- **Actions**: tap, enter, scroll, swipe, type, select
- **Verifications**: verify, check, ensure, confirm
- **Elements**: button, field, screen, tab, label, text

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend won't start | Check API key: `ios-test-automator config` |
| No UI elements found | Re-index app: `ios-test-automator rag ingest --app-dir /path` |
| Simulator not found | List simulators: `xcrun simctl list devices` |
| UI shows "Backend Offline" | Start backend: `ios-test-automator server` |
| Build failed | Open Xcode and check for errors |

---

## 📞 Getting Help

| Need | Resource |
|------|----------|
| Documentation | `cat ~/.ios-test-automator/USER_GUIDE.md` |
| Help | `ios-test-automator help` |
| Status check | `ios-test-automator status` |
| GitHub Issues | https://github.com/yourusername/iOS-test-automator/issues |

---

## ⚙️ Configuration Keys

Add these to `~/.ios-test-automator/.env`:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-...

# Optional
BACKEND_PORT=8000
STREAMLIT_PORT=8501
RAG_TOP_K=10
SIMULATOR_NAME="iPhone 17"
```

---

## 🎯 Workflow

```
1. Index app → 2. Start backend → 3. Start UI → 4. Create test → 5. Review results
     ↓              ↓                 ↓              ↓                ↓
  (once)        (daily)          (daily)        (many times)    (watch video)
```

---

## 💡 Tips

- ✅ **Be specific** in test descriptions
- ✅ **Include verifications** (always check results)
- ✅ **Use actual values** ("test@example.com" not "valid email")
- ✅ **One test per flow** (don't combine unrelated actions)
- ✅ **Watch videos** (they show what really happened)
- ✅ **Re-index after changes** (when app code changes)

---

## 🔥 Hot Keys

| Key | Action |
|-----|--------|
| `Cmd+K` | Focus test description field (in UI) |
| `Cmd+Enter` | Generate & Run (in UI) |
| `Ctrl+C` | Stop backend/UI (in terminal) |

---

## 📊 Test Results

| Icon | Meaning |
|------|---------|
| ✅ PASSED | Test completed successfully |
| ❌ FAILED | Test failed (check logs) |
| ⏱️ Duration | How long test took |
| 📹 Video | Click to watch recording |
| 📝 Logs | Click to see details |

---

## 🚨 Emergency Commands

```bash
# Stop all services
pkill -f "ios-test-automator"

# Reset configuration
rm -rf ~/.ios-test-automator
ios-test-automator init

# Clear RAG store
rm -rf ~/.ios-test-automator/rag_store
ios-test-automator rag ingest --app-dir /path

# Check if services are running
lsof -i :8000  # Backend
lsof -i :8501  # UI
```

---

## 📦 Update

```bash
# Homebrew
brew update
brew upgrade ios-test-automator

# Verify version
ios-test-automator version
```

---

## 🎓 Learn More

| Topic | Command |
|-------|---------|
| Full user guide | `open ~/.ios-test-automator/USER_GUIDE.md` |
| Quick start | `cat ~/.ios-test-automator/QUICK_START.md` |
| RAG details | `cat ~/.ios-test-automator/RAG_INTEGRATION.md` |

---

**Print this page and keep it near your desk!** 📄

For detailed help: `ios-test-automator help` or visit the [documentation](https://github.com/yourusername/iOS-test-automator)
