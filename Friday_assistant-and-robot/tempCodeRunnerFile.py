import requests

url = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "query",
    "list": "search",
    "srsearch": "France",
    "format": "json"
}

r = requests.get(url, params=params)

print(r.status_code)
print(r.headers.get("Content-Type"))
print(r.text[:500])