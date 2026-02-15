# Automated Setup Guide: Schedule → Google Photos → Samsung Fridge

## Overview

```
GitHub Actions (daily 1 AM Pacific)
    → Generates updated PNG (past days crossed out)
    → Uploads to Google Photos "Ramadan Schedule" album
    → Samsung Fridge photo widget shows latest image
```

Total cost: **$0**

---

## Part 1: Google Cloud Setup (one time, ~10 min)

### 1A. Create a Google Cloud Project
1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Click the project dropdown at the top → **New Project**
3. Name: `ramadan-fridge` → **Create**
4. Make sure this project is selected

### 1B. Enable Google Photos API
1. Go to [console.cloud.google.com/apis/library](https://console.cloud.google.com/apis/library)
2. Search for **"Photos Library API"**
3. Click it → **Enable**

### 1C. Set Up OAuth Consent Screen
1. Go to [console.cloud.google.com/apis/credentials/consent](https://console.cloud.google.com/apis/credentials/consent)
2. Choose **External** → **Create**
3. Fill in:
   - App name: `Ramadan Fridge`
   - User support email: your email
   - Developer contact: your email
4. Click **Save and Continue**
5. On "Scopes" page → **Add or Remove Scopes**
   - Search for `photoslibrary` and check both scopes
   - Click **Update** → **Save and Continue**
6. On "Test users" page → **Add Users** → add your Gmail address → **Save and Continue**

### 1D. Create OAuth Credentials
1. Go to [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
2. Click **+ Create Credentials** → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `fridge-updater`
5. Click **Create**
6. Click **Download JSON**
7. Rename the downloaded file to **`google_credentials.json`**

---

## Part 2: Get Your Tokens (one time, ~5 min)

### On your computer:

```bash
# Install dependencies
pip install google-auth-oauthlib requests

# Place google_credentials.json in the same folder as the setup script
# Then run:
python3 google_auth_setup.py
```

This will:
1. Open your browser to sign in with Google
2. Create a "Ramadan Schedule" album in Google Photos
3. Print 4 values you need — keep them handy

---

## Part 3: Add Secrets to GitHub (~2 min)

1. Go to your repo: `github.com/ahaq/samsung_fridge_ramadan_cal`
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each:

| Secret Name               | Value                           |
|---------------------------|---------------------------------|
| `GOOGLE_CLIENT_ID`        | (from setup script output)      |
| `GOOGLE_CLIENT_SECRET`    | (from setup script output)      |
| `GOOGLE_REFRESH_TOKEN`    | (from setup script output)      |
| `GOOGLE_PHOTOS_ALBUM_ID`  | (from setup script output)      |

---

## Part 4: Update Your Repo (~2 min)

Copy the new/updated files into your repo:

```bash
cd samsung_fridge_ramadan_cal

# Replace the workflow file
cp path/to/new/.github/workflows/update-schedule.yml .github/workflows/update-schedule.yml

# Add the new upload script
cp path/to/new/upload_to_google_photos.py .

# Push changes
git add -A
git commit -m "Add Google Photos upload"
git push
```

---

## Part 5: Test It

1. Go to your repo → **Actions** → **Update Ramadan Schedule**
2. Click **Run workflow**
3. Wait ~1 minute
4. Open **Google Photos** on your phone — check the "Ramadan Schedule" album
5. You should see the schedule image!

---

## Part 6: Set Up Samsung Fridge (~3 min)

1. On your fridge, go to **Photos** or **Gallery** app
2. Connect to **Google Photos** (sign in with the same Google account)
3. Select the **"Ramadan Schedule"** album
4. Set it as your photo display / photo board
5. The fridge will show the latest image from the album

Alternatively, via the **SmartThings app** on your phone:
1. Open SmartThings → select your fridge
2. Go to the display/photo settings
3. Link Google Photos → select the "Ramadan Schedule" album

---

## Done!

Every day at 1 AM Pacific, the schedule automatically updates with past days crossed out and uploads to your Google Photos album. Your fridge pulls the latest image.

No maintenance needed for the rest of Ramadan.
