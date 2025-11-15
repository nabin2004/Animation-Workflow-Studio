import requests

url = "http://localhost:6277/mcp/run"  # endpoint MCP expects

payload = {
    "sessionId": "test-session",
    "tool": "greet_user",
    "args": {"name": "Nabin", "style": "funny"}
}

response = requests.post(url, json=payload)
print(response.json())