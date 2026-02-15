# Ramadan Schedule → Samsung Fridge Display

Automatically updates your BVMCC Ramadan 1447/2026 prayer schedule daily, crossing out past days, and serves it as a web page you can bookmark on your Samsung Family Hub fridge browser.

**Cost: $0/month** — runs entirely on GitHub Actions (free) + GitHub Pages (free).

---

## How It Works

```
GitHub Actions (daily cron at 1 AM Pacific)
    ↓
Converts PDF → PNG with past days grayed out
    ↓
Commits updated image to repo
    ↓
GitHub Pages serves it as a web page
    ↓
Samsung fridge browser auto-refreshes the page every hour
```

---

## Setup (10 minutes)

### Step 1: Create the GitHub Repository

1. Go to [github.com/new](https://github.com/new) and create a new repository
   - Name: `ramadan-fridge-schedule` (or anything you like)
   - Set to **Public** (free GitHub Pages) or **Private** (still free, 2000 min/month Actions)
2. Clone it to your computer:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ramadan-fridge-schedule.git
   cd ramadan-fridge-schedule
   ```

### Step 2: Add the Files

Copy these files into the repo:
```
ramadan-fridge-schedule/
├── .github/
│   └── workflows/
│       └── update-schedule.yml    ← GitHub Actions workflow
├── docs/                          ← GitHub Pages will serve from here
│   └── (auto-generated)
├── update_schedule.py             ← The Python script
├── BVMCC_-_Ramadan_1447_2026_Athan_and_Iqama_schedule.pdf  ← Your PDF
└── README.md
```

### Step 3: Add Your PDF

Copy your BVMCC Ramadan schedule PDF into the repo root:
```bash
cp /path/to/BVMCC_-_Ramadan_1447_2026_Athan_and_Iqama_schedule.pdf .
```

### Step 4: Push to GitHub

```bash
git add -A
git commit -m "Initial setup"
git push
```

### Step 5: Enable GitHub Pages

1. Go to your repo on GitHub → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, folder: `/docs`
4. Click **Save**

### Step 6: Run It the First Time

1. Go to your repo → **Actions** tab
2. Click **"Update Ramadan Schedule"** on the left
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait ~1 minute for it to complete

### Step 7: Bookmark on Your Fridge

Your schedule is now live at:
```
https://YOUR_USERNAME.github.io/ramadan-fridge-schedule/
```

On your Samsung Family Hub fridge:
1. Open the **built-in web browser**
2. Navigate to your GitHub Pages URL
3. **Bookmark it** or add it to the home screen
4. The page auto-refreshes every hour, so it always shows the latest version

---

## That's It!

The GitHub Action runs every day at 1:00 AM Pacific and updates the image automatically. The fridge browser page refreshes itself hourly. Zero maintenance until next Ramadan.

---

## Alternative: Use SmartThings + Photo Frame

If your fridge doesn't have a browser, or you prefer the photo display:

1. Each day after the Action runs, download the updated image from:
   ```
   https://YOUR_USERNAME.github.io/ramadan-fridge-schedule/schedule.png
   ```
2. Or set up **IFTTT** to auto-download the image and sync it to your Samsung fridge photo frame

---

## Customization

Edit `update_schedule.py` to change:
- **Gray overlay opacity**: `fill=(80, 80, 80, 140)` — increase 140 for darker
- **Strikethrough color**: `fill=(220, 30, 30, 230)` — RGB + alpha
- **Strikethrough width**: `width=4`
- **Today's highlight**: Blue border around today's row (enabled by default)
- **DPI**: `DPI = 200` — increase for sharper image

Edit `.github/workflows/update-schedule.yml` to change:
- **Schedule time**: `cron: '0 8 * * *'` — currently 8:00 UTC = 1:00 AM Pacific

---

## Cost Breakdown

| Service | Cost |
|---------|------|
| GitHub Actions | Free (runs ~30 sec/day, well within 2,000 min/month limit) |
| GitHub Pages | Free (static hosting) |
| GitHub repo | Free (public or private) |
| **Total** | **$0/month** |
