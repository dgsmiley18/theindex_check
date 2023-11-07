import requests


def brokensite():
    urls_index = ["anime", "hentai", "manga"]
    working = 0
    not_working = 0
    for index, library in enumerate(urls_index):
        # Start reading all the links from the file
        with open(f"{library}.txt", "r") as reader:
            for line in reader.readlines():
                r = requests.get(f"http://{line}".strip())
                with open(f"{library}_tested.txt", "w") as writer:
                    if r.status_code == 200:
                        writer.write(f"{line} = Working")
                        working += 1
                    else:
                        writer.write(f"{line} = Not Working (status code = {r.status_code}")
                        not_working += 1
                        

brokensite()
