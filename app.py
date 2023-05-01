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
from utlits import compiler_json_data
from database.client import UrlsDatabase
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

interactions = App(os.environ['CLIENT_PUBLIC_KEY'], os.environ['APPLICATION_ID'], debug=True)

@interactions.command
def ping(cmd: commands.Ping):
    return "Pong!"

@interactions.command(commands.Source)
def source(ctx: Context):
    return "https://github.com/HazemMeqdad/embed-bot", True

random_code = lambda: "".join(random.choices(string.ascii_letters + string.digits, k=6))

@interactions.command(commands.Create)
def create(ctx: Context):
    ...

def create_embed(data: str, code: str):
    code = code if code else random_code()
    if not data:
        return "Please give me a data, use this site https://discohook.org/ to make a embed data\nCopy only one embed Just"
    clean_code = compiler_json_data(data)
    if clean_code is False:
        return "This data is not a json Or wrong embed data"
    if UrlsDatabase.get_url(code):
        return "This url already exists"
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
    return create_embed(data, code)

# Register message command
interactions._commands["Make Embed"] = CommandData(
    name="Make Embed",
    cb=make_embed_context_menu,
    cmd=ApplicationCommand(
        name="Make Embed", 
        description=None, 
        type=ApplicationCommandType.MESSAGE.value
    )
)

if __name__ == "__main__":
    interactions.run("0.0.0.0", os.getenv("PORT", 80))
