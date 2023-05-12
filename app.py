import os
from handler import App, Embed
import commands
import string 
import random
from discord_interactions.flask_ext import CommandContext as Context
from discord_interactions.flask_ext import CommandData
from discord_interactions import (
    InteractionResponse, 
    InteractionApplicationCommandCallbackData, 
    InteractionCallbackType,
    ApplicationCommandType,
    ApplicationCommand
)
from utlits import compiler_json_data, video_compiler_json
from database.client import UrlsDatabase
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass
import requests
from bs4 import BeautifulSoup
import re
import json
interactions = App(os.environ['PUBLIC_KEY'], os.environ['APPLICATION_ID'], debug=True, token=os.environ['TOKEN'])

@interactions.command
def ping(cmd: commands.Ping):
    return "Pong!"

@interactions.command(commands.Source)
def source(ctx: Context):
    return "https://github.com/HazemMeqdad/embed-bot", True

@interactions.command(commands.Invite)
def invite(ctx: Context):
    return f"https://discord.com/api/oauth2/authorize?client_id={interactions._app_id}&permissions=49152&scope=bot%20applications.commands", True

random_code = lambda: "".join(random.choices(string.ascii_letters + string.digits, k=6))

@interactions.command(commands.Create)
def create(ctx: Context):
    ...

def create_embed(data: str, code: str):
    code = code if code else random_code()
    if not data:
        return "**Please provide a valid JSON data or use the website \"https://discohook.org/\" to generate a single embed.**"
    clean_code = compiler_json_data(data)
    if clean_code is False:
        return "**Invalid JSON data or incorrect embedded JSON format detected**"
    if UrlsDatabase.get_url(code):
        return "**This url with code || {} || already exists**".format(code)
    UrlsDatabase.push_url(clean_code, code)
    return os.getenv("HOST") + code

def create_video_embed_data(data: str, code: str):
    code = code if code else random_code()
    if not data:
        return "**Please provide a valid JSON data with this keys.**\n **[\'`title`\', \'`description`\', \'`video`\', \'`width`\', \'`height`\' \'`image`\']**"
    clean_code = video_compiler_json(data)
    if clean_code is False:
        return "**Invalid JSON data or incorrect embedded JSON format detected use this keys to make a vaild data**\n **[\'`title`\', \'`description`\', \'`video`\', \'`width`\', \'`height`\' \'`image`\']**"
    if UrlsDatabase.get_url(code):
        return "**This url with code || {} || already exists**".format(code)
    UrlsDatabase.push_url(clean_code, code)
    return os.getenv("HOST") + code

@create.subcommand()
def embed(ctx: Context, cmd: commands.CreateEmbed):
    code = cmd.code
    data = cmd.data
    return create_embed(data, code)


@create.fallback
def create_fallback(_: Context):
    return "Please select a sub command"

@interactions.command(commands.Help)
def help(ctx: Context):
    cmds = interactions.commands
    embed = Embed(title="Help command", description="This is a help command for this bot\n\n")
    # Help command with sub commands and metion the code with id
    for cmd in cmds:
        if cmd.type != ApplicationCommandType.CHAT_INPUT:
            continue 
        # Sub commands
        if cmd.options and 1 in [i.type.value for i in cmd.options]:
            for sub_cmd in cmd.options:
                embed.description += f"**/{cmd.name} {sub_cmd.name}** -  {sub_cmd.description}\n"
        # Normal commands
        else:
            embed.description += f"**/{cmd.name}** - {cmd.description}\n"
    return InteractionResponse(
        type=InteractionCallbackType.CHANNEL_MESSAGE,
        data=InteractionApplicationCommandCallbackData(
            embeds=[embed]
        ),
    )


def make_embed_context_menu(ctx: Context):
    code = random_code()
    data = list(ctx.interaction.data.resolved.messages.values())[0].content
    return 

def create_video_embed(ctx: Context):
    code = random_code()
    data = list(ctx.interaction.data.resolved.messages.values())[0].content
    return create_video_embed_data(data=data, code=code)

def get_embed_context_menu(ctx: Context):
    print("Start")
    message = list(ctx.interaction.data.resolved.messages.values())[0].content
    if not message:
        return "No message content"
    url_pattern = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\)])+(?<![),]))"
    urls = re.findall(url_pattern, message)
    embed_list = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                title_tag = soup.find("meta", property="og:title")
                title = title_tag["content"] if title_tag else None

                image_tag = soup.find("meta", property="og:image")
                image = image_tag["content"] if image_tag else None

                url_tag = soup.find("meta", property="og:url")
                url_ = url_tag["content"] if url_tag else None

                description_tag = soup.find("meta", property="og:description")
                description = description_tag["content"] if description_tag else None

                author_tag = soup.find("meta", property="og:site_name")
                author = author_tag["content"] if author_tag else None

                color_tag = soup.find("meta", property="theme-color")
                print(color_tag)
                color = color_tag["content"] if color_tag else 0

                if title or image or url_ or description or author or color:
                    embed_data = {
                        "title": title,
                        "url": url_,
                        "description": description,
                        "author": {
                            "name": author
                        },
                        "color": color,
                        "image": {
                            "url": image
                        }
                    }
                    embed_list.append(embed_data)
        except (requests.RequestException, KeyError):
            print(f"Error occurred while fetching embed information for {url}")

    if embed_list:
        json_data = json.dumps(embed_list, indent=4) #Make it easy to Read 
        code_block = "```json\n" + json_data + "\n```"
        return code_block
    else:
        return "**No embeds found in the provided in the message URLs.**"

# Register message command
interactions._commands["Make Embed"] = CommandData(
    name="Create a discord embed",
    cb=make_embed_context_menu,
    cmd=ApplicationCommand(
        name="Create a discord embed", 
        description=None, 
        type=ApplicationCommandType.MESSAGE.value
    )
)
interactions._commands["Get Embed"] = CommandData(
    name="Get a discord embed",
    cb=get_embed_context_menu,
    cmd=ApplicationCommand(
        name="Get a discord embed", 
        description=None, 
        type=ApplicationCommandType.MESSAGE.value
    )
)
interactions._commands["Create a video embed"] = CommandData(
    name="Create a video embed",
    cb=create_video_embed,
    cmd=ApplicationCommand(
        name="Create a video embed", 
        description=None, 
        type=ApplicationCommandType.MESSAGE.value
    )
)
if __name__ == "__main__":
    interactions.run("0.0.0.0", os.getenv("PORT", 80))
