import json
import requests

from dotenv import dotenv_values

config = dotenv_values()


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    response = None
    content = None
    dict = None
    try:
        api_key = config["OPENAI_API_KEY"]
        api_url = "https://chatgpt-api.shn.hk/v1"
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": req}],
        }
        data = json.dumps(data)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        response = requests.post(api_url, data=data, headers=headers)
        content = response.content.decode("utf-8")
        dict = json.loads(content)

        return dict["choices"][0]["message"]["content"]
    except json.JSONDecodeError:
        content = content.removeprefix("OpenAI API responded:")
        dict = json.loads(content)

        if dict["error"] and dict["error"]["message"]:
            return dict["error"]["message"]
        else:
            return "Something went wrong. Please try again later."
