import discord
from discord.ext import commands
from discord.ext.commands import command
from pathlib import Path
import requests
from PIL import Image
import os


class GENERAL(
        commands.Cog, ):
    def __init__(self, bot):
        self.bot = bot
        self.stolen = Path("cogs/Images/stolenav.png")
        self.profilepic = Path("cogs/Images/av.png")
        self.password = os.environ["pass"]

    @commands.command()
    async def set_name(self, ctx, *, name):
        name = "".join(name)
        await self.bot.user.edit(password=self.password, username=name)

    @commands.command()
    async def set_picture(self, ctx, url):  # b'\xfc'
        with open(self.profilepic, 'wb') as f:
            r = requests.get(url, stream=True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)
        try:
            Image.open(self.profilepic).convert('RGB')
            with open(self.profilepic, 'rb') as f:
                await self.bot.user.edit(password=self.password,
                                         avatar=f.read())
        except discord.HTTPException as e:
            print(e)


#######################################################################################

    @commands.command()
    async def steal_picture(self, ctx, user: discord.Member):
        with open(self.stolen, 'wb') as f:
            r = requests.get(user.avatar_url, stream=True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)
        try:
            Image.open(self.stolen).convert('RGB')
            with open(self.stolen, 'rb') as f:
                await self.bot.user.edit(password=self.password,
                                         avatar=f.read())
        except discord.HTTPException as e:
            print(e)

    @commands.command()
    async def steal_name(self, ctx, user: discord.Member):
        return await self.bot.user.edit(password=self.password,
                                        username=user.name)


def setup(bot):
    bot.add_cog(GENERAL(bot))
