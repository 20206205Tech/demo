import json
import urllib.error
import urllib.request

from env import TOKEN


def start_new_chat():
    """
    Calls the /chats/start endpoint to initialize a new chat session and obtain a chatId.
    """
    url = "https://20206205.tech/api/api-gateway/code-conversation-service/chats/start"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "sec-ch-ua-platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    req = urllib.request.Request(url, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            chat_id = data.get("data", {}).get("chatId")
            if not chat_id:
                raise ValueError(f"Could not retrieve chatId from response: {res_body}")
            return chat_id
    except urllib.error.HTTPError as e:
        print(f"HTTP Error starting chat: {e.code} - {e.reason}")
        print(e.read().decode("utf-8", errors="ignore"))
        raise
    except Exception as e:
        print(f"Error starting chat: {e}")
        raise
