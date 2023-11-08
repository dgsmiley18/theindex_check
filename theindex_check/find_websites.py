import requests
import json


r = requests.get(f"https://theindex.moe/_next/data/WR6kC01BpbK8Nyw4ytHn_/items.json")
response = r.json()
items = response["pageProps"]["items"]
for item in items:
    print(item["name"])
    print(item["urls"][0])