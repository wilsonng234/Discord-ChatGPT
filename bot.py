import json
import discord
import requests

from dotenv import dotenv_values

config = dotenv_values()
api_url = config.get("API_URL") + "/chatgpt"
discord_bot_token = config["DISCORD_BOT_TOKEN"]

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)


async def fetch_messages(message, n):
    return [
        {"author": msg.author.id, "content": msg.content}
        async for msg in message.channel.history(limit=n)
    ]


@client.event
async def on_message(message):
    if message.author.bot:
        return

    await message.channel.typing()

    messages = await fetch_messages(message, 100)
    messages.reverse()
    data = json.dumps(
        {
            "author": message.author.id,
            "messages": messages,
        }
    )

    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, data=data, headers=headers)
    content = response.content.decode("utf-8")

    if content:
        await message.channel.send(content)
    else:
        await message.channel.send("Something went wrong. Please try again later.")


client.run(discord_bot_token)
