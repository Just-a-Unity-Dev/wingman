from concurrent.futures import process
import os
import discord
from discord.commands import Option
from discord.ui import Button, Modal, InputText, View
from dotenv import load_dotenv
load_dotenv()

owner_id = 780807643451228190

client = discord.Bot()
guild_ids = [882062811667247125]

class MarketForm(Modal):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.add_item(InputText(label='Item', placeholder="eg: 64 sand / a stack of sand"))
		self.add_item(InputText(label='Price', placeholder="eg: 16$ / 8 iron ingots"))
		self.add_item(
			InputText(
				label='Type',
				placeholder="looking for / selling"
			)
		)
		self.add_item(InputText(label='Description', placeholder="i need a stack of sand for my builds"))
		
	async def callback(self, interaction: discord.Interaction):
		global channels

		embed = discord.Embed(title='Market Item', description=self.children[3].value, color=discord.Color.random())
		embed.add_field(name='Item', value=self.children[0].value, inline=True)
		embed.add_field(name='Price', value=self.children[1].value, inline=True)
		embed.add_field(name='Type', value=self.children[2].value, inline=True)
		embed.set_footer(icon_url=interaction.user.avatar.url, text="Requested by {}".format(interaction.user.name))

		await mls.purge(limit=1)

		rootMessage = await mls.send(embed=embed)
		thread = await rootMessage.create_thread(name=f"{self.children[0].value} - {self.children[2].value}", auto_archive_duration=60)
		await thread.send(f"<@&956708907449987102>")
		await makemarketlisting()

		await interaction.response.send_message(f"Successfully made a listing in <#{mls.id}> under the thread <#{thread.id}>", ephemeral=True)


@client.slash_command(guild_ids=guild_ids)
async def hello(ctx, name: str = None):
	name = name or ctx.author.name
	await ctx.respond(f"Hello {name}!")

async def makemarketlisting():
	global channels
	
	button = Button(label='Submit', style=discord.ButtonStyle.gray)
	
	async def callback(interaction):
		form = MarketForm("New Market Listing")
		await interaction.response.send_modal(form)

		await mls.purge(limit=1)
		await makemarketlisting()

	button.callback = callback

	view = View()
	view.add_item(button)

	embed = discord.Embed(
			title="Create A Listing",
			description="__Welcome to the market!__\n\nSome of us look for items, some look for a quick buck. Some just wanna get rid of junk.\nThe market is the place for everyone, buyers and sellers alike!\nWant to get notified when theres a new listing? Pick the Market Ping Role in <#882064590542888960> and you'll be notified when there's a new listing!\n\nPress the green button to open the Market Form, fill it in and you're on your way!",
			color=discord.Color.magenta()
		)

	await mls.send(view=view, embed=embed)

# @client.slash_command(guild_ids=guild_ids, pass_context=True)
# async def setup(ctx):
# 	if ctx.author.id != owner_id:
# 		await ctx.respond("Shut the fuck up")
# 		return None
# 	await makemarketlisting()
# 	await ctx.respond("Finished setup!")

@client.event
async def on_ready():
	global mls

	mls = client.get_guild(guild_ids[0]).get_channel(963299254653296691)
	await client.change_presence(activity=discord.Game(name="Minecraft"))

	await mls.purge(limit=1)
	await makemarketlisting()

	print(f"Logged in as {client.user}")

client.run(os.getenv("DISCORD_TOKEN"))