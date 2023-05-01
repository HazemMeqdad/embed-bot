from flask import Flask
from discord_interactions.flask_ext import Interactions
from database.client import UrlsDatabase

CODES = {
    "title": "<meta content=\"{0}\" property=\"og:title\" />",
    "image": "<meta content=\"{0}\" property=\"og:image\" />",  # small image
    "url": "<meta content=\"{0}\" property=\"og:url\" />",
    "description": "<meta content=\"{0}\" property=\"og:description\" />",
    "author": "<meta content=\"{0}\" property=\"og:site_name\" />",

    "color": "<meta content=\"{0}\" name=\"theme-color\" />",
}

int_to_hex = lambda x: '#{0:06X}'.format(x)

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
        html_code += "<meta property=\"og:type\" content=\"website\">"
        for key, value in data.items():
            if key not in CODES.keys():
                continue
            if key == "thumbnail":
                html_code += CODES[key].format(value["url"].replace("\"", "\\\"")) + "\n"
            elif key == "image":
                html_code += CODES[key].format(value["url"].replace("\"", "\\\"")) + "\n"
            elif key == "author":
                html_code += CODES[key].format(value["name"].replace("\"", "\\\"")) + "\n"
            elif key == "color":
                html_code += CODES[key].format(int_to_hex(value))+ "\n"
            else:
                html_code += CODES[key].format(value.replace("\"", "\\\"") if isinstance(value, str) else value) + "\n"
        return html_code

    def run(self, *args, **kwargs):
        App.app.run(*args, **kwargs)