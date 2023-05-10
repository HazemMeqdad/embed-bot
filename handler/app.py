from flask import Flask
from discord_interactions.flask_ext import Interactions
from database.client import UrlsDatabase
## uncomment this if you wanna use your own ssl made by certbot 
## if you wanna to generate one use this command in your ubuntu server
## sudo certbot certonly --standalone -d kmcoders.com 
## replace kmcoders with your own domain 
# import ssl
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('/etc/letsencrypt/live/kmcoders.com-0001/fullchain.pem', '/etc/letsencrypt/live/kmcoders.com-0001/privkey.pem')
import json
# i try to use all otg meta code i stil work on it 
CODES = {
    "title": "<meta content=\"{0}\" property=\"og:title\" />",
    "image": "<meta content=\"{0}\" property=\"og:image\" />",  # small image
    "thumbnail": "<meta content=\"{0}\" property=\"og:image\" />",
    "url": "<meta content=\"{0}\" property=\"og:url\" />",
    "description": "<meta content=\"{0}\" property=\"og:description\" />",
    "author": "<meta content=\"{0}\" property=\"og:site_name\" />",
    "color": "<meta content=\"{0}\" name=\"theme-color\" />",
    "site": "<meta content=\"{0}\" property=\"og:site\" />",
    "type": "<meta content=\"{0}\" property=\"og:type\" />",
    "audio": "<meta content=\"{0}\" property=\"og:audio\" />",
    "video": "<meta content=\"{0}\" property=\"og:video\" />",
    "locale": "<meta content=\"{0}\" property=\"og:locale\" />",
    "locale:alternate": "<meta content=\"{0}\" property=\"og:locale:alternate\" />",
    "restrictions:age": "<meta content=\"{0}\" property=\"og:restrictions:age\" />",
    "restrictions:age:allowed": "<meta content=\"{0}\" property=\"og:restrictions:age:allowed\" />",
    "restrictions:age:content": "<meta content=\"{0}\" property=\"og:restrictions:age:content\" />",
    "see_also": "<meta content=\"{0}\" property=\"og:see_also\" />",
    "determiner": "<meta content=\"{0}\" property=\"og:determiner\" />",
    "availability": "<meta content=\"{0}\" property=\"og:availability\" />",
    "tag": "<meta content=\"{0}\" property=\"og:tag\" />",
}

int_to_hex = lambda x: '#{0:06X}'.format(x)


class App(Interactions):
    app = Flask(__name__)
    def __init__(self, client_public_key: str, application_id: str, *args, **kwargs):
        super().__init__(App.app, client_public_key, path="/interactions", app_id=application_id)

    # a bettter OGP Meta code builder 
    @app.route("/<code>")
    def index(code):
        data = UrlsDatabase.get_url(code)
        if not data:
            return ""
        html_code = "<meta name=\"twitter:card\" content=\"summary\">\n"
        html_code += "<meta property=\"og:type\" content=\"website\">\n"
        for key, value in data.items():
            if key not in CODES.keys():
                continue
            if key == "thumbnail" or key == "image":
                if isinstance(value, dict) and "url" in value:
                    html_code += CODES[key].format(value["url"].replace("\"", "\\\"")) + "\n"
            elif key == "author":
                if isinstance(value, dict) and "name" in value:
                    html_code += CODES[key].format(value["name"].replace("\"", "\\\"")) + "\n"
            elif key == "color":
                if isinstance(value, int):
                    html_code += CODES[key].format(int_to_hex(value)) + "\n"
            else:
                if isinstance(value, str):
                    html_code += CODES[key].format(value.replace("\"", "\\\"")) + "\n"
                else:
                    html_code += CODES[key].format(value) + "\n"
        return html_code

    def run(self, *args, **kwargs):
        # App.app.run(ssl_context=context, *args, **kwargs)
        App.app.run(*args, **kwargs)
