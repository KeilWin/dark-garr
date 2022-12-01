import os


import discord
from dotenv import load_dotenv


from bot import DarkGarr
from player import Player


load_dotenv()


def create_bot(player):
    token = os.getenv("DISCORD_BOT_TOKEN")
    command_prefix = os.getenv("DISCORD_BOT_COMMAND_PREFIX")
    intents = discord.Intents.default()
    intents.message_content = True
    bot = DarkGarr(token, command_prefix, intents, player)
    return bot


def create_player():
    token = os.getenv("YANDEX_MUSIC_TOKEN")
    player = Player(token)
    return player


def main():
    player = create_player()
    bot = create_bot(player)
    bot.run()


if __name__ == "__main__":
    main()
