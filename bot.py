from dotenv import dotenv_values

config = dotenv_values()
api_url = config.get("API_URL")
discord_bot_id = config["DISCORD_BOT_ID"]
discord_bot_token = config["DISCORD_BOT_TOKEN"]
openai_api_key = config["OPENAI_API_KEY"]

import json
import discord
import requests
from io import BytesIO

from discord import app_commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def handle_chatgpt(message):
    async def fetch_messages(message, n):
        return [
            {"author_id": msg.author.id, "content": msg.content}
            async for msg in message.channel.history(limit=n)
        ]

    if (
        message.author.bot
        or not message.type == discord.MessageType.default
        or (
            not message.channel.name == "chatgpt"
            and not message.content.startswith("!chat")
        )
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
            "channel": message.channel.name,
        }
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }

    try:
        response = requests.post(api_url + "/chatgpt", data=data, headers=headers)
        content = response.content.decode("utf-8")
        content = json.loads(content)

        if content.get("response") is not None:
            await message.channel.send(content.get("response"))
        elif content.get("error") is not None:
            await message.channel.send("Error:\n" + content.get("error"))
        else:
            await message.channel.send("Something went wrong. Please try again later.")
    except Exception as e:
        await message.channel.send("Error:\n" + str(e))


@tree.command(name="image", description="Generate image with DALL·E 2a")
async def image(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)

    data = json.dumps({"prompt": prompt})
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }

    try:
        response = requests.post(api_url + "/dalle2", data=data, headers=headers)
        content = response.content.decode("utf-8")
        content = json.loads(content)

        if content.get("response") is not None:
            image_url = content.get("response")
            image_data = requests.get(image_url).content
            image_file = BytesIO(image_data)
            picture = discord.File(image_file, filename="image.png")

            await interaction.followup.send(file=picture)
        elif content.get("error") is not None:
            await interaction.followup.send("Error:\n" + content.get("error"))
        else:
            await interaction.followup.send(
                "Something went wrong. Please try again later."
            )
    except Exception as e:
        await interaction.followup.send("Error:\n" + str(e))


@client.event
async def on_message(message):
    if message.author != client.user:
        await handle_chatgpt(message)


@client.event
async def on_ready():
    synced = await tree.sync()
    print(f"Synced {len(synced)} commands!")


client.run(discord_bot_token)
