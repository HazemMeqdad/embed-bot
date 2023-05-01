from discord_interactions.ocm import Command, Option, OptionChoices, SubCommand
from discord_interactions import ApplicationCommandOptionType

class Ping(Command):
    """ simple ping command just send pong! """

class CreateEmbed(SubCommand):
    """ create a embed url it host on bot server """
    name = "embed"
    data: str = Option("Enter json data", type=ApplicationCommandOptionType.STRING)
    code: bool = Option("If you want to add custom code", type=ApplicationCommandOptionType.STRING, required=False)

class Create(Command):
    """ Embed command """
    embed: str = CreateEmbed()

class Help(Command):
    """Show all commands and sub commands bot used it"""

class Source(Command):
    """Show the bot source code"""

class Invite(Command):
    """Show the bot invite link"""

