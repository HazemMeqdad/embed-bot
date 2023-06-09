import discord_interactions
from discord_interactions import ApplicationClient
import os

from app import interactions


if __name__ == "__main__":
    client = ApplicationClient(os.getenv("TOKEN"), os.getenv("APPLICATION_ID"))
    # IF YOU WANNA TO REMOVE ALL COMMANDS
    # commands = client.get_commands()
    # for command in commands:
    #     client.delete_command(command.id)

    # You might specify a guild here.
    # Global commands can take up to one hour to be available after registration.
    client.bulk_overwrite_commands(interactions.commands)