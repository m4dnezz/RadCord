import os
import discord
from arrapi import RadarrAPI
from channel_ids import logg
import sys

API_KEY = os.getenv("RADARR_API")
RADARR_URL = os.getenv("RADARR_URL")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not API_KEY:
    raise ValueError("API key not found. Please make sure to set RADARR_API envoirment variable")

if not RADARR_URL:
    raise ValueError("API key not found. Please make sure to set RADARR_URL envoirment variable")

if not DISCORD_TOKEN:
    raise ValueError("API key not found. Please make sure to set DISCORD_TOKEN envoirment variable")

if not sys.version.startswith("3.11.9") and sys.platform == 'win32':
    print("This bot was made for python 3.11.9, and win32")
    print("Compatability for other versions and platforms are not guaranteed")
    input("Press anything to continue...")

# Make use of the very nice API wrapper by @meisnate12
radarr = RadarrAPI(RADARR_URL, API_KEY)
radarr.respect_list_exclusions_when_adding()

# initialize bot
intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    global channel
    channel = client.get_channel(logg)
    # await channel.send("RadCord is Live!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content

    if content == "!movies":
        await channel.send("Movies huh,  Alright hold on...?")
        try:
            movies = radarr.all_movies()
            for i in range(0, len(movies), 20):
                Moviebatch = movies[i:i+20]
                MovieTitles = [movie.title + "\n" for movie in Moviebatch]
                movie_titles_str = "".join(MovieTitles)
                await message.channel.send(movie_titles_str)
        except Exception as e:
            print(f"Could not retrieve movies from radarr: {e}")

    if content == "!ping":
        response = os.system("ping -n 1 " + "google.com")
        if response == 0:
            await message.channel.send("RadCord is up and running")
        else:
            await message.channel.send("RadCord is dying, slowly...")


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
