# Step-by-Step Setup Guide

This guide walks you through setting up the Facebook Automation Agent from scratch.

## Prerequisites

- A GitHub account (free)
- A Facebook page (not a personal profile)
- 15 minutes of your time

## Step 1: Get Your API Keys

### 1.1 Google Gemini API Key

1. Open https://aistudio.google.com/app/apikeys in your browser
2. Click the blue **"Create API Key"** button
3. Select **"Create API key in new project"**
4. Wait for it to generate
5. Click **"Copy"** to copy the key
6. **Save this somewhere safe** - you'll need it in Step 3

### 1.2 Facebook Page Access Token

This is the trickiest part. Follow carefully:

1. Go to https://developers.facebook.com/
2. If you don't have a developer account, sign up
3. Click **"My Apps"** → **"Create App"**
4. Choose **"Consumer"** as the app type
5. Fill in the app name and email
6. Click **"Create App"**
7. In the left sidebar, find **"Tools"** → **"Graph API Explorer"**
8. At the top, change the dropdown from **"me"** to your **Facebook Page name**
9. Click **"Generate Access Token"**
10. A dialog will appear showing your access token
11. **Important:** This token expires. To get a long-lived token:
    - Click the info icon next to the token
    - Click **"Open in Token Debugger"**
    - At the bottom, click **"Extend Access Token"**
    - Copy the new token
12. **Save this token** - you'll need it in Step 3

### 1.3 NewsAPI Key

1. Go to https://newsapi.org/
2. Click **"Register"** and sign up (free)
3. Verify your email
4. Go to your dashboard
5. Copy your **API Key**
6. **Save this key** - you'll need it in Step 3

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Name it `facebook-automation` (or whatever you want)
3. Choose **"Public"** or **"Private"** (private is more secure)
4. Click **"Create repository"**
5. Copy the repository URL (you'll need it next)

## Step 3: Upload the Code

### Option A: Using GitHub Web Interface (Easiest)

1. Go to your new repository
2. Click **"Add file"** → **"Upload files"**
3. Download all files from this project:
   - `main.py`
   - `requirements.txt`
   - `.env.example`
   - `README.md`
   - `.gitignore`
4. Create a folder `.github/workflows/` and upload `post.yml`
5. Drag and drop all files into GitHub
6. Click **"Commit changes"**

### Option B: Using Git Command Line

```bash
# Clone your new repository
git clone https://github.com/YOUR_USERNAME/facebook-automation.git
cd facebook-automation

# Copy all files from this project into the folder
# (You'll have: main.py, requirements.txt, .env.example, README.md, .gitignore, .github/workflows/post.yml)

# Commit and push
git add .
git commit -m "Initial commit: Facebook automation agent"
git push origin main
```

## Step 4: Add Secrets to GitHub

This is how you securely store your API keys:

1. Go to your GitHub repository
2. Click **"Settings"** (top right)
3. In the left sidebar, click **"Secrets and variables"** → **"Actions"**
4. Click the green **"New repository secret"** button
5. Add these secrets one by one:

### Secret 1: GEMINI_API_KEY
- **Name:** `GEMINI_API_KEY`
- **Value:** (paste your Gemini API key from Step 1.1)
- Click **"Add secret"**

### Secret 2: FACEBOOK_ACCESS_TOKEN
- **Name:** `FACEBOOK_ACCESS_TOKEN`
- **Value:** (paste your Facebook token from Step 1.2)
- Click **"Add secret"**

### Secret 3: NEWSAPI_KEY
- **Name:** `NEWSAPI_KEY`
- **Value:** (paste your NewsAPI key from Step 1.3)
- Click **"Add secret"**

### Secret 4 (Optional): GOOGLE_SHEETS_ID
- **Name:** `GOOGLE_SHEETS_ID`
- **Value:** (your Google Sheets ID if you want logging)
- Click **"Add secret"**

You should now see 3-4 secrets listed.

## Step 5: Enable GitHub Actions

1. Go to your repository
2. Click the **"Actions"** tab at the top
3. You should see "Facebook Automation Post" workflow listed
4. If you see a yellow warning, click **"I understand my workflows, go ahead and enable them"**

## Step 6: Test It!

### Manual Test (Recommended First)

1. Go to the **"Actions"** tab
2. Click **"Facebook Automation Post"** on the left
3. Click the blue **"Run workflow"** button
4. Click **"Run workflow"** again in the dialog
5. Watch the workflow run in real-time
6. Check your Facebook page - your post should appear!

### Scheduled Test

The workflow will automatically run on this schedule:
- **Monday-Thursday:** 12:00 PM UTC (8:00 PM Philippine Time)
- **Friday:** 6:00 PM UTC (2:00 AM next day Philippine Time)
- **Saturday:** 10:00 AM UTC (6:00 PM Philippine Time)
- **Sunday:** 8:00 AM UTC (4:00 PM Philippine Time)

Wait for the next scheduled time and check if it posts automatically.

## Step 7: Customize (Optional)

### Change the Schedule

Edit `.github/workflows/post.yml`:

1. Go to your repository
2. Click on `.github/workflows/post.yml`
3. Click the pencil icon to edit
4. Find the `schedule:` section
5. Modify the `cron` times (use https://crontab.guru/ to help)
6. Click **"Commit changes"**

### Change Topics/Personas

Edit `main.py`:

1. Go to your repository
2. Click on `main.py`
3. Click the pencil icon to edit
4. Find the `_init_day_configs()` method
5. Modify the topics for each day
6. Click **"Commit changes"**

## Troubleshooting

### Workflow doesn't run at scheduled time
- GitHub Actions can be delayed by up to 15 minutes
- Check the Actions tab to see if it ran
- Try manually triggering it first

### "Secrets not found" error
- Make sure you added all 3 required secrets
- Check the spelling of secret names (they're case-sensitive)
- Wait a few minutes after adding secrets

### Facebook post doesn't appear
- Check your Facebook page's privacy settings
- Verify the access token is still valid
- Try manually triggering the workflow to see the error logs

### "No articles found from NewsAPI"
- This is normal sometimes - the script has a fallback
- Check that your NewsAPI key is correct
- The script will still post even if news fetching fails

## What Happens When It Runs

1. **Selects a persona** - Rotates weekly between 3 personas
2. **Picks a vibe** - Changes daily (Brutal Real Talk, Relatable Comfort, Hope & Celebration)
3. **Fetches news** - Gets latest Philippines news
4. **Generates image** - Creates a cinematic image using Pollinations.ai
5. **Writes post** - Uses Gemini to write engaging Taglish content
6. **Posts to Facebook** - Uploads image and text
7. **Adds Bible verse** - Posts a Bible verse as the first comment
8. **Logs everything** - Records the post details

## Next Steps

- ✅ Check your Facebook page for the post
- ✅ Adjust the schedule if needed
- ✅ Customize topics and personas
- ✅ Add Instagram/Telegram support (optional)
- ✅ Monitor the Actions tab for any errors

## Need Help?

1. Check the GitHub Actions logs (Actions tab → workflow run)
2. Re-read the README.md for more details
3. Check that all API keys are correct
4. Verify your Facebook page has the correct permissions

---

**You're all set! Your Facebook automation is now running. 🚀**
