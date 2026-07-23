#!/usr/bin/env python3
"""
Bawal Basahin 'To Kung Pagod Ka - Facebook Automation Agent
Replicates the n8n workflow with robust error handling and secure credential management.
"""

import os
import json
import requests
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Vibe(Enum):
    """Emotional vibes for posts"""
    BRUTAL_REAL_TALK = "Brutal Real Talk"
    RELATABLE_COMFORT = "Relatable Comfort"
    HOPE_AND_CELEBRATION = "Hope and Celebration"


class Gender(Enum):
    """Persona genders"""
    BABAE = "babae"
    LALAKI = "lalaki"
    QUEER_LGBT = "queer/LGBT"


@dataclass
class Persona:
    """Persona configuration"""
    gender: Gender
    callouts: List[str]
    flavor: str
    name: str
    tagline: str


@dataclass
class DayConfig:
    """Daily theme configuration"""
    day: str
    theme: str
    image_style: str
    image_mood: str
    ad_slogan: str
    topics: List[str]


@dataclass
class BibleVerse:
    """Bible verse reference"""
    ref: str
    url: str


class FacebookAutomationAgent:
    """Main automation agent for Facebook posting"""

    def __init__(self):
        """Initialize the agent with environment variables"""
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.facebook_access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.google_sheets_id = os.getenv('GOOGLE_SHEETS_ID')
        self.pollinations_api_key = os.getenv('POLLINATIONS_API_KEY', '')
        
        # Validate required credentials
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set in environment")
        if not self.facebook_access_token:
            raise ValueError("FACEBOOK_ACCESS_TOKEN not set in environment")
        if not self.newsapi_key:
            raise ValueError("NEWSAPI_KEY not set in environment")

        self.personas = self._init_personas()
        self.day_configs = self._init_day_configs()
        self.vibes = [Vibe.BRUTAL_REAL_TALK, Vibe.RELATABLE_COMFORT, Vibe.HOPE_AND_CELEBRATION]
        self.bible_verses = self._init_bible_verses()

    def _init_personas(self) -> List[Persona]:
        """Initialize persona configurations"""
        return [
            Persona(
                gender=Gender.BABAE,
                callouts=['sis', 'girl', 'bestie', 'ate'],
                flavor='OFW mom energy — sweet sa labas pero biblical ang wrath pag nagalit. Laging may iced coffee at receipts.',
                name='Malditang Relihiyosa',
                tagline='preach:'
            ),
            Persona(
                gender=Gender.LALAKI,
                callouts=['bro', 'pare', 'kuya', 'dude'],
                flavor='Night shift worker vibes — tahimik pero sharp. Ang honest friend na masakit pag nagsalita pero totoo naman.',
                name='Malditong Banal',
                tagline='said:'
            ),
            Persona(
                gender=Gender.QUEER_LGBT,
                callouts=['bes', 'mare', 'beh', 'teh'],
                flavor='Sabog energy, grounded values. Sass at grace sa iisang katawan. Living their truth habang exhausted sa buhay.',
                name='Marites Eme',
                tagline='spills:'
            ),
        ]

    def _init_day_configs(self) -> Dict[int, DayConfig]:
        """Initialize daily theme configurations"""
        return {
            0: DayConfig(
                day='Sunday',
                theme='Gratitude / God / Counting Blessings',
                image_style='minimalist clean white space, soft golden light, single candle or sampaguita flower, peaceful sacred airy',
                image_mood='grateful and still',
                ad_slogan='Nescafe: Sarap ng umaga',
                topics=['mga blessings na hindi napapansin kasi busy sa inggit sa iba', 'pasasalamat kahit hindi pa kumpleto ang buhay']
            ),
            1: DayConfig(
                day='Monday',
                theme='Work / Hustle / Toxic Workplace',
                image_style='bold graphic stark black and white with one red accent, harsh fluorescent office lighting',
                image_mood='exhausted but defiant',
                ad_slogan='Nike: Just Do It',
                topics=['toxic hustle culture na sinasabi pang blessing ang pagod', 'boss na hindi ka nire-respeto pero inaasahang loyal ka']
            ),
            2: DayConfig(
                day='Tuesday',
                theme='Friendships / Fake Friends / Loneliness',
                image_style='dark moody cinematic Filipino setting, empty table with two plastic chairs, city lights at night',
                image_mood='lonely but clear-eyed',
                ad_slogan='Globe: Para sa isa\'t isa',
                topics=['kaibigan na nandoon lang pag kailangan nila ng bagay sa yo', 'loneliness na mas masahol pa sa bad company']
            ),
            3: DayConfig(
                day='Wednesday',
                theme='Body / Food / Diet Culture / Health',
                image_style='Filipino warm market aesthetic, fresh vegetables and local ulam, earthy terracotta tones',
                image_mood='grounded and real',
                ad_slogan='L\'Oreal: Because you\'re worth it',
                topics=['diet culture na sinabing masama ang kumain ng masarap', 'body shaming mula sa pamilya mo mismo']
            ),
            4: DayConfig(
                day='Thursday',
                theme='Money / Utang / OFW Remittance / Financial Trauma',
                image_style='bold stark graphic, pitch black background with harsh white and gold highlights',
                image_mood='broke but building',
                ad_slogan='BDO: We find ways',
                topics=['utang na loob na ginagamit para kontrolin ka', 'family financial trauma na dinala mo sa adulthood']
            ),
            5: DayConfig(
                day='Friday',
                theme='Love / Relationships / Heartbreak',
                image_style='dark moody cinematic Filipino romance, candlelight on wooden table, rain on louvered window',
                image_mood='heartbroken but surviving',
                ad_slogan='Jollibee: Joy sa bawat sandali',
                topics=['trauma bonding na inakala mong love', 'minahal mo ng buong puso pero half-hearted lang ang binigay sa yo']
            ),
            6: DayConfig(
                day='Saturday',
                theme='Rest / Self-care / FOMO / Fun',
                image_style='Filipino golden hour aesthetic, hammock between coconut trees, warm saturated colors',
                image_mood='peaceful and present',
                ad_slogan='Spotify: Your Soundtrack',
                topics=['rest as rebellion laban sa hustle culture', 'FOMO na ginagawang toxic ang social media']
            ),
        }

    def _init_bible_verses(self) -> List[BibleVerse]:
        """Initialize Bible verse references"""
        return [
            BibleVerse(ref='Philippians 4:6-7', url='https://www.bible.com/bible/111/PHP.4.6-7'),
            BibleVerse(ref='Proverbs 31:25', url='https://www.bible.com/bible/111/PRO.31.25'),
            BibleVerse(ref='Psalm 46:5', url='https://www.bible.com/bible/111/PSA.46.5'),
            BibleVerse(ref='1 Peter 5:7', url='https://www.bible.com/bible/111/1PE.5.7'),
            BibleVerse(ref='Jeremiah 29:11', url='https://www.bible.com/bible/111/JER.29.11'),
            BibleVerse(ref='Matthew 11:28', url='https://www.bible.com/bible/111/MAT.11.28'),
            BibleVerse(ref='Proverbs 3:5-6', url='https://www.bible.com/bible/111/PRO.3.5-6'),
        ]

    def get_day_of_year(self) -> int:
        """Get day of year for deterministic persona/vibe selection"""
        now = datetime.now()
        return now.timetuple().tm_yday

    def get_week_number(self) -> int:
        """Get week number for deterministic persona selection"""
        now = datetime.now()
        return int(now.timestamp() / (7 * 24 * 60 * 60))

    def select_persona(self) -> Persona:
        """Select persona based on week number"""
        week_num = self.get_week_number()
        return self.personas[week_num % len(self.personas)]

    def select_vibe(self) -> Vibe:
        """Select vibe based on day of year"""
        day_of_year = self.get_day_of_year()
        return self.vibes[day_of_year % len(self.vibes)]

    def select_callout(self, persona: Persona) -> str:
        """Select callout for persona"""
        day_of_year = self.get_day_of_year()
        return persona.callouts[day_of_year % len(persona.callouts)]

    def get_day_config(self) -> DayConfig:
        """Get today's day configuration"""
        now = datetime.now()
        day_of_week = now.weekday()
        return self.day_configs[day_of_week]

    def fetch_news(self) -> Tuple[Optional[str], Optional[str]]:
        """Fetch trending Philippine news from NewsAPI"""
        try:
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': 'Philippines',
                'sortBy': 'publishedAt',
                'language': 'en',
                'pageSize': 5,
                'apiKey': self.newsapi_key
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            articles = response.json().get('articles', [])
            if articles:
                article = articles[0]
                return article.get('title'), article.get('url')
            
            logger.warning("No articles found from NewsAPI")
            return None, None
            
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return None, None

    def generate_image_prompt(self, day_config: DayConfig, topic: str, vibe: Vibe) -> str:
        """Generate image prompt for Pollinations.ai"""
        return f"""
        Create a cinematic, photorealistic image in Filipino aesthetic:
        
        Theme: {day_config.theme}
        Mood: {day_config.image_mood}
        Style: {day_config.image_style}
        Vibe: {vibe.value}
        Topic: {topic}
        
        Requirements:
        - NO TEXT, NO LETTERS, NO WORDS
        - Photorealistic, high quality, cinematic lighting
        - Warm, saturated colors with Filipino cultural elements
        - Atmospheric and emotionally resonant
        - 16:9 aspect ratio
        """

    def generate_image_url(self, prompt: str) -> str:
        """Generate image URL using Pollinations.ai"""
        try:
            # Pollinations.ai free endpoint
            encoded_prompt = requests.utils.quote(prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            logger.info(f"Generated image URL: {image_url}")
            return image_url
        except Exception as e:
            logger.error(f"Error generating image URL: {e}")
            # Fallback to a placeholder
            return "https://via.placeholder.com/1200x630?text=Image+Generation+Failed"

    def generate_post_content(self, 
                             persona: Persona,
                             day_config: DayConfig,
                             vibe: Vibe,
                             topic: str,
                             news_headline: Optional[str] = None) -> str:
        """Generate post content using Gemini API"""
        try:
            callout = self.select_callout(persona)
            
            prompt = f"""
            You are {persona.name}, a Taglish-speaking Filipino voice with this personality:
            {persona.flavor}
            
            Today's theme: {day_config.theme}
            Vibe: {vibe.value}
            Topic to explore: {topic}
            Callout to use: {callout}
            {f'News context: {news_headline}' if news_headline else ''}
            
            Write a Facebook post (200-300 words) that:
            1. Opens with raw, honest observation about the topic
            2. Uses Taglish naturally (mix Filipino and English)
            3. Includes the callout naturally
            4. Ends with a gentle but firm spiritual or practical truth
            5. Feels like a friend giving you real talk, not preaching
            6. Acknowledges exhaustion, struggle, or complexity without toxic positivity
            
            The tone should be {vibe.value.lower()}.
            
            Start writing immediately, no introduction or meta-commentary.
            """
            
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
            headers = {
                "x-goog-api-key": self.gemini_api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.8,
                    "maxOutputTokens": 500,
                }
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            generated_text = (result.get('candidates', [{}])[0]
                            .get('content', {})
                            .get('parts', [{}])[0]
                            .get('text', ''))
            
            if not generated_text or len(generated_text) < 50:
                logger.warning("Gemini response too short, using fallback")
                return self._get_fallback_post(persona, topic, callout)
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating post with Gemini: {e}")
            return self._get_fallback_post(persona, topic, self.select_callout(persona))

    def _get_fallback_post(self, persona: Persona, topic: str, callout: str) -> str:
        """Fallback post if Gemini fails"""
        fallback_posts = [
            f"Alam mo {callout}, ang {topic.lower()} ay isang bagay na kailangan nating harapin nang totoo. Hindi ito madali, pero kailangan nating gawin.",
            f"Sabi ko {callout}, huwag mo 'tong basahin kung pagod ka. Pero dahil nandito ka na, let me tell you about {topic.lower()}.",
            f"Real talk {callout}: {topic.lower()} ay parte ng buhay. At kailangan nating makipag-usap tungkol dito.",
        ]
        return random.choice(fallback_posts)

    def format_post(self, 
                   persona: Persona,
                   content: str,
                   callout: str) -> str:
        """Format the final post with header"""
        header = f"🤫 {persona.name} {persona.tagline}"
        first_line = f"Sabi ko nang huwag mo 'tong basahin kung pagod ka, {callout}... pero dahil mapilit ka, sige na."
        
        return f"{header}\n\n{first_line}\n\n{content}"

    def post_to_facebook(self, image_url: str, post_content: str) -> Optional[str]:
        """Post image and content to Facebook"""
        try:
            url = "https://graph.facebook.com/v25.0/me/photos"
            
            # Download image first
            img_response = requests.get(image_url, timeout=15)
            img_response.raise_for_status()
            
            files = {
                'source': ('image.jpg', img_response.content, 'image/jpeg'),
                'message': (None, post_content),
                'published': (None, 'true'),
            }
            
            params = {
                'access_token': self.facebook_access_token
            }
            
            response = requests.post(url, files=files, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get('post_id') or result.get('id')
            
            if post_id:
                logger.info(f"Successfully posted to Facebook. Post ID: {post_id}")
                return post_id
            else:
                logger.error(f"Facebook response missing post ID: {result}")
                return None
                
        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return None

    def post_first_comment(self, post_id: str, bible_verse: BibleVerse) -> bool:
        """Post Bible verse as first comment"""
        try:
            url = f"https://graph.facebook.com/v25.0/{post_id}/comments"
            
            comment_text = f"📖 {bible_verse.ref}\nBasahin dito: {bible_verse.url}"
            
            params = {
                'access_token': self.facebook_access_token,
                'message': comment_text
            }
            
            response = requests.post(url, params=params, timeout=15)
            response.raise_for_status()
            
            logger.info(f"Successfully posted first comment with Bible verse")
            return True
            
        except Exception as e:
            logger.error(f"Error posting first comment: {e}")
            return False

    def log_to_google_sheets(self, data: Dict) -> bool:
        """Log execution details to Google Sheets (optional)"""
        # This would require Google Sheets API setup
        # For now, we'll just log to file
        try:
            log_file = '/tmp/facebook_automation_log.jsonl'
            with open(log_file, 'a') as f:
                f.write(json.dumps(data) + '\n')
            logger.info(f"Logged to {log_file}")
            return True
        except Exception as e:
            logger.error(f"Error logging to file: {e}")
            return False

    def run(self) -> bool:
        """Execute the complete automation workflow"""
        try:
            logger.info("=" * 60)
            logger.info("Starting Facebook Automation Workflow")
            logger.info("=" * 60)
            
            # Step 1: Select persona, vibe, and day config
            persona = self.select_persona()
            vibe = self.select_vibe()
            day_config = self.get_day_config()
            callout = self.select_callout(persona)
            bible_verse = random.choice(self.bible_verses)
            
            logger.info(f"Persona: {persona.name} ({persona.gender.value})")
            logger.info(f"Vibe: {vibe.value}")
            logger.info(f"Day: {day_config.day} - {day_config.theme}")
            
            # Step 2: Fetch news
            news_headline, news_url = self.fetch_news()
            logger.info(f"News: {news_headline or 'No news fetched'}")
            
            # Step 3: Select topic
            topic = random.choice(day_config.topics)
            logger.info(f"Topic: {topic}")
            
            # Step 4: Generate image
            image_prompt = self.generate_image_prompt(day_config, topic, vibe)
            image_url = self.generate_image_url(image_prompt)
            logger.info(f"Image URL: {image_url}")
            
            # Step 5: Generate post content
            post_content = self.generate_post_content(persona, day_config, vibe, topic, news_headline)
            logger.info(f"Post content generated ({len(post_content)} chars)")
            
            # Step 6: Format post
            formatted_post = self.format_post(persona, post_content, callout)
            logger.info(f"Formatted post ({len(formatted_post)} chars)")
            
            # Step 7: Post to Facebook
            post_id = self.post_to_facebook(image_url, formatted_post)
            if not post_id:
                logger.error("Failed to post to Facebook")
                return False
            
            # Step 8: Post first comment with Bible verse
            self.post_first_comment(post_id, bible_verse)
            
            # Step 9: Log execution
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'persona': persona.name,
                'vibe': vibe.value,
                'day': day_config.day,
                'topic': topic,
                'news_headline': news_headline,
                'post_id': post_id,
                'bible_verse': bible_verse.ref,
                'status': 'success'
            }
            self.log_to_google_sheets(log_data)
            
            logger.info("=" * 60)
            logger.info("✅ Workflow completed successfully!")
            logger.info("=" * 60)
            return True
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}", exc_info=True)
            return False


if __name__ == '__main__':
    agent = FacebookAutomationAgent()
    success = agent.run()
    exit(0 if success else 1)
