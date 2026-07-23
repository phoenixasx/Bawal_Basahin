# Bawal Basahin 'To Kung Pagod Ka - Facebook Automation Agent

A production-ready Python automation agent that replicates your n8n workflow for posting engaging Filipino content to Facebook. This agent runs completely free on GitHub Actions with secure credential management.

## 🎯 What This Does

This automation agent:

- **Generates contextual posts** using Google Gemini 2.5 Flash with rotating personas (Malditang Relihiyosa, Malditong Banal, Marites Eme)
- **Creates cinematic images** using Pollinations.ai (no text/letters, pure visual storytelling)
- **Fetches trending news** from NewsAPI to keep posts timely and relevant
- **Posts to Facebook** with proper formatting and Bible verse comments
- **Logs everything** to Google Sheets for tracking and analytics
- **Runs on a schedule** via GitHub Actions (completely free, no server needed)

## ✨ Key Features

✅ **Deterministic Persona Selection** - Same persona for the week, different vibes each day  
✅ **Smart Scheduling** - Different times for different days (Mon-Thu 12PM, Fri 6PM, Sat 10AM, Sun 8AM UTC)  
✅ **Error Resilience** - Graceful fallbacks if any API fails  
✅ **Secure Credentials** - All secrets stored in GitHub Secrets, never in code  
✅ **Comprehensive Logging** - Track every post, error, and execution  
✅ **Zero Cost** - GitHub Actions free tier covers all your needs  

## 🚀 Quick Start

### 1. Fork/Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/facebook-automation.git
cd facebook-automation
```

### 2. Get Your API Keys

You'll need 3 API keys (all free tiers available):

#### Google Gemini API
1. Go to https://aistudio.google.com/app/apikeys
2. Click "Create API Key"
3. Copy the key

#### Facebook Page Access Token
1. Go to https://developers.facebook.com/
2. Create an app (if you don't have one)
3. Add "Facebook Login" product
4. Go to Tools → Graph API Explorer
5. Select your page from the dropdown
6. Generate a Page Access Token
7. **Important:** Use the "Get Page Access Token" button to get a long-lived token (doesn't expire)

#### NewsAPI Key
1. Go to https://newsapi.org/
2. Sign up for free
3. Copy your API key

### 3. Add Secrets to GitHub

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Click "New repository secret" and add:
   - `GEMINI_API_KEY` → Your Gemini key
   - `FACEBOOK_ACCESS_TOKEN` → Your Facebook page token
   - `NEWSAPI_KEY` → Your NewsAPI key
   - `GOOGLE_SHEETS_ID` (optional) → Your Google Sheets ID for logging

### 4. Enable GitHub Actions

1. Go to your repo → Actions tab
2. Click "I understand my workflows, go ahead and enable them"

### 5. Test It

1. Go to Actions → Facebook Automation Post
2. Click "Run workflow" → "Run workflow"
3. Watch the logs in real-time

## 📅 Schedule

The agent posts on this schedule (all times in UTC, adjust for your timezone):

| Day | Time | PHT Time |
|-----|------|----------|
| Monday-Thursday | 12:00 PM | 8:00 PM |
| Friday | 6:00 PM | 2:00 AM (next day) |
| Saturday | 10:00 AM | 6:00 PM |
| Sunday | 8:00 AM | 4:00 PM |

**To change the schedule:** Edit `.github/workflows/post.yml` and modify the `cron` expressions.

## 🔧 Local Testing

To test the script locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Copy the example env file
cp .env.example .env

# Edit .env with your actual API keys
nano .env

# Run the script
python main.py
```

## 📊 How It Works

### Workflow Steps

1. **Persona Selection** - Rotates weekly (3 personas, repeats every 3 weeks)
2. **Vibe Selection** - Rotates daily (3 vibes: Brutal Real Talk, Relatable Comfort, Hope & Celebration)
3. **Day Config** - Pulls theme, topics, and image style for the day of week
4. **News Fetching** - Gets latest Philippines news from NewsAPI
5. **Image Generation** - Creates cinematic image prompt and generates via Pollinations.ai
6. **Post Generation** - Uses Gemini 2.5 Flash to write engaging Taglish content
7. **Facebook Posting** - Posts image + content to your Facebook page
8. **Bible Comment** - Adds a Bible verse as the first comment
9. **Logging** - Records everything for tracking

### Data Flow

