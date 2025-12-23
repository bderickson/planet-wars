# 🔍 Understanding This Workflow

## What Does This Do?

This GitHub Actions workflow automatically runs your test suite every time you:
1. Push code to any branch
2. Create or update a pull request
3. Manually trigger it from GitHub's Actions tab

## Step-by-Step Breakdown

### Triggers (`on:`)
```yaml
on:
  push:
    branches: [ "**" ]  # "**" means all branches
  pull_request:
    branches: [ "**" ]
  workflow_dispatch:    # Adds "Run workflow" button in GitHub UI
```

### Jobs (`jobs:`)
A workflow can have multiple jobs. We have one called `test`.

### Runner (`runs-on:`)
```yaml
runs-on: ubuntu-latest
```
This tells GitHub to use their latest Ubuntu (Linux) server. Free tier includes:
- Ubuntu runners: ✅ Free for public repos
- macOS runners: ✅ Free but slower (limited minutes)
- Windows runners: ✅ Free for public repos

### Strategy Matrix (`strategy:`)
```yaml
strategy:
  matrix:
    python-version: ["3.11"]
```
This allows testing on multiple Python versions. Currently set to 3.11, but you could add:
```yaml
python-version: ["3.10", "3.11", "3.12"]
```
This would run the ENTIRE workflow 3 times (once per version).

### Steps

#### 1. Checkout Code (`actions/checkout@v4`)
- **What it does**: Downloads your repository code to the runner
- **Why**: The runner starts empty, needs your code first
- **Cost**: Free, provided by GitHub

#### 2. Setup Python (`actions/setup-python@v5`)
- **What it does**: Installs specified Python version
- **Why**: Ensures consistent Python environment
- **Cost**: Free, provided by GitHub

#### 3. Install System Dependencies
```bash
sudo apt-get install -y python3-pygame ffmpeg libsdl2-mixer-2.0-0
```
- **python3-pygame**: Pygame system libraries
- **ffmpeg**: Required for audio processing (pydub uses this)
- **libsdl2-mixer**: Audio playback support

#### 4. Install pipenv
```bash
pip install pipenv
```
- Installs your dependency manager

#### 5. Install Project Dependencies
```bash
pipenv install --dev
```
- Installs everything from Pipfile
- `--dev` includes pytest, coverage tools, etc.

#### 6-7. Run Tests
```bash
pipenv run pytest tests/unit/ -v --tb=short
pipenv run pytest tests/integration/ -v --tb=short
```
- Runs unit tests first, then integration
- **If any test fails, the workflow FAILS** ❌
- Separate steps show which suite failed

#### 8. Generate Coverage
```bash
pipenv run pytest --cov=game --cov-report=term --cov-report=xml
```
- Measures what % of your code is tested
- Creates `coverage.xml` report

#### 9. Upload Artifact
```yaml
uses: actions/upload-artifact@v4
with:
  name: coverage-report
  path: coverage.xml
```
- Saves coverage report for 90 days
- Download from GitHub Actions tab

## Viewing Results

After pushing to GitHub:
1. Go to your repo
2. Click **"Actions"** tab
3. See all workflow runs
4. Click any run to see detailed logs
5. Green ✅ = passed, Red ❌ = failed

## Status Badge

Add this to your README.md to show build status:

```markdown
![Tests](https://github.com/YOUR_USERNAME/planet_wars/actions/workflows/tests.yml/badge.svg)
```

Replace `YOUR_USERNAME` with your GitHub username.

## Free Tier Limits

**For public repositories:**
- ✅ Unlimited minutes on Ubuntu runners
- ✅ Unlimited storage for artifacts (90-day retention)
- ✅ Unlimited concurrent jobs

**For private repositories (if you make it private):**
- 2,000 minutes/month of Ubuntu runner time
- 500 MB artifact storage

## Modifying the Workflow

Want to add linting? Add a step:
```yaml
- name: Run linter
  run: |
    pipenv run pylint game/
```

Want to test on multiple Python versions?
```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

Want to run on multiple OS?
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ["3.11"]
runs-on: ${{ matrix.os }}
```

## Common Issues

**Issue**: "pipenv: command not found"
- **Fix**: Already handled in workflow with `pip install pipenv`

**Issue**: Pygame import fails
- **Fix**: Already handled with system dependency installation

**Issue**: Tests pass locally but fail in CI
- **Fix**: Check Python version matches, check file paths are correct

## Next Steps

1. Push this workflow to GitHub
2. Check Actions tab
3. See tests run automatically
4. Add status badge to README
5. All future pushes will be tested automatically! 🎉

