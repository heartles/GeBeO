from discord.ext import commands
import discord
from helpers.filecmdhelper import *

class Sounds():
    def __init__(self, bot : commands.Bot):
        print("initializing sounds")
        self.bot = bot

    def after_sound_clip(self, player):
        player.vc.loop.create_task(player.vc.disconnect())

    async def soundhandler(self, message : discord.Message, filename : str):
        vchan = message.author.voice.voice_channel
        if vchan == None:
            await self.bot.say("You're not in a voice channel!")
        else:
            voice = await self.bot.join_voice_channel(vchan)
            player = voice.create_ffmpeg_player(filename, after=self.after_sound_clip)
            player.vc = voice
            player.start()

    @commands.command()
    async def slist(self):
        await filelister(self.bot, "sounds")

    @commands.command(pass_context=True)
    async def s(self, ctx : commands.Context):
        await filegetter(self.bot, "sounds", ctx.message, self.soundhandler)

    @commands.command(pass_context=True)
    async def sadd(self, ctx : commands.Context):
        await fileadder(self.bot, "sounds", ctx.message)

    @commands.command(pass_context=True)
    async def srm(self, ctx : commands.Context):
        await fileremover(self.bot, "sounds", ctx.message)

    @commands.command(pass_context=True)
    async def sstop(self, ctx : commands.Context):
        for vc in self.bot.voice_clients:
            for m in vc.channel.voice_members:
                if ctx.message.author == m:
                    await vc.disconnect()
                    return
        await self.bot.say("You're not in a voice chat that the bot is in!")

    @commands.command(pass_context=True)
    async def yt(self, ctx : commands.Context):
        arg = ' '.join(ctx.message.content.split(' ')[1:])
        vchan = ctx.message.author.voice.voice_channel
        if vchan == None:
            await self.bot.say("You're not in a voice channel!")
        else:
            voice = await self.bot.join_voice_channel(vchan)
            player = await voice.create_ytdl_player(arg, after=self.after_sound_clip)
            player.vc = voice
            player.start()

def setup(bot):
    print("setting up sounds")

    if not os.path.exists("sounds"):
        os.makedirs("sounds")

    bot.add_cog(Sounds(bot))