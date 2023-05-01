import json
import typing as t

class UrlsDatabase:
    @staticmethod
    def push_url(data: dict, url: str) -> None:
        with open("./database/urls.json", "r") as f:
            embed = json.load(f)
        embed[url] = data
        with open("./database/urls.json", "w") as f:
            json.dump(embed, f, indent=4)

    @staticmethod
    def get_url(url: str) -> t.Optional[dict]:
        with open("./database/urls.json", "r") as f:
            embed = json.load(f)
        return embed.get(url, None)

    @staticmethod
    def edit_url(url: str, data: dict) -> None:
        with open("./database/urls.json", "r") as f:
            embed = json.load(f)
        embed[url] = data
        with open("./database/urls.json", "w") as f:
            json.dump(embed, f, indent=4)

    @staticmethod
    def delete_url(url: str) -> None:
        with open("./database/urls.json", "r") as f:
            embed = json.load(f)
        del embed[url]
        with open("./database/urls.json", "w") as f:
            json.dump(embed, f, indent=4)

    @staticmethod
    def get_all_urls() -> dict:
        with open("./database/urls.json", "r") as f:
            embed = json.load(f)
        return embed
    
