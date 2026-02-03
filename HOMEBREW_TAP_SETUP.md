# Homebrew Tap Setup Guide

This guide explains how to set up and maintain a Homebrew tap for iOS Test Automator.

## What is a Homebrew Tap?

A Homebrew "tap" is a third-party repository that contains formulae (installation recipes) for Homebrew packages. By creating a tap, users can install your tool with:

```bash
brew tap yourusername/tap
brew install ios-test-automator
```

## Step 1: Create a Homebrew Tap Repository

### 1.1 Create the Repository

On GitHub, create a new repository named: `homebrew-tap` (or `homebrew-ios`)

The naming convention must be `homebrew-*` for Homebrew to recognize it.

```bash
# Create the repository on GitHub
gh repo create yourusername/homebrew-tap --public --description "Homebrew formulae for iOS Test Automator"

# Clone it locally
git clone https://github.com/yourusername/homebrew-tap.git
cd homebrew-tap

# Create Formula directory
mkdir -p Formula

# Copy the formula
cp ../iOS-test-automator/Formula/ios-test-automator.rb Formula/

# Commit and push
git add Formula/ios-test-automator.rb
git commit -m "Add iOS Test Automator formula"
git push origin main
```

### 1.2 Repository Structure

Your tap repository should look like this:

```
homebrew-tap/
├── Formula/
│   └── ios-test-automator.rb
└── README.md
```

## Step 2: Update Formula URLs

Before releasing, update the formula with correct URLs and SHA256 checksums.

### 2.1 Create a GitHub Release

```bash
# In your iOS-test-automator repo
cd iOS-test-automator

# Create a tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Or use GitHub CLI to create release
gh release create v1.0.0 --generate-notes
```

### 2.2 Package the Source

```bash
# Create the tarball
./scripts/package.sh 1.0.0

# Upload to GitHub Release
gh release upload v1.0.0 dist/ios-test-automator-1.0.0.tar.gz
```

### 2.3 Get SHA256 Checksum

```bash
# Calculate SHA256 of the release tarball
shasum -a 256 dist/ios-test-automator-1.0.0.tar.gz

# Or download from GitHub and calculate
curl -L https://github.com/yourusername/iOS-test-automator/archive/refs/tags/v1.0.0.tar.gz | shasum -a 256
```

### 2.4 Update Formula

Edit `Formula/ios-test-automator.rb`:

```ruby
url "https://github.com/yourusername/iOS-test-automator/archive/refs/tags/v1.0.0.tar.gz"
sha256 "YOUR_ACTUAL_SHA256_HERE"
```

## Step 3: Test the Formula

Before publishing, test the formula locally:

```bash
# Test installation from local formula
brew install --build-from-source Formula/ios-test-automator.rb

# Test the installed CLI
ios-test-automator --help
ios-test-automator init

# Uninstall
brew uninstall ios-test-automator
```

## Step 4: Publish the Tap

```bash
cd homebrew-tap

# Add updated formula
git add Formula/ios-test-automator.rb
git commit -m "Update to v1.0.0"
git push origin main
```

## Step 5: Users Can Now Install

Users can now install your tool with:

```bash
# Add your tap
brew tap yourusername/tap

# Install the formula
brew install ios-test-automator

# Or in one command
brew install yourusername/tap/ios-test-automator
```

## Maintaining the Tap

### Releasing New Versions

When you release a new version:

1. **Create a new Git tag**:
   ```bash
   git tag -a v1.1.0 -m "Release v1.1.0"
   git push origin v1.1.0
   ```

2. **Create GitHub Release**:
   ```bash
   gh release create v1.1.0 --generate-notes
   ```

3. **Update the formula**:
   ```bash
   # Get new SHA256
   curl -L https://github.com/yourusername/iOS-test-automator/archive/refs/tags/v1.1.0.tar.gz | shasum -a 256

   # Update Formula/ios-test-automator.rb with new URL and SHA256
   ```

4. **Test and push**:
   ```bash
   brew install --build-from-source Formula/ios-test-automator.rb
   brew test ios-test-automator
   brew uninstall ios-test-automator

   # Commit and push
   git add Formula/ios-test-automator.rb
   git commit -m "Update to v1.1.0"
   git push origin main
   ```

### Automated Updates (Optional)

You can automate formula updates using the GitHub Action included in `.github/workflows/release.yml`.

The workflow will:
1. Create a release when you push a tag
2. Build the package
3. Calculate SHA256
4. Update the formula
5. Test installation

## Alternative: Submit to Homebrew Core

If your tool becomes popular, you can submit it to the official Homebrew repository:

1. The tool must be notable/widely used
2. Must have stable releases
3. Must have good documentation
4. Submit a PR to https://github.com/Homebrew/homebrew-core

For most projects, a personal tap is the better option.

## Troubleshooting

### Formula Not Found

If users get "formula not found":
- Ensure repo is named `homebrew-*`
- Ensure formula is in `Formula/` directory
- Ask user to run: `brew update`

### Installation Fails

If installation fails:
- Check Python dependencies are correct
- Verify SHA256 matches the release tarball
- Test locally: `brew install --debug --verbose Formula/ios-test-automator.rb`

### Outdated Formula

If formula is outdated:
- Run: `brew update` to refresh tap
- Reinstall: `brew reinstall ios-test-automator`

## Example Tap Repositories

- https://github.com/stripe/homebrew-stripe-cli
- https://github.com/kong/homebrew-kong
- https://github.com/derailed/homebrew-k9s

## Resources

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Creating Taps](https://docs.brew.sh/How-to-Create-and-Maintain-a-Tap)
- [Python Formulae](https://docs.brew.sh/Python-for-Formula-Authors)
- [brew Formula API](https://rubydoc.brew.sh/Formula)

---

**Ready to publish?**

1. Create your `homebrew-tap` repository
2. Run `./scripts/package.sh 1.0.0`
3. Create a GitHub release: `gh release create v1.0.0`
4. Update and push the formula
5. Announce to users! 🎉
