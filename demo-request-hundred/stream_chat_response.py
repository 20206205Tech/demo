import json
import urllib.error
import urllib.request

from env import TOKEN


def stream_chat_response(chat_id, query):
    """
    Sends the query to the /chats/stream endpoint and parses the SSE stream.
    Returns: (full_answer, sources)
    """
    url = "https://20206205.tech/api/api-gateway/code-conversation-service/chats/stream"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "sec-ch-ua-platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    payload = {
        "chat_id": chat_id,
        "query": query,
        "file_ids": [],
        "use_reasoning": True,
    }

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST"
    )

    content_parts = []
    full_answer = None
    sources = []

    try:
        with urllib.request.urlopen(req) as response:
            buffer = ""
            for chunk in response:
                buffer += chunk.decode("utf-8", errors="ignore")
                while "\n\n" in buffer:
                    block, buffer = buffer.split("\n\n", 1)
                    for line in block.split("\n"):
                        line = line.strip()
                        if line.startswith("data:"):
                            data_str = line[5:].strip()
                            try:
                                event = json.loads(data_str)
                                event_type = event.get("type")

                                if event_type == "content":
                                    content_parts.append(event.get("message", ""))
                                elif event_type == "metadata":
                                    msg_data = event.get("message", {})
                                    full_answer = msg_data.get("full_answer")
                                    sources = msg_data.get("sources", [])
                            except json.JSONDecodeError:
                                pass
    except urllib.error.HTTPError as e:
        print(f"HTTP Error in streaming response: {e.code} - {e.reason}")
        print(e.read().decode("utf-8", errors="ignore"))
        raise
    except Exception as e:
        print(f"Error during streaming: {e}")
        raise

    if not full_answer:
        full_answer = "".join(content_parts)

    return full_answer, sources
