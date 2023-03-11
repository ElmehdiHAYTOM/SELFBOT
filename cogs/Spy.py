import discord
from discord.ext import commands
from discord.ext.commands import command


class Utils(commands.Cog):
	def __init__(self,bot):
		self.bot=bot


	def embed(self,ctx,dict,spy):
		print(dict)
		k=0

		embed = discord.Embed(title="SPY : "+spy,)
		embed.set_author(name=self.guild.name, icon_url=self.guild.icon_url)
		for i in dict:
			embed.add_field(name="-> "+ i+ str(len(dict[i])), value=dict[i], inline=0)
			k +=len(dict[i])
		embed.set_footer(text="total = "+str(k))
		return embed

	def embed_channel(self,ctx,list,spy):
		k=0

		embed = discord.Embed(title="SPY : "+spy,)
		embed.set_author(name=self.guild.name, icon_url=self.guild.icon_url)
		for i in dict:
			k+=1
			embed.add_field(name="-> "+ str(k), value=i, inline=0)
		embed.set_footer(text="total = "+str(k))
		return embed



	@commands.group()
	async def spy(self,ctx , server):
		self.guild = self.bot.get_guild(int(server))
############################################## USERS SPY ###########################################
	@spy.command()
	async def roles(self,ctx):
		for role in self.guild.roles:
            await asyncio.sleep(2)
			await ctx.send("***"+role.name+"***"+"\n")
		return


	@spy.command()
	async def users(self,ctx):
		voices = {}
		for voice in self.guild.voice_channels:
            await asyncio.sleep(2)
			members=[]
			for member in voice.members:
				members.append(member.name)
			if len(members)>0:
				voices[voice.name] = voice.voice_states.keys()#members#"\n".join(members)
			
			if len(voice.voice_states.keys())>0:
				await ctx.send("***"+"\n"+"\n"+voice.name + "    :  "+"\n"+"\n"+"***")
				for i in list(voice.voice_states.keys()) :
					member=self.guild.get_member(i)
					if member:


						await ctx.send(member.name)
	

					else:
						await ctx.send(i)
			else:
				pass
		return


def setup(bot):
	bot.add_cog(Utils(bot))
