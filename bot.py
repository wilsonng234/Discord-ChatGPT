import json
import discord
import requests

from dotenv import dotenv_values

config = dotenv_values()
api_url = config.get("API_URL") + "/chatgpt"
discord_bot_id = config["DISCORD_BOT_ID"]
discord_bot_token = config["DISCORD_BOT_TOKEN"]

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)


async def handle_chatgpt(message):
    async def fetch_messages(message, n):
        return [
            {"author_id": msg.author.id, "content": msg.content}
            async for msg in message.channel.history(limit=n)
        ]

    if (
        message.author.bot
        or not message.type == discord.MessageType.default
        or not message.content.startswith("!chat")
    ):
        return

    await message.channel.typing()

    messages = await fetch_messages(message, 100)
    messages.reverse()
    data = json.dumps(
        {
            "user_id": message.author.id,
            "chatgpt_bot_id": discord_bot_id,
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


@client.event
async def on_message(message):
    if message.author != client.user:
        await handle_chatgpt(message)


client.run(discord_bot_token)
