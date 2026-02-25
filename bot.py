import discord
from discord.ext import commands
from discord.ext import tasks
import datetime
import os
from flask import Flask
from threading import Thread

# ---- KEEP ALIVE WEB SERVER ----
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ---- DISCORD BOT SETUP ----
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
# ---- CHANNEL IDS ----
LATEST_JOBS_CHANNEL = 1476042365281112307
EXAM_CHANNEL = 1476042397287710861
RESULTS_CHANNEL = 1476042428593995831
INTERNSHIP_CHANNEL = 1476042458792988874

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    scheduled_posts.start()

@tasks.loop(minutes=1)
async def scheduled_posts():
    now = datetime.datetime.utcnow()

    # 9:00 AM IST (3:30 UTC)
    if now.hour == 3 and now.minute == 30:
        channel = bot.get_channel(LATEST_JOBS_CHANNEL)
        if channel:
            await channel.send("🇮🇳 Good Morning! Check 🏛️ latest-jobs for fresh government notifications.")

    # 12:00 PM IST (6:30 UTC)
    if now.hour == 6 and now.minute == 30:
        channel = bot.get_channel(EXAM_CHANNEL)
        if channel:
            await channel.send("📝 Midday Update! Stay updated with latest exam notifications.")

    # 6:00 PM IST (12:30 UTC)
    if now.hour == 12 and now.minute == 30:
        channel = bot.get_channel(RESULTS_CHANNEL)
        if channel:
            await channel.send("📊 Evening Results Check! New results may have been published today.")

    # 8:00 PM IST (14:30 UTC)
    if now.hour == 14 and now.minute == 30:
        channel = bot.get_channel(INTERNSHIP_CHANNEL)
        if channel:
            await channel.send("🎓 Night Update! Explore new internship opportunities.")

# ---- START BOT ----
keep_alive()

bot.run(TOKEN)