```
Schedule Trigger
    ↓
Select Persona + Vibe + Day Config
    ↓
Fetch News (NewsAPI)
    ↓
Generate Image Prompt
    ↓
Generate Image (Pollinations.ai)
    ↓
Generate Post Content (Gemini)
    ↓
Post to Facebook (Graph API)
    ↓
Add Bible Verse Comment
    ↓
Log to Google Sheets (optional)
```

## 💰 Cost Breakdown

| Service | Cost | Notes |
|---------|------|-------|
| **Google Gemini 2.5 Flash** | ~$0.075 per 1M input tokens | ~$2-3/month for 1 post/day |
| **Pollinations.ai** | Free | No cost for image generation |
| **Facebook Graph API** | Free | Posting to your own page is free |
| **NewsAPI** | Free tier | 100 requests/day (plenty for 1 post/day) |
| **GitHub Actions** | Free | 2,000 minutes/month (more than enough) |
| **Google Sheets** | Free | Logging is free |

**Total Monthly Cost: ~$2-5** (just Gemini API)

## 🛠️ Customization

### Change Daily Topics

Edit `main.py` in the `_init_day_configs()` method:

```python
def _init_day_configs(self) -> Dict[int, DayConfig]:
    return {
        1: DayConfig(
            day='Monday',
            theme='Work / Hustle / Toxic Workplace',
            topics=['your custom topic 1', 'your custom topic 2']
        ),
        # ... more days
    }
```

### Change Personas

Edit the `_init_personas()` method to add new personas or modify existing ones.

### Change Schedule

Edit `.github/workflows/post.yml` and update the `cron` expressions:

```yaml
schedule:
  - cron: '0 12 * * 1'  # Monday at 12 PM UTC
  - cron: '0 14 * * 2'  # Tuesday at 2 PM UTC
  # ... more times
```

[Cron syntax reference](https://crontab.guru/)

### Add Instagram/Telegram Support

The original n8n workflow had Instagram and Telegram nodes. To add them:

1. Add methods to `FacebookAutomationAgent` class:
   ```python
   def post_to_instagram(self, image_url: str, caption: str) -> bool:
       # Implementation here
       pass
   
   def post_to_telegram(self, image_url: str, caption: str) -> bool:
       # Implementation here
       pass
   ```

2. Call them in the `run()` method after Facebook posting

## 🐛 Troubleshooting

### "GEMINI_API_KEY not set in environment"
- Check that you added the secret to GitHub Secrets
- Verify the secret name is exactly `GEMINI_API_KEY`
- Wait a few minutes after adding the secret

### "Facebook did not return a post ID"
- Check that your access token is still valid
- Verify the token has `pages_manage_posts` permission
- Try regenerating a new long-lived token

### "No articles found from NewsAPI"
- NewsAPI might be down or rate-limited
- The script has a fallback that generates a generic post
- Check your NewsAPI key is valid

### Workflow not triggering at scheduled time
- GitHub Actions can be delayed by up to 15 minutes
- Check the Actions tab to see if it ran
- Manually trigger it to test

## 📝 Logging

All executions are logged to `/tmp/facebook_automation_log.jsonl` with:
- Timestamp
- Persona used
- Vibe used
- Day and theme
- Topic selected
- News headline
- Facebook post ID
- Bible verse
- Success/failure status

## 🔐 Security Best Practices

✅ **Never commit `.env` file** - It's in `.gitignore`  
✅ **Use GitHub Secrets** - All credentials stored securely  
✅ **Rotate tokens regularly** - Especially Facebook access tokens  
✅ **Monitor logs** - Check GitHub Actions logs for errors  
✅ **Use long-lived tokens** - Facebook tokens expire; use the long-lived version  

## 📞 Support

If you encounter issues:

1. Check the GitHub Actions logs (Actions tab → workflow run)
2. Run locally with `python main.py` to see detailed errors
3. Verify all API keys are correct and have proper permissions
4. Check that your Facebook page has the correct permissions

## 🎓 Learning Resources

- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Facebook Graph API Docs](https://developers.facebook.com/docs/graph-api)
- [NewsAPI Docs](https://newsapi.org/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Cron Syntax](https://crontab.guru/)

## 📄 License

This project is provided as-is for personal use.

## 🙏 Credits

Built as a replacement for n8n workflow with improved reliability, cost-effectiveness, and ease of deployment.

---

**Happy posting! 🚀**
