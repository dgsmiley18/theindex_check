import requests
import json

r = requests.get("https://theindex.moe/_next/data/WR6kC01BpbK8Nyw4ytHn_/items.json")
response = r.json()
items = response["pageProps"]["items"]

# List to store the items
list_items = []

for item in items:
    dictionary = {
        "name": item["name"],
        "url":  item["urls"][0]
    }

    list_items.append(dictionary)

# It will store all the items in a JSON file
with open("items.json", 'w') as file:
    json.dump(list_items, file, indent=4)
