import discord
from discord.ext import commands
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

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# ---- START BOT ----
keep_alive()
bot.run(TOKEN)