# GitHub Actions Concurrency Control

## 🎯 What is Concurrency Control?

Concurrency control allows you to:
1. **Cancel outdated workflow runs** when new commits are pushed
2. **Queue runs** instead of running them in parallel
3. **Save CI/CD minutes** by not testing obsolete code
4. **Get results faster** by focusing on the latest changes

## 📝 The Implementation

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Breaking Down the Syntax

**`group:`** - Defines what makes runs "the same" for concurrency purposes

```yaml
group: ${{ github.workflow }}-${{ github.ref }}
```

- `${{ github.workflow }}` = "Tests" (your workflow name)
- `${{ github.ref }}` = The branch or PR reference
  - `refs/heads/main` for main branch
  - `refs/heads/feature-x` for feature-x branch
  - `refs/pull/123/merge` for PR #123

**Examples of groups**:
- `Tests-refs/heads/main` - All runs on main branch
- `Tests-refs/heads/feature-x` - All runs on feature-x branch
- `Tests-refs/pull/42/merge` - All runs on PR #42

**`cancel-in-progress:`** - What to do with old runs

- `true` = Cancel old runs when new one starts
- `false` = Queue new runs (wait for old ones to finish)

## 🎬 How It Works

### Scenario 1: Multiple Pushes to Same Branch

```bash
# You're on feature-branch
git commit -m "fix 1"
git push                    # ← Triggers Run #1

git commit -m "fix 2" 
git push                    # ← Triggers Run #2

git commit -m "fix 3"
git push                    # ← Triggers Run #3
```

**What happens**:
```
Run #1 (feature-branch): Started ───────► CANCELLED (by Run #2)
Run #2 (feature-branch): Started ───────► CANCELLED (by Run #3)
Run #3 (feature-branch): Started ───────► COMPLETED ✅
```

**Time saved**: ~4-6 minutes (2 cancelled runs × 2-3 min each)

### Scenario 2: Different Branches Run Independently

```bash
# On main branch
git push main              # ← Run #A (group: Tests-refs/heads/main)

# On feature branch
git push feature           # ← Run #B (group: Tests-refs/heads/feature)
```

**What happens**:
```
Run #A (main):    Started ───────► COMPLETED ✅
Run #B (feature): Started ───────► COMPLETED ✅
```

Both run because they're in **different groups** (different refs).

### Scenario 3: Pull Request Updates

```bash
# You update a PR with new commits
git push                   # ← Run #1 for PR
# Review feedback, make changes
git push                   # ← Run #2 for PR
# More fixes
git push                   # ← Run #3 for PR
```

**What happens**:
```
Run #1: Started ───────► CANCELLED (by Run #2)
Run #2: Started ───────► CANCELLED (by Run #3)
Run #3: Started ───────► COMPLETED ✅
```

Only the latest code gets tested!

## 📊 Comparison Table

| Feature | Without Concurrency | With Concurrency |
|---------|-------------------|------------------|
| **3 rapid pushes** | 3 runs × 3 min = 9 min | 1 run × 3 min = 3 min ✅ |
| **CI minutes used** | 9 minutes | 3 minutes ✅ |
| **Feedback time** | 3 minutes | 3 minutes |
| **Outdated tests** | 2 runs wasted ❌ | 0 runs wasted ✅ |
| **Results clarity** | 3 results (2 obsolete) | 1 result (current) ✅ |

## 🎨 Advanced Patterns

### Pattern 1: Different Concurrency for PRs vs Branches

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event_name }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

- **Pull requests**: Cancel old runs
- **Direct pushes**: Let all runs complete

### Pattern 2: Per-PR Concurrency (Current Default)

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

- Each branch/PR has its own group
- Multiple branches can run simultaneously
- Within a branch, only latest runs

### Pattern 3: Global Queue (One at a Time)

```yaml
concurrency:
  group: ${{ github.workflow }}
  cancel-in-progress: false
```

- Only workflow name in group (no branch)
- All runs queue up
- Only one runs at a time across ALL branches
- Useful for deployment workflows

### Pattern 4: Allow Main to Always Run

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}
```

- Feature branches: Cancel old runs
- Main branch: Never cancel (always complete)

## 🔍 What You'll See in GitHub

### Before Concurrency

Actions tab shows:
```
✅ Tests - feature-branch - commit3 (3 min ago)
❌ Tests - feature-branch - commit2 (4 min ago)  # Probably fails or times out
❌ Tests - feature-branch - commit1 (5 min ago)  # Probably fails or times out
```

### After Concurrency

Actions tab shows:
```
✅ Tests - feature-branch - commit3 (3 min ago)
🚫 Tests - feature-branch - commit2 (4 min ago) - Cancelled
🚫 Tests - feature-branch - commit1 (5 min ago) - Cancelled
```

**Much clearer!** Only one result to look at.

## 💰 Cost Implications

### For Public Repos (Free Plan)
- Unlimited minutes anyway
- **Benefit**: Faster feedback, cleaner results

### For Private Repos (Free Plan: 2,000 min/month)

**Example: 20 PRs/month, 3 pushes each, 3 min/test**

Without concurrency:
```
20 PRs × 3 pushes × 3 min = 180 minutes used
```

With concurrency:
```
20 PRs × 1 run × 3 min = 60 minutes used
Saved: 120 minutes (67% reduction!)
```

## ⚠️ Important Notes

### When Runs Get Cancelled

A run is cancelled if:
1. New commit pushed to same branch/PR
2. Run is still in progress (queued or running)
3. `cancel-in-progress: true` is set

### When Runs Are NOT Cancelled

Runs continue if:
1. Different branch/PR (different group)
2. Run already completed
3. `cancel-in-progress: false` (queuing mode)
4. Manual workflow trigger with different inputs

### Cancellation is Immediate

- Cancelled runs show up as "Cancelled" (not failed)
- No charges for cancelled time
- Cleanup steps don't run (be careful with deployments!)

## 🎯 Best Practices

### ✅ DO use concurrency for:
- Test workflows (like yours)
- Lint/format checks
- Build verification
- Preview deployments

### ❌ DON'T use cancellation for:
- Production deployments
- Database migrations
- Workflows with important cleanup steps
- Workflows that track state

### 🤔 Consider queuing (`cancel-in-progress: false`) for:
- Workflows that must complete in order
- Deployment workflows
- Release workflows
- Workflows that modify external state

## 🧪 Testing Your Concurrency

To test if it's working:

1. Make a trivial change
   ```bash
   echo "test" >> README.md
   git commit -m "test 1"
   git push
   ```

2. Immediately make another change
   ```bash
   echo "test2" >> README.md
   git commit -m "test 2"
   git push
   ```

3. Check Actions tab
   - First run should show "Cancelled"
   - Second run should complete

## 📚 Variables Reference

Common variables for `group:`:

| Variable | Value Example | Use Case |
|----------|---------------|----------|
| `github.workflow` | "Tests" | Workflow name |
| `github.ref` | "refs/heads/main" | Branch or PR |
| `github.event_name` | "push" or "pull_request" | Event type |
| `github.actor` | "username" | Who triggered |
| `github.run_id` | "1234567890" | Unique run ID |
| `github.sha` | "abc123..." | Commit SHA |

## 🎉 Your Current Setup

Your workflow now has:
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**This means**:
- ✅ Each branch/PR has independent concurrency
- ✅ Old runs cancelled when new commits pushed
- ✅ Multiple branches can run simultaneously
- ✅ Saves time and keeps results clear
- ✅ Perfect for a test workflow!

---

**Your workflow is now optimized for rapid development!** 🚀

