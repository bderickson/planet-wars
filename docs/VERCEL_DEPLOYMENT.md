# Deploying Planet Wars to Vercel

## 🚀 Quick Start

### Prerequisites
- GitHub account
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Your code pushed to GitHub

### Deployment Steps

#### 1. Push Your Code to GitHub

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

#### 2. Connect Vercel to GitHub

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Add New Project"
3. Click "Import Git Repository"
4. Select your `planet-wars` repository
5. Click "Import"

#### 3. Configure Project Settings

Vercel will auto-detect settings from `vercel.json`, but verify:

**Framework Preset**: Other
**Root Directory**: `./` (leave as is)
**Build Command**: `pipenv run pygbag --build main.py`
**Output Directory**: `build/web`
**Install Command**: `pip install pipenv && pipenv install`

#### 4. Deploy!

Click **"Deploy"** and wait ~2-3 minutes

Your game will be live at: `https://planet-wars-xxx.vercel.app`

---

## 📁 Project Structure for Vercel

```
planet_wars/
├── vercel.json          # ✅ Vercel configuration
├── main.py              # ✅ Entry point
├── Pipfile              # ✅ Dependencies
├── Pipfile.lock         # ✅ Locked versions
├── game/                # ✅ Game code
├── assets/              # ✅ Audio files
└── build/               # ⚠️ Generated (gitignored)
    └── web/             # ← Vercel serves this
        ├── index.html
        ├── planet_wars.apk
        └── favicon.png
```

---

## 🔧 Configuration Details

### `vercel.json` Explained

```json
{
  "buildCommand": "pipenv run pygbag --build main.py",
  // Runs Pygbag to convert Python → WebAssembly
  
  "outputDirectory": "build/web",
  // Tells Vercel to serve files from build/web/
  
  "installCommand": "pip install pipenv && pipenv install",
  // Installs dependencies before build
  
  "headers": [
    // Required for WebAssembly to work in browsers
    {
      "Cross-Origin-Embedder-Policy": "require-corp",
      "Cross-Origin-Opener-Policy": "same-origin"
    }
  ]
}
```

### Why These Headers?

WebAssembly requires these security headers:
- **COEP** (`require-corp`): Ensures resources are explicitly allowed
- **COOP** (`same-origin`): Isolates browsing context

Without them, your game won't load (you'll see CORS errors).

---

## 🎯 Build Process

What happens when you deploy:

```
1. Vercel clones your repo
   ↓
2. Runs: pip install pipenv && pipenv install
   (Installs Python dependencies)
   ↓
3. Runs: pipenv run pygbag --build main.py
   (Converts Python → WebAssembly)
   ↓
4. Pygbag outputs to build/web/
   - index.html (game page)
   - planet_wars.apk (WASM bundle)
   - favicon.png (icon)
   ↓
5. Vercel serves build/web/ as static site
   ↓
6. Game is live! 🎉
```

---

## 🌐 Custom Domain (Optional)

### Free Vercel Subdomain
Your game gets: `https://planet-wars-xxx.vercel.app`

### Custom Domain
1. Go to your project settings
2. Click "Domains"
3. Add your domain (e.g., `planetwars.yourdomain.com`)
4. Follow Vercel's DNS instructions

---

## 🔄 Continuous Deployment

**Automatic deploys** on every push:

```bash
git commit -m "Fix game bug"
git push origin main
# ↓ Vercel automatically:
# - Detects push
# - Runs build
# - Deploys new version
# - Live in ~2 minutes!
```

**Branch previews** for PRs:
- Open a PR → Vercel deploys preview
- Test changes before merging
- Preview URL in PR comments

---

## 🐛 Troubleshooting

### Build Fails: "Command not found: pipenv"

**Problem**: Vercel can't find pipenv

**Solution**: Check `vercel.json`:
```json
"installCommand": "pip install pipenv && pipenv install"
```

### Build Fails: "No module named 'pygame'"

**Problem**: Dependencies not installed

**Solution**: Ensure `Pipfile` includes pygame:
```toml
[packages]
pygame = "*"
pygbag = "*"
```

