# 🌐 Browser Deployment Guide

This guide walks you through deploying Planet Wars to run in the browser using Pygbag and GitHub Pages.

## 📋 Prerequisites

- Git and GitHub account
- Python 3.11 with pipenv
- Your game already has async support (✅ done!)

## 🚀 Quick Start

### 1. Install/Update Dependencies

```bash
# Make sure pygbag is installed
pipenv install

# Or if you need to update
pipenv update pygbag
```

### 2. Test Locally with Pygbag

```bash
# Build and serve locally (recommended first step!)
pipenv run pygbag --build main.py

# This will:
# - Build the game for web
# - Start a local server (usually at http://localhost:8000)
# - Open your browser automatically
```

**What to expect:**
- First build takes 2-3 minutes (downloads WebAssembly Python)
- Subsequent builds are faster (cached)
- Your game will open in the browser!

### 3. Test Your Game in Browser

Once the server starts:
1. Game should load in your browser
2. Test all features:
   - ✅ Main menu
   - ✅ Game configuration
   - ✅ Gameplay
   - ✅ Sound effects
   - ✅ Scoreboard
   - ✅ Victory/Defeat screens

**Common issues during local testing:**
- **Sounds don't work initially**: Click anywhere in the page first (browser security requirement)
- **Loading takes time**: First load downloads ~50MB of Python/WASM
- **File paths**: All assets must use relative paths (you're already doing this ✅)

---

## 📦 Deployment Options

### Option A: GitHub Pages (Recommended - Free!)

#### Step 1: Prepare Your Repository

```bash
# Make sure everything is committed
git add .
git commit -m "Prepare for browser deployment"
git push origin main
```

#### Step 2: Build for Production

```bash
# Build without serving (creates build/ folder)
pipenv run pygbag --build --template noctx.tmpl main.py

# The build/ folder contains your entire web game
```

#### Step 3: Deploy to GitHub Pages

**Option 3a: Using gh-pages branch (Automated)**

```bash
# Install gh-pages helper (one time)
pip install ghp-import

# Build and deploy in one command
pipenv run pygbag --build main.py
ghp-import -n -p -f build/

# Your game will be at:
# https://YOUR_USERNAME.github.io/planet_wars/
```

**Option 3b: Manual (More control)**

1. Go to your GitHub repository settings
2. Navigate to "Pages" section
3. Create a `gh-pages` branch:
   ```bash
   git checkout --orphan gh-pages
   git rm -rf .
   cp -r build/web/* .
   git add .
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```
4. In GitHub Settings > Pages, set source to `gh-pages` branch
5. Your game will be live at: `https://YOUR_USERNAME.github.io/planet_wars/`

---

### Option B: Itch.io (Alternative - Also Free!)

Great for game distribution with built-in community features.

#### Steps:

1. **Build your game:**
   ```bash
   pipenv run pygbag --build main.py
   ```

2. **Zip the build folder:**
   ```bash
   cd build/web
   zip -r planet-wars.zip .
   cd ../..
   ```

3. **Upload to itch.io:**
   - Create account at https://itch.io
   - Click "Upload new project"
   - Set as "HTML" project
   - Upload `planet-wars.zip`
   - Set viewport to 1200x800 (or your screen dimensions)
   - Check "This file will be played in the browser"
   - Publish!

---

## 🐛 Troubleshooting

### Build Fails

**Error: `ModuleNotFoundError: No module named 'pygbag'`**
```bash
pipenv install pygbag
```

**Error: `asyncio` issues**
✅ Your code already uses async! No changes needed.

### Game Loads But Doesn't Work

**Sounds Don't Play:**
- Browser security requires user interaction first
- Add a "Click to Start" screen (optional enhancement)
- Sounds will work after first click

**Scoreboard Doesn't Persist:**
- Browser localStorage is used instead of files
- This is normal and expected
- Scoreboard will persist per-browser

**Performance Issues:**
- First load is slow (downloading WASM Python)
- Subsequent loads are much faster
- Consider showing loading screen (pygbag does this automatically)

### Assets Not Loading

**Problem:** Images/sounds not found

**Solution:** Ensure all paths are relative:
```python
# ✅ Good
"assets/audio/sound.mp3"

# ❌ Bad
"/Users/you/project/assets/audio/sound.mp3"
```

---

## 🎮 Testing Checklist

Before deploying, test these in your browser:

- [ ] Game loads without errors
- [ ] Main menu displays correctly
- [ ] Can enter player name
- [ ] Can configure game (map size, AI, sounds)
- [ ] Gameplay works (select planets, send ships)
- [ ] Sound effects play (after first click)
- [ ] AI opponent functions
- [ ] Can win/lose game
- [ ] Victory/defeat screen shows correctly
- [ ] Scoreboard displays and saves
- [ ] Can return to menu and start new game
- [ ] No console errors in browser DevTools

---

## 📱 Mobile Support

Your game can work on mobile with some adjustments:

### Current Status:
- ✅ Touch events work as clicks
- ⚠️ UI might be cramped on small screens
- ⚠️ No on-screen controls

### Recommended Enhancements:
```python
# Detect mobile and adjust UI
import pygame
is_mobile = pygame.display.Info().current_w < 768

if is_mobile:
    # Scale UI elements
    # Adjust button sizes
    # Show touch hints
```

---

## 🔧 Advanced: Custom Domain

After deploying to GitHub Pages:

1. **Add CNAME file to gh-pages branch:**
   ```bash
   echo "planetwars.yourdomain.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Configure DNS:**
   - Add CNAME record: `planetwars` → `YOUR_USERNAME.github.io`
   - Wait for DNS propagation (5-30 minutes)

3. **Enable HTTPS:**
   - GitHub Pages will automatically provision SSL certificate
   - Check "Enforce HTTPS" in repository settings

---

## 📊 Analytics (Optional)

Track your game's usage:

### Google Analytics

Add to your build (in `index.html` after build):
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

---

## 🎯 Performance Tips

### Optimize Build Size:
1. Remove unused assets before building
2. Compress audio files (already done! ✅)
3. Use PNG instead of BMP for images

### Optimize Load Time:
```python
# In main.py, consider showing a loading screen
# Pygbag does this automatically, but you can customize:

async def show_loading_screen():
    # Your custom loading screen
    pass
```

---

## 📦 Build Artifacts

After `pygbag --build main.py`, you'll have:

```
build/web/
├── index.html          # Entry point
├── pythondev.py       # Python runtime
├── pythondev.data     # Python modules (large file)
├── pythondev.wasm     # WebAssembly Python
├── main.py            # Your game
├── game/              # Your game modules
└── assets/            # Your assets
```

**Note:** The `pythondev.data` file is ~50MB. This is normal for WASM Python.

---

## 🎉 You're Ready!

Run this command to test:

```bash
pipenv run pygbag --build main.py
```

Then visit http://localhost:8000 in your browser!

**Your game should work perfectly because:**
- ✅ Already using async/await
- ✅ Already using relative paths
- ✅ Already using pygame 2.5+
- ✅ No platform-specific code

Good luck, and enjoy seeing your game run in the browser! 🚀🌐

