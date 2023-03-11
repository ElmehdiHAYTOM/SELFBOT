from discord.ext import commands
from discord.ext.commands import command
import discord
class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk = 0
        self.Guild=0
        self.Voice_channel=0
        
    @command()
    async def AFK(self,ctx,guild=None,channel=None):
        await ctx.message.delete()

        if self.afk==1:
            self.afk=0

        elif self.afk == 0:
            self.afk=1
            self.Guild=guild
            self.Voice_channel=channel







    @commands.Cog.listener()
    async def on_voice_state_update(self,member,befor,after):
        if member.id == self.bot.user.id and self.afk:
            try:
                ws = self.bot._connection._get_websocket(int(self.Guild))
                await ws.voice_state(str(self.Guild), str(self.Voice_channel))
            except Exception as e:
                print("Error Joining voice channel")
                print("-"*(len(str(e))-1))
                print("|"+e+"|")
                print("-"*(len(str(e))-1))

def setup(bot):
    bot.add_cog(AFK(bot))
