# Release Instructions

## How to Create a New Release

This project uses GitHub Actions to automatically build and release the macOS application.

### Steps to Release:

1. **Update Version** (optional, for tracking):
   - Update version in your code if you track it
   - Update CHANGELOG.md if you maintain one

2. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "Prepare release v1.0.0"
   git push origin main
   ```

3. **Create and Push a Version Tag**:
   ```bash
   # Create a new tag (use semantic versioning)
   git tag -a v1.0.0 -m "Release version 1.0.0"
   
   # Push the tag to GitHub
   git push origin v1.0.0
   ```

4. **Automatic Build**:
   - GitHub Actions will automatically trigger
   - The workflow will:
     - Build the macOS app
     - Create a DMG and ZIP file
     - Create a GitHub release
     - Upload the artifacts

5. **Monitor the Build**:
   - Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
   - Watch the "Build and Release" workflow
   - Should complete in 5-10 minutes

6. **Verify the Release**:
   - Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/releases`
   - Your new release should be published
   - Download and test the artifacts

### Version Numbering

Use [Semantic Versioning](https://semver.org/):
- **v1.0.0** - Major release (breaking changes)
- **v1.1.0** - Minor release (new features)
- **v1.0.1** - Patch release (bug fixes)

### Example Release Flow:

```bash
# Make your changes
git add .
git commit -m "Add stop button functionality"

# Push to main
git push origin main

# Create and push a new version tag
git tag -a v1.1.0 -m "Add stop button and improve error handling"
git push origin v1.1.0

# GitHub Actions will automatically build and create the release
```

### Troubleshooting

If the build fails:
1. Check the Actions tab for error logs
2. Test the build locally with `python build.py`
3. Fix issues and create a new patch version

### Manual Release (if needed)

If you need to create a release manually:

```bash
# Build locally
python build.py

# Create release on GitHub manually
# Upload dist/ElderlyCareScraper.app (zipped)
```
