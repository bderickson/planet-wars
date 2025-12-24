# 🚀 GitHub Actions Setup Guide

## Quick Start Checklist

- [ ] 1. Initialize git repository (if not already done)
- [ ] 2. Create GitHub repository
- [ ] 3. Push workflow files to GitHub
- [ ] 4. Verify Actions tab shows the workflow
- [ ] 5. Add status badge to README

## Step-by-Step Instructions

### 1. Initialize Git Repository (if needed)

```bash
cd /Users/brian.derickson/dev/personal/planet_wars
git init
```

### 2. Create `.gitignore` (already exists, but verify)

Your `.gitignore` should include:
```
# Already configured ✓
files/*
!files/README.md
*.pyc
__pycache__/
.pytest_cache/
.coverage
htmlcov/
build/
```

### 3. Create GitHub Repository

1. Go to https://github.com/new
2. Name: `planet_wars`
3. Description: "A browser-based space strategy game"
4. Public: ✅ (for free unlimited Actions)
5. Don't initialize with README (you already have one)
6. Click "Create repository"

### 4. Push to GitHub

```bash
# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Planet Wars strategy game with CI/CD"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/planet_wars.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 5. Verify GitHub Actions

1. Go to your repository on GitHub
2. Click **"Actions"** tab at the top
3. You should see "Tests" workflow
4. It will automatically run on your first push
5. Click on the run to see detailed logs

### 6. Add Status Badge to README

Add this line near the top of your `README.md`:

```markdown
# Planet Wars 🌍🚀

![Tests](https://github.com/YOUR_USERNAME/planet_wars/actions/workflows/tests.yml/badge.svg)
```

Replace `YOUR_USERNAME` with your actual GitHub username.

This creates a badge that shows:
- ✅ Green "passing" if tests pass
- ❌ Red "failing" if tests fail

## What Happens Next?

### On Every Push:
1. GitHub receives your code
2. Actions workflow triggers automatically
3. Ubuntu runner spins up (takes ~30 seconds)
4. Python 3.12 gets installed
5. Dependencies install (~1-2 minutes)
6. Unit tests run (~5 seconds)
7. Integration tests run (~5 seconds)
8. Coverage report generates
9. Results appear in Actions tab

**Total time: ~2-3 minutes per run**

### If Tests Fail:
- ❌ Workflow shows red X
- Email notification (if enabled)
- Badge turns red
- You can click through to see which test failed
- Fix the code, push again, automatic retest

### If Tests Pass:
- ✅ Workflow shows green checkmark
- Badge turns green
- Coverage report available for download
- Safe to merge pull requests

## Viewing Logs

After a workflow runs:

1. Go to Actions tab
2. Click on any workflow run
3. Click "test" job on the left
4. Expand any step to see detailed output

Example of what you'll see:
```
Run unit tests
  pipenv run pytest tests/unit/ -v --tb=short
  ============================= test session starts ==============================
  tests/unit/test_abilities.py::TestAbility::test_ability_init PASSED      [  1%]
  tests/unit/test_abilities.py::TestAbility::test_ability_activate PASSED  [  2%]
  ...
  ============================== 44 passed in 0.26s ===============================
```

## Troubleshooting

### "Workflow not found"
- Make sure files are in `.github/workflows/` directory
- Make sure file ends with `.yml` or `.yaml`
- Push the files to GitHub

### "Tests failing on GitHub but pass locally"
- Check Python version matches (3.12)
- Check all dependencies in Pipfile
- Look at the actual error in the logs

### "Workflow takes too long"
- Normal for first run (installs everything)
- Subsequent runs use cache (faster)
- 2-3 minutes is normal for your test suite

### "Want to run manually"
- Go to Actions tab
- Select "Tests" workflow
- Click "Run workflow" button
- Select branch
- Click "Run workflow"

## Advanced: Multiple Python Versions

Want to test on Python 3.11, 3.12, AND 3.13?

Edit `.github/workflows/tests.yml`:

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
```

This will run the entire test suite 3 times (one per version).

## Advanced: Multiple Operating Systems

Want to test on Linux, Windows, AND macOS?

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.12"]
runs-on: ${{ matrix.os }}
```

**Note**: macOS and Windows use more minutes on free tier for private repos.

## Cost Tracking

For public repos: **$0.00** ✅

For private repos:
- Check usage: Settings → Billing → Actions minutes
- 2,000 free minutes/month on Ubuntu
- After that: $0.008 per minute

Your test suite (3 minutes) = 500+ runs per month free

## Next Steps

After setup:
1. [ ] Push to GitHub
2. [ ] Verify workflow runs
3. [ ] Add status badge
4. [ ] Make a test change and push
5. [ ] Watch it test automatically!

## Questions?

- GitHub Actions Docs: https://docs.github.com/en/actions
- GitHub Actions Marketplace: https://github.com/marketplace?type=actions
- Workflow syntax: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions

---

**Your CI/CD is ready! Every push will now be automatically tested.** 🎉

