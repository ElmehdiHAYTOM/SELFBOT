import discord
from discord.ext import commands
from discord.ext.commands import command
import os
import requests
import shutil
import json, time
import asyncio
from PIL import Image


class cloner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def download_image(self, url, name):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36'
        }
        extension = url[-3:]
        response = requests.get(url, stream=True, headers=headers)
        with open(f"cogs/Images/emojies/{name}.{extension}", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

    @commands.group()
    async def add(self, ctx):
        pass

    @add.command(aliases=["channels"])
    async def achannels(self, ctx, server):
        '''
        clone channels +serverID
        '''
        server = self.bot.get_guild(int(server))
        myserver = ctx.guild
        for cat in server.categories:
            mycat = await myserver.create_category(cat.name,
                                                   overwrites=cat.overwrites)
            texts = cat.text_channels
            voices = cat.voice_channels
            for text in texts:
                await asyncio.sleep(3)
                myoverwrites = {}
                for role, perm in text.overwrites.items():
                    myrole = discord.utils.find(lambda r: r.name == role.name,
                                                myserver.roles)
                    myoverwrites[myrole] = perm
                try:
                    await mycat.create_text_channel(text.name,
                                                    overwrites=myoverwrites)
                except:
                    await mycat.create_text_channel(text.name)
            for voice in voices:
                await asyncio.sleep(3)
                myoverwrites = {}
                for role, perm in voice.overwrites.items():
                    await asyncio.sleep(3)
                    myrole = discord.utils.find(lambda r: r.name == role.name,
                                                myserver.roles)
                    myoverwrites[myrole] = perm
                try:
                    await mycat.create_voice_channel(
                        voice.name,
                        overwrites=myoverwrites,
                        user_limit=voice.user_limit)
                except:
                    await mycat.create_voice_channel(
                        voice.name, user_limit=voice.user_limit)

    @add.command(aliases=["roles"])
    async def aroles(self, ctx, server):
        '''
        clone roles +serverID
        '''
        server = self.bot.get_guild(int(server))
        myserver = ctx.guild
        roleslist = server.roles
        roleslist.reverse()
        for role in roleslist:
            await asyncio.sleep(3)
            if role.managed or role.name == "@everyone":
                pass
            else:
                try:
                    await myserver.create_role(name=role.name,
                                               permissions=role.permissions,
                                               colour=role.colour,
                                               hoist=role.hoist,
                                               mentionable=role.mentionable)
                except:
                    pass

    @add.command()
    async def all(self, ctx, server):
        await self.aroles(ctx, server)
        await self.achannels(ctx, server)
        await self.emojies(ctx, server)


############################################################

    @commands.group()
    async def clone(self, ctx):
        pass

    @clone.command()
    async def channels(self, ctx, server):
        '''
        clone channels +serverID
        '''
        server = self.bot.get_guild(int(server))
        myserver = ctx.guild
        for channel in myserver.channels:
            await channel.delete()
            await asyncio.sleep(3)
        for cat in server.categories:
            mycat = await myserver.create_category(cat.name,
                                                   overwrites=cat.overwrites)
            texts = cat.text_channels
            voices = cat.voice_channels
            for text in texts:
                await asyncio.sleep(3)
                myoverwrites = {}
                for role, perm in text.overwrites.items():
                    myrole = discord.utils.find(lambda r: r.name == role.name,
                                                myserver.roles)
                    myoverwrites[myrole] = perm
                try:
                    await mycat.create_text_channel(text.name,
                                                    overwrites=myoverwrites)
                except:
                    await mycat.create_text_channel(text.name)
            for voice in voices:
                await asyncio.sleep(3)
                myoverwrites = {}
                for role, perm in voice.overwrites.items():
                    myrole = discord.utils.find(lambda r: r.name == role.name,
                                                myserver.roles)
                    myoverwrites[myrole] = perm
                try:
                    await mycat.create_voice_channel(
                        voice.name,
                        overwrites=myoverwrites,
                        user_limit=voice.user_limit)
                except:
                    await mycat.create_voice_channel(
                        voice.name, user_limit=voice.user_limit)

    @clone.command()
    async def roles(self, ctx, server):
        '''
        clone roles +serverID
        '''
        server = self.bot.get_guild(int(server))
        myserver = ctx.guild
        for role in myserver.roles:
            await asyncio.sleep(3)
            try:
                await role.delete()
            except:
                pass
        roleslist = server.roles
        roleslist.reverse()
        for role in roleslist:
            await asyncio.sleep(3)
            if role.managed or role.name == "@everyone":
                pass
            else:
                try:
                    await myserver.create_role(name=role.name,
                                               permissions=role.permissions,
                                               colour=role.colour,
                                               hoist=role.hoist,
                                               mentionable=role.mentionable)
                except:
                    pass

    @clone.command()
    async def emojies(self, ctx, server):
        """
        clone emojies +serverID
        """
        server = self.bot.get_guild(int(server))
        myserver = ctx.guild
        for each in server.emojis:

            new_name = "HB_" + each.name

            if each.animated:
                self.download_image(
                    f"https://cdn.discordapp.com/emojis/{each.id}.gif",
                    each.name)
                im = open(f"cogs/Images/emojies/{each.name}.gif", 'rb')
                await myserver.create_custom_emoji(name=new_name,
                                                   image=im.read())
                im.close()
                os.remove(f"cogs/Images/emojies/{each.name}.gif")
            else:
                self.download_image(
                    f"https://cdn.discordapp.com/emojis/{each.id}.png",
                    each.name)
                im = open(f"cogs/Images/emojies/{each.name}.png", 'rb')
                await myserver.create_custom_emoji(name=new_name,
                                                   image=im.read())
                im.close()
                os.remove(f"cogs/Images/emojies/{each.name}.png")

    @clone.command()
    async def icon(self, ctx, server):  # b'\xfc'
        '''
        cloneicon +serverID
        '''
        server = self.bot.get_guild(int(server))
        icon_url = server.icon_url
        with open('cogs/Images/stolensv.png', 'wb') as f:
            r = requests.get(icon_url, stream=True)
            for block in r.iter_content(1024):
                if not block:
                    break
                f.write(block)
        Image.open('cogs/Images/stolensv.png').convert('RGB')
        with open('cogs/Images/stolensv.png', 'rb') as f:
            await ctx.message.guild.edit(icon=f.read())

    @clone.command()
    async def name(self, ctx, server):  # b'\xfc'
        '''
        clonename +serverID
        '''
        server = self.bot.get_guild(int(server))
        await ctx.message.guild.edit(name=server.name)

    @clone.command()
    async def all(self, ctx, server):
        await self.roles(ctx, server)
        await self.channels(ctx, server)
        await self.icon(ctx, server)
        await self.name(ctx, server)

        #await self.emojies(ctx, server)


def setup(bot):
    bot.add_cog(cloner(bot))
