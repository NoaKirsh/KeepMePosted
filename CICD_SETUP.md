# CI/CD Setup Guide

Automated testing with GitHub Actions.

## What is CI/CD?

**CI/CD** = Continuous Integration / Continuous Deployment

GitHub automatically runs your tests every time you push code.

## What You Get

- Runs all tests on every push
- Tests on Python 3.10, 3.11, and 3.12 (**matrix testing**)
- Code quality checks (Ruff linter, Black formatter)
- Shows ✅/❌ status on GitHub

## Setup (One-Time)

### Step 1: Push to GitHub

```bash
cd KeepMePosted
git add .
git commit -m "ci: add GitHub Actions testing pipeline"
git push origin master
```

### Step 2: That's It!

Go to your GitHub repo → **Actions** tab → Watch tests run automatically

## How It Works

The `.github/workflows/ci.yml` file tells GitHub:

```yaml
on:
  push:  # Run on every push
  pull_request:  # Run on every PR
```

GitHub then:
1. Creates a fresh Ubuntu VM
2. Installs Python (3.10, 3.11, 3.12)
3. Installs your dependencies
4. Runs your tests
5. Reports results

## Matrix Testing Explained

```yaml
matrix:
  python-version: ["3.10", "3.11", "3.12"]
```

This runs **3 test jobs in parallel**:
- Job 1: Tests on Python 3.10
- Job 2: Tests on Python 3.11
- Job 3: Tests on Python 3.12

**Why?** Ensures your code works for all users, regardless of their Python version.

## Local Development

Run the same checks locally **before** pushing:

```bash
python scripts/run_tests.py
```

This runs all tests with coverage, Black formatting check, and Ruff linter.

## Files Explained

| File | Purpose |
|------|---------|
| `.github/workflows/ci.yml` | GitHub Actions configuration (what to run) |
| `pyproject.toml` | Tool configuration (pytest, black, ruff settings) |
| `scripts/run_tests.py` | Local testing script (same checks as CI) |

## Troubleshooting

### Tests Pass Locally But Fail on GitHub

**Common causes:**
1. **Python version difference** - CI tests on 3.10, 3.11, 3.12
2. **Missing dependency** - Check `requirements.txt`
3. **OS difference** - CI runs on Ubuntu (Linux)

**Solution:** Check the GitHub Actions logs for the exact error.

### How to View Logs

1. Go to GitHub → **Actions** tab
2. Click on the failed workflow
3. Click on the failed job
4. Expand the failed step to see error details

## FAQ

**Q: Do I need to install anything?**  
A: No, GitHub Actions runs on GitHub's servers.

**Q: Does it cost money?**  
A: No, it's free for public repos.

**Q: Can I disable it?**  
A: Yes, delete `.github/workflows/ci.yml`

**Q: Why don't linter failures block the build?**  
A: They have `continue-on-error: true` - only test failures block.
