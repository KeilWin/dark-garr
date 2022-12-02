import asyncio
import threading

import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
from typing import Optional


from .errors import (AudioAlreadyPauseError, AudioNoTrackError, AudioAlreadyPlayError,
                     ChannelBusyError, ChannelNoVoiceError,
                     CommandSyntaxError, CommandLeaveError)
from .answers import messages

from player.errors import SearchNoFindError
from player import Player


class DarkGarr:
    _bot: commands.Bot
    _token: str
    _player: Player

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
            try:
                if ctx.author.voice is None:
                    raise ChannelNoVoiceError()
                if len(args) == 0:
                    raise CommandSyntaxError()
                track = self._player.search_track(' '.join(args))[:10][0]
                self._player.download_track(track)
                if ctx.voice_client and ctx.voice_client.channel == ctx.author.voice.channel:
                    voice = ctx.voice_client
                else:
                    voice = await ctx.author.voice.channel.connect()
                source = FFmpegPCMAudio('music/track.mp3')
                await ctx.reply(messages['player']['track_template'].format(
                    artists=' '.join([artist.name for artist in track.artists]),
                    title=track.title,
                    duration=f'{int(track.duration_ms / 60000)}:{int(track.duration_ms % 60000) // 1000}'
                ))
                if voice.is_playing():
                    voice.stop()
                player = voice.play(source)
            except ChannelNoVoiceError:
                await ctx.reply(messages['discord']['no_voice_channel'])
            except CommandSyntaxError:
                await ctx.reply(messages['command']['invalid_command_use'])
            except SearchNoFindError:
                await ctx.reply(messages['player']['no_track'])
            except:
                await ctx.reply(messages['discord']['unknown'])
                raise

        @self._bot.command()
        async def pause(ctx: commands.Context):
            try:
                if ctx.author.voice is None:
                    raise ChannelNoVoiceError()
                voice = discord.utils.get(self._bot.voice_clients, guild=ctx.guild)
                if voice is None:
                    raise AudioNoTrackError()
                if voice.is_paused():
                    raise AudioAlreadyPauseError()
                if not voice.is_playing():
                    raise AudioNoTrackError()
                voice.pause()
            except ChannelNoVoiceError:
                await ctx.reply(messages['discord']['no_voice_channel'])
            except AudioNoTrackError:
                await ctx.reply(messages['discord']['no_active'])
            except AudioAlreadyPauseError:
                await ctx.reply(messages['discord']['already_pause'])
            except:
                await ctx.reply(messages['discord']['unknown'])
                raise

        @self._bot.command()
        async def resume(ctx: commands.Context):
            try:
                if ctx.author.voice is None:
                    raise ChannelNoVoiceError()
                voice = discord.utils.get(self._bot.voice_clients, guild=ctx.guild)
                if voice is None:
                    raise AudioNoTrackError()
                if voice.is_playing():
                    raise AudioAlreadyPlayError()
                if not voice.is_paused():
                    raise AudioNoTrackError()
                voice.resume()
            except ChannelNoVoiceError:
                await ctx.reply(messages['discord']['no_voice_channel'])
            except AudioNoTrackError:
                await ctx.reply(messages['discord']['no_active'])
            except AudioAlreadyPlayError:
                await ctx.reply(messages['discord']['already_play'])
            except:
                await ctx.reply(messages['discord']['unknown'])
                raise

        @self._bot.command()
        async def stop(ctx: commands.Context):
            try:
                if ctx.author.voice is None:
                    raise ChannelNoVoiceError()
                voice = discord.utils.get(self._bot.voice_clients, guild=ctx.guild)
                if voice is None:
                    raise AudioNoTrackError()
                if voice.is_playing and not voice.is_paused():
                    raise AudioNoTrackError()
                voice.stop()
            except ChannelNoVoiceError:
                await ctx.reply(messages['discord']['no_voice_channel'])
            except AudioNoTrackError:
                await ctx.reply(messages['discord']['no_active'])
            except AudioAlreadyPlayError:
                await ctx.reply(messages['discord']['already_play'])
            except:
                await ctx.reply(messages['discord']['unknown'])
                raise

        @self._bot.command()
        async def leave(ctx: commands.Context):
            try:
                if ctx.author.voice is None:
                    raise ChannelNoVoiceError()
                voice = discord.utils.get(self._bot.voice_clients, guild=ctx.guild)
                if voice is None:
                    raise CommandLeaveError()
                await voice.disconnect(force=True)
            except CommandLeaveError:
                await ctx.reply(messages['discord']['voice_channel_deactive'])
            except:
                await ctx.reply(messages['discord']['unknown'])
                raise

    def run(self):
        self._bot.run(self._token)
