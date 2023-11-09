import requests
import json

def brokensite():
    
    with open('items.json', 'r') as file:
        data = json.load(file)
        for website in data:
            print(website["url"])
            try:
                r = requests.get(website['url'])
            except requests.exceptions.ConnectionError as err:
                print(f"Connection error occurred: {err}")
                continue
            except requests.exceptions.RequestException as err:
                print(f"Other error occurred: {err}")
                continue

            with open('websites_working.txt', 'a') as writer:
                    if r.status_code == 200:
                        writer.write(f"{website['url']} = Working\n")
                    elif r.status_code == 403:
                        writer.write(f"{website['url']} = Forbidden (status code = {r.status_code})\n")
                    else:
                        writer.write(f"{website['url']} = Not Working (status code = {r.status_code})\n")

brokensite()
