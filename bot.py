import discord
import requests

from dotenv import dotenv_values

config = dotenv_values()
api_url = config.get("API_URL") + "/chatgpt"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    await message.channel.typing()

    headers = {"Content-Type": "text/plain"}
    response = requests.post(api_url, data=message.content, headers=headers)
    content = response.content.decode("utf-8")

    if content:
        await message.channel.send(content)
    else:
        await message.channel.send("Something went wrong. Please try again later.")


client.run(config["DISCORD_BOT_TOKEN"])
