import discord
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:3002/chat")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)

def query_backend(user_message):
    """Send the user's query to our FastAPI backend and return the AI response."""
    payload = {"userMessage": user_message}
    
    try:
        response = requests.post(BACKEND_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("botMessage", "Error: No response from AI.")
    except requests.RequestException as e:
        print(f"Error communicating with backend: {e}")
        return "Error: Unable to fetch response from AI."

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        query = message.content.replace(f"<@{client.user.id}>", "").strip()

        if not query:
            await message.channel.send("You mentioned me, but didn't ask a question. Please provide a question!")
            return

        response = query_backend(query)
        print(f"Bot response: '{response}'")

        await message.channel.send(response)

client.run(DISCORD_TOKEN)
