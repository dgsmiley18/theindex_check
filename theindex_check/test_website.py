import requests


def brokensite():
    urls_index = ["anime", "hentai", "manga"]
    for library in enumerate(urls_index):
        # Start reading all the links from the file
        with open(f"{library}.txt", "r") as reader:
            for website in reader.readlines():
                r = requests.get(f"http://{website}".strip())

                with open(f"{library}_tested.txt", "w") as writer:
                    if r.status_code == 200:
                        writer.write(f"{website} = Working")
                    else:
                        writer.write(
                            f"{website} = Not Working (status code = {r.status_code}"
                        )

brokensite()