### Game Doesn't Load: White Screen

**Problem**: Missing CORS headers

**Solution**: Check `vercel.json` has headers section

**Verify**:
```bash
curl -I https://your-game.vercel.app/
# Should show:
# cross-origin-embedder-policy: require-corp
# cross-origin-opener-policy: same-origin
```

### Game Loads But No Audio

**Problem**: OGG files not included in build

**Solution**: Check Pygbag output includes `/assets/audio/ogg/`

**Verify**:
```bash
# After build, check:
ls build/web/
# Should see planet_wars.apk (contains all assets)
```

### Build Takes Too Long / Times Out

**Problem**: Vercel has a 5-minute build limit (free tier)

**Solution**: Optimize build
```json
// Add to vercel.json:
"github": {
  "silent": true
}
```

### Large Build Size Warning

**Problem**: planet_wars.apk is large (audio files)

**Current size**: ~2-3 MB (acceptable)
**Vercel limit**: 100 MB (you're fine)

**To reduce**:
- Remove MP3 files (only need OGG for web)
- Compress audio files further

---

## 📊 Monitoring

### Vercel Dashboard

View at `vercel.com/[your-username]/planet-wars`:

- **Deployments**: History of all builds
- **Analytics**: Page views, load times
- **Logs**: Build and runtime logs
- **Domains**: URL management

### Build Logs

If build fails:
1. Go to Deployments
2. Click failed deployment
3. Click "Build Logs"
4. See error messages

---

## 🎨 Environment Variables

If you need secrets (API keys, etc):

1. Go to Project Settings
2. Click "Environment Variables"
3. Add variables
4. Redeploy

**Access in Python**:
```python
import os
API_KEY = os.getenv('API_KEY')
```

---

## 🚦 Deployment Checklist

Before deploying, ensure:

- [ ] `vercel.json` exists
- [ ] Code pushed to GitHub
- [ ] `Pipfile` has all dependencies
- [ ] Local build works: `pipenv run pygbag --build main.py`
- [ ] `build/web/index.html` exists after build
- [ ] Git repo is public (or Vercel has access)

---

## 🎯 Best Practices

### 1. Test Locally First

```bash
# Build and test locally
pipenv run pygbag main.py

# Visit http://localhost:8000
# Verify game works
```

### 2. Use Preview Deployments

- Create feature branch
- Push to GitHub
- Vercel creates preview URL
- Test before merging

### 3. Monitor Build Times

Vercel shows build duration:
- Current: ~2-3 minutes (good!)
- If > 4 minutes: Optimize

### 4. Check Analytics

See how many people play:
- Go to Vercel Dashboard
- Click "Analytics"
- View visitors, page views

---

## 🔗 Useful Links

- **Your game**: `https://planet-wars-xxx.vercel.app` (after deploy)
- **Vercel docs**: https://vercel.com/docs
- **Pygbag docs**: https://pygame-web.github.io/
- **Project settings**: `https://vercel.com/[user]/planet-wars/settings`

---

## 🎉 After Deployment

### Share Your Game!

Add to your README:
```markdown
## 🎮 Play Online

**[Play Planet Wars →](https://planet-wars-xxx.vercel.app)**

Deployed on Vercel with automatic updates from GitHub.
```

### Update Your Badges

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/bderickson/planet-wars)
```

---

## 📈 What's Next?

After successful deployment:

1. **Test thoroughly** on different browsers
2. **Share the link** with friends
3. **Monitor analytics** to see usage
4. **Iterate** based on feedback
5. **Deploy updates** automatically

---

## 🆘 Need Help?

If deployment fails:

1. Check **Build Logs** in Vercel dashboard
2. Test **local build**: `pipenv run pygbag --build main.py`
3. Verify **vercel.json** syntax
4. Check **Vercel status**: https://www.vercel-status.com/

Common fixes:
- Clear Vercel cache (redeploy)
- Update `Pipfile.lock`: `pipenv lock`
- Check Python version compatibility

---

**Ready to deploy?** Follow Step 1-4 above and your game will be live in minutes! 🚀

