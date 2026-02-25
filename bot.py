import discord
from discord.ext import commands, tasks
import os
from flask import Flask
from threading import Thread
import requests
from bs4 import BeautifulSoup
import json

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
CHANNEL_ID = 1476042365281112307  # SSC Job Channel

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- LOAD POSTED JOBS ----
def load_posted_jobs():
    try:
        with open("posted_jobs.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_posted_jobs(jobs):
    with open("posted_jobs.json", "w") as f:
        json.dump(jobs, f)

# ---- FETCH SSC JOBS ----
def fetch_ssc_jobs():
    url = "https://ssc.nic.in/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Find notice links (this may need adjustment later)
    for link in soup.find_all("a"):
        text = link.get_text(strip=True)
        href = link.get("href")

        if text and href and "Notice" in text:
            full_link = href if href.startswith("http") else "https://ssc.nic.in/" + href
            jobs.append({
                "title": text,
                "link": full_link
            })

    return jobs[:5]  # Limit to latest 5

# ---- TASK LOOP ----
@tasks.loop(minutes=30)
async def ssc_job_task():
    print("Checking SSC jobs...")

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found!")
        return

    posted_jobs = load_posted_jobs()
    jobs = fetch_ssc_jobs()

    for job in jobs:
        if job["link"] not in posted_jobs:
            embed = discord.Embed(
                title="📢 New SSC Notification",
                description=f"**{job['title']}**",
                color=0x2ecc71
            )
            embed.add_field(name="Apply Here", value=job["link"], inline=False)
            embed.set_footer(text="Staff Selection Commission Updates")

            await channel.send(embed=embed)

            posted_jobs.append(job["link"])
            save_posted_jobs(posted_jobs)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    ssc_job_task.start()

# ---- START BOT ----
keep_alive()
bot.run(TOKEN)
