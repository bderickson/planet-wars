# Codecov Setup Guide

## 🎯 What is Codecov?

Codecov is a code coverage reporting service that:
- ✅ Automatically generates coverage badges
- ✅ Comments on PRs with coverage changes
- ✅ Provides detailed coverage reports
- ✅ Tracks coverage trends over time
- ✅ Shows line-by-line coverage

## 🚀 Current Setup

Your repository is now configured with:

### 1. **GitHub Actions Integration** ✅

The workflow (`.github/workflows/tests.yml`) automatically:
- Runs pytest with coverage
- Generates `coverage.xml`
- Uploads to Codecov
- Updates badge automatically

### 2. **README Badge** ✅

Your README displays:
```markdown
[![codecov](https://codecov.io/gh/bderickson/planet-wars/branch/main/graph/badge.svg)](https://codecov.io/gh/bderickson/planet-wars)
```

This badge:
- Updates automatically after each push
- Shows current coverage percentage
- Links to detailed coverage report
- Color changes based on coverage:
  - 🟢 Green: 80%+
  - 🟡 Yellow: 60-80%
  - 🔴 Red: <60%

### 3. **PR Comments** ✅

When you open/update a PR, Codecov will automatically:
- Comment with coverage changes
- Show diff coverage (% of changed lines covered)
- Highlight which files need more tests
- Compare branch vs base coverage

## 📊 What You'll See

### Badge in README

The badge shows at the top of your README:

```
🟢 codecov: 85%
```

Click it to see full report at codecov.io!

### PR Comments

Example PR comment from Codecov:

```
## Codecov Report

Coverage: 85.23% (+2.3%) 🎉

Diff Coverage: 100% ✅

@@            Coverage Diff             @@
##             main     #42      +/-   ##
==========================================
+ Coverage   82.9%   85.2%   +2.3%     
==========================================
  Files         15      16       +1     
  Lines        450     475      +25     
==========================================
+ Hits         373     405      +32     
+ Misses        77      70       -7     

Additional details:
| File | Coverage | +/- |
|------|----------|-----|
| game/abilities.py | 100% | +5% ✅ |
| game/sound.py | 90% | -2% ⚠️ |
```

### Web Dashboard

Visit: https://codecov.io/gh/bderickson/planet-wars

Features:
- 📈 Coverage trends over time
- 🔍 Line-by-line coverage (which lines tested)
- 📁 File-by-file breakdown
- 🌿 Branch comparison
- 📊 Sunburst visualization
- 📉 Coverage graphs

## 🔐 First-Time Setup

### For Public Repositories (Your Case)

**Good news**: No setup required! 🎉

Codecov automatically:
- Detects your repo on first upload
- Creates your dashboard
- Starts tracking coverage
- No tokens/secrets needed

Just push your changes and the badge will appear!

### For Private Repositories

If you ever make the repo private:

1. Go to [codecov.io](https://codecov.io/)
2. Sign in with GitHub
3. Add your repository
4. Copy your Codecov token
5. Add as GitHub secret: `CODECOV_TOKEN`
6. Update workflow:
   ```yaml
   - uses: codecov/codecov-action@v4
     with:
       token: ${{ secrets.CODECOV_TOKEN }}
       files: ./coverage.xml
   ```

## 📖 Reading Coverage Reports

### Understanding the Numbers

**Coverage: 85%**
- 85% of your code lines are executed by tests
- Higher is better (aim for 80%+)
- 100% is possible but not always practical

**Diff Coverage: 100%**
- % of new/changed lines that are tested
- Most important for PRs
- Should be 100% or close to it

**Files/Lines/Hits/Misses**
- Files: Number of Python files
- Lines: Total executable lines
- Hits: Lines covered by tests
- Misses: Lines NOT covered

### Color Codes

🟢 **Green** (+2.3%): Coverage increased - great!
🔴 **Red** (-2.3%): Coverage decreased - needs attention
⚪ **White** (0%): No change

### Coverage Thresholds

Generally accepted standards:
- 🏆 **90%+**: Excellent
- ✅ **80-90%**: Good
- ⚠️ **70-80%**: Acceptable
- ❌ **<70%**: Needs improvement

Your current coverage: **~83%** (Good! ✅)

## 🎯 Using Coverage to Improve Code

### 1. Find Uncovered Code

On codecov.io:
1. Click on a file
2. See line-by-line coverage
3. Red lines = not tested
4. Write tests for red lines!

### 2. PR Review Process

When reviewing PRs:
1. Check Codecov comment
2. Look at diff coverage
3. If <80%, ask for more tests
4. Click "show uncovered lines"
5. Suggest specific test cases

### 3. Set Coverage Goals

In your workflow, you can add:
```yaml
- name: Check coverage threshold
  run: |
    pipenv run pytest --cov=game --cov-fail-under=80
```

This fails the build if coverage drops below 80%.

## 🔧 Advanced Configuration

### codecov.yml (Optional)

Create `.codecov.yml` in repo root for custom settings:

```yaml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%
    patch:
      default:
        target: 80%

comment:
  layout: "reach, diff, flags, files"
  behavior: default
  require_changes: false

ignore:
  - "tests/"
  - "assets/"
  - "build/"
```

### Ignore Files

By default, Codecov is smart and ignores:
- Test files
- `__init__.py`
- Migration files
- Build artifacts

## 📊 Tracking Progress

### Coverage Over Time

Codecov shows:
- Coverage per commit
- Coverage per branch
- Coverage per PR
- Trends (improving vs declining)

### Setting Up Notifications

Configure Codecov to:
- ✅ Comment on PRs (already enabled)
- 📧 Email on coverage drop
- 💬 Slack notifications
- 🪝 Webhooks

## 🐛 Troubleshooting

### Badge Not Showing

**Problem**: Badge shows "unknown"

**Solution**: 
1. Push code to trigger workflow
2. Wait 2-3 minutes for first upload
3. Refresh README
4. Check Actions tab for upload success

### Upload Failed

**Problem**: Codecov upload step fails

**Solution**:
```yaml
# Already configured in your workflow
fail_ci_if_error: false
```

This prevents workflow failure if Codecov is down.

### Coverage Seems Wrong

**Problem**: Coverage % doesn't match local run

**Causes**:
- Different files included
- Branch vs coverage
- Cache issues

**Solution**:
```bash
# Run locally to compare
pipenv run pytest --cov=game --cov-report=term
```

## 🎨 Other Badges in README

Your README now has:

### 1. **Tests Badge**
```markdown
[![Tests](https://github.com/bderickson/planet-wars/actions/workflows/tests.yml/badge.svg)](...)
```
- Shows if tests are passing
- Updates on each push
- Green = passing, Red = failing

### 2. **Codecov Badge**
```markdown
[![codecov](https://codecov.io/gh/bderickson/planet-wars/branch/main/graph/badge.svg)](...)
```
- Shows coverage percentage
- Links to detailed report
- Updates automatically

### 3. **Python Version Badge**
```markdown
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](...)
```
- Shows required Python version
- Static badge (you update manually)
- Links to Python downloads

### 4. **PRs Welcome Badge**
```markdown
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](...)
```
- Encourages contributions
- Links to your PRs page
- Shows you're open to collaboration

## 📈 Best Practices

### DO ✅
- Keep coverage above 80%
- Write tests for new features
- Check Codecov comments on PRs
- Aim for 100% diff coverage on PRs
- Use coverage to find edge cases

### DON'T ❌
- Don't obsess over 100% coverage
- Don't test trivial code
- Don't ignore falling coverage
- Don't merge PRs that tank coverage
- Don't game the system (meaningless tests)

## 🎯 Coverage Goals for Planet Wars

Current state:
- **Unit tests**: ~83% coverage
- **Integration tests**: Additional coverage
- **Overall**: ~83% (Good!)

Suggested goals:
- **Short term**: Maintain 80%+
- **Medium term**: Reach 85%+
- **Long term**: Stabilize at 85-90%

Areas that could use more tests:
- Edge cases in game logic
- Error handling paths
- UI interaction flows
- AI decision making

## 🚀 Next Steps

1. **Push your changes** to trigger first Codecov upload
2. **Check the badge** appears in README (may take 2-3 min)
3. **Open a test PR** to see Codecov comments in action
4. **Visit codecov.io/gh/bderickson/planet-wars** to explore dashboard
5. **Set up coverage goals** if desired (optional)

## 🔗 Useful Links

- **Your Coverage Dashboard**: https://codecov.io/gh/bderickson/planet-wars
- **Codecov Docs**: https://docs.codecov.com/
- **Badge Styles**: https://shields.io/
- **GitHub Actions**: https://docs.github.com/en/actions

---

**Your coverage tracking is now fully automated!** 📊✨

