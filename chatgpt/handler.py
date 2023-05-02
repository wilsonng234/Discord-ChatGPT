import json
import requests

from dotenv import dotenv_values

config = dotenv_values()
api_key = config["OPENAI_API_KEY"]
api_url = "https://chatgpt-api.shn.hk/v1"


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    response = None
    content = None
    dict = None

    try:
        req = json.loads(req)
        author = req["author"]
        messages = req["messages"]
        # Only get the last 10 messages
        conversationLog = list(
            filter(lambda message: message["author"] == author, messages)
        )[-10:]
        conversationLog = list(
            map(
                lambda message: {"role": "user", "content": message["content"]},
                conversationLog,
            )
        )

        data = json.dumps(
            {
                "model": "gpt-3.5-turbo",
                "messages": conversationLog,
            }
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        response = requests.post(api_url, data=data, headers=headers)
        content = response.content.decode("utf-8")
        dict = json.loads(content)

        return dict["choices"][0]["message"]["content"]
    except json.JSONDecodeError:
        try:
            content = content.removeprefix("OpenAI API responded:")
            dict = json.loads(content)
        except json.JSONDecodeError:
            return "Something went wrong. Please try again later."

        if dict["error"] and dict["error"]["message"]:
            return dict["error"]["message"]
        else:
            return "Something went wrong. Please try again later."
