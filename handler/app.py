from flask import Flask
from discord_interactions.flask_ext import Interactions
from database.client import UrlsDatabase

CODES = {
    "title": ["<title>{0}</title>", "<meta content=\"{0}\" property=\"og:title\" />"],
    "description": ["<meta content=\"{0}\" property=\"og:description\" />"],
    "url": ["<meta content=\"{0}\" property=\"og:url\" />"],
    "thumbnail": ["<meta content=\"{0}\" property=\"og:image\" />"],  # small image
    "color": ["<meta content=\"{0}\" property=\"og:color\" />"],
    "author": ["<meta content=\"{0}\" property=\"og:author\" />"],
    "image": ["<meta content=\"{0}\" name=\"twitter:card\" />"],  # large image
}

class App(Interactions):
    app = Flask(__name__)
    def __init__(self, client_public_key: str, application_id: str, *args, **kwargs):
        super().__init__(App.app, client_public_key, path="/interactions", app_id=application_id)

    @app.route("/<code>")
    def index(code):
        data = UrlsDatabase.get_url(code)
        if not data:
            return ""
        html_code = "<meta name=\"twitter:card\" content=\"summary\">\n"
        for key, value in data.items():
            if key not in CODES.keys():
                continue
            if key == "thumbnail":
                html_code += CODES[key][0].format(value["url"].replace("\"", "\\\"")) + "\n"
            elif key == "image":
                html_code += CODES[key][0].format(value["url"].replace("\"", "\\\"")) + "\n"
            elif key == "author":
                html_code += CODES[key][0].format(value["name"].replace("\"", "\\\"")) + "\n"
            else:
                html_code += CODES[key][0].format(value.replace("\"", "\\\"") if isinstance(value, str) else value) + "\n"
        return html_code

    def run(self, *args, **kwargs):
        App.app.run(*args, **kwargs)