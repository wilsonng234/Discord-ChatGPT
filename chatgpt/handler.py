import json
import openai

from dotenv import dotenv_values

config = dotenv_values()
api_url = "https://chatgpt-api.shn.hk/v1"
openai_api_key = config["OPENAI_API_KEY"]


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    try:
        req = json.loads(req)
        user_id = req["user_id"]
        chatgpt_bot_id = req["chatgpt_bot_id"]
        messages = req["messages"]

        conversationLog = []
        count = 0
        for msg in messages[::-1]:
            # Only get the last 20 messages
            if count == 20:
                break

            if str(msg["author_id"]) == str(chatgpt_bot_id):
                conversationLog.append({"role": "assistant", "content": msg["content"]})
                count += 1

            elif not msg["content"].startswith("!chat"):
                pass

            elif str(msg["author_id"]) == str(user_id):
                conversationLog.append(
                    {"role": "user", "content": msg["content"].removeprefix("!chat")}
                )
                count += 1

        conversationLog.reverse()

        openai.api_key = openai_api_key
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversationLog,
        )

        return completion.choices[0].message.content
    except Exception as e:
        return e
