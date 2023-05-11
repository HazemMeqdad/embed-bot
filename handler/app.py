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
import requests 
from PIL import Image
import io

int_to_hex = lambda x: '#{0:06X}'.format(x)


class App(Interactions):
    app = Flask(__name__)
    def __init__(self, client_public_key: str, application_id: str, *args, **kwargs):
        super().__init__(App.app, client_public_key, path="/interactions", app_id=application_id)

    @staticmethod
    def get_image_dimensions(url):
        try:
            response = requests.get(url)
            img_data = io.BytesIO(response.content)
            image = Image.open(img_data)
            return image.width, image.height
        except:
            return None, None

    @app.route("/<code>")
    def index(code):
        embed_data = UrlsDatabase.get_url(code)
        if not embed_data:
            return ""
        html_code = "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
        html_code += "<meta property=\"og:type\" content=\"object\">\n"

        if "title" in embed_data:
            html_code += "<meta property=\"og:title\" content=\"{}\">\n".format(embed_data["title"])
            html_code += "<meta name=\"twitter:title\" content=\"{}\">\n".format(embed_data["title"])

        if "description" in embed_data:
            html_code += "<meta property=\"og:description\" content=\"{}\">\n".format(embed_data["description"])
            html_code += "<meta name=\"twitter:description\" content=\"{}\">\n".format(embed_data["description"])

        if "color" in embed_data:
            theme_color = int_to_hex(embed_data["color"])
        else:
            theme_color = "#ffffff"

        html_code += "<meta name=\"theme-color\" content=\"{}\">\n".format(theme_color)

        if "image" in embed_data and "url" in embed_data["image"]:
            image_url = embed_data["image"]["url"]
            image_width, image_height = App.get_image_dimensions(image_url)
            html_code += "<meta property=\"og:image\" content=\"{}\">\n".format(image_url)
            if image_width and image_height:
                html_code += "<meta property=\"og:image:width\" content=\"{}\">\n".format(image_width)
                html_code += "<meta property=\"og:image:height\" content=\"{}\">\n".format(image_height)
            html_code += "<meta property=\"og:image:alt\" content=\"{}\">\n".format(embed_data.get("description", "kmcoders"))

        if "author" in embed_data and isinstance(embed_data["author"], dict) and "name" in embed_data["author"]:
            html_code += "<meta property=\"og:site_name\" content=\"{}\">\n".format(embed_data["author"]["name"])
            html_code += "<meta name=\"twitter:site\" content=\"{}\">\n".format(embed_data["author"]["name"])
        return html_code

    def run(self, *args, **kwargs):
        # App.app.run(ssl_context=context, *args, **kwargs)
        App.app.run(*args, **kwargs)
