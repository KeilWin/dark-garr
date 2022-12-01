import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from typing import Optional


class DarkGarr:
    _bot: commands.Bot
    _token: str

    def __init__(self, token: str, command_prefix: str, intents: discord.Intents, player):
        self._token = token
        self._player = player
        self._bot = commands.Bot(command_prefix=command_prefix, intents=intents)
        self.init_handlers()

    def init_handlers(self):
        @self._bot.command()
        async def hello(ctx: commands.Context):
            await ctx.reply("Нет")

        @self._bot.command()
        async def play(ctx: commands.Context, *args):
            if ctx.author.voice:
                channel = ctx.author.voice.channel

                search = self._player.search_track(' '.join(args))
                if search:
                    if ctx.voice_client and ctx.voice_client.channel == ctx.author.voice.channel:
                        voice = ctx.voice_client
                    else:
                        voice = await channel.connect()
                    source = FFmpegPCMAudio('music/track.mp3')
                    player = voice.play(source)
                else:
                    await ctx.reply('Трек не найден')
            else:
                await ctx.reply('Канал не обнаружен')

        @self._bot.command()
        async def pause(ctx: commands.Context):
            if ctx.author.voice:
                voice = discord.utils.get(self._bot.voice_clients, guild=ctx.guild)
                if voice:
                    if voice.is_playing():
                        voice.pause()
                    else:
                        await ctx.reply('Нечего')
                else:
                    await ctx.reply('Не играет')
            else:
                await ctx.reply('Канал не обнаружен')

        @self._bot.command()
        async def resume(ctx: commands.Context):
            if ctx.author.voice:
                voice = discord.utils.get(self._bot.voice_clients, guild=ctx.guild)
                if voice:
                    if voice.is_paused():
                        voice.resume()
                    else:
                        await ctx.reply('Нечего')
                else:
                    await ctx.reply('Не играет')
            else:
                await ctx.reply('Канал не обнаружен')

        @self._bot.command()
        async def stop(ctx: commands.Context):
            if ctx.author.voice:
                voice = discord.utils.get(self._bot.voice_clients, guild=ctx.guild)
                if voice:
                    voice.stop()
                else:
                    await ctx.reply('Не играет')
            else:
                await ctx.reply('Канал не обнаружен')

    def run(self):
        self._bot.run(self._token)
