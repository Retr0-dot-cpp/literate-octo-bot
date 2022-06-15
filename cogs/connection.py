import discord
from discord.ext import commands
from discord.ext.commands import errors
from discord import errors as dpy_errors

class Connection(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener() 
	async def on_ready(self):
		database = self.client.get_guild(986282733561073706)
		server = database.categories[0]
		connectionAmount = server.channels[0]

		print(f"[CONNECTION] {connectionAmount.name[12:]} applications are currently connected to the database")

	@commands.command()
	async def updateConnection(self, ctx):
		database = self.client.get_guild(986282733561073706)
		connectionAmount = -1

		for i in database.categories:
			connectionAmount += 1

		server = database.categories[0]
		checker = server.channels[0]

		await checker.delete()
		await server.create_text_channel(name=f"connections-{connectionAmount}")
		await ctx.send("Connection amount has been manually and successfully updated")

		print("Connection amount has been reloaded")

	@commands.command()
	async def createCluster(self, ctx, name=None):
		if name is None:
			await ctx.send("You must enter name for the cluster you want to create.")
		else:
			database = self.client.get_guild(986282733561073706)
			checker = 0

			for i in database.categories:
				if i.name == name:
					await ctx.send("Unfortunately for now you can't create cluster with following name as it is already existing.")
					break
				else:
					checker += 1

			if checker == len(database.categories):
				cluster = await database.create_category(name=name)
				firstChannel = await cluster.create_text_channel(name="main_info")

				await ctx.send("Cluster with following name was successfully created. To create \ncollections, try using `$createCollection command`")
				await firstChannel.edit(topic=f"'creator': {ctx.author.id}")

	@commands.command()
	async def deleteCluster(self, ctx, name=None):	
		if name is None:
			await ctx.send("You must enter name for the cluster you want to delete.")
		else:
			database = self.client.get_guild(986282733561073706)
			checker = 0
			authorId = 0
			categoryId = None
			message = ctx.message

			for i in database.categories:
				if i.name == name:
					categoryId = i.id

					for j in i.channels:
						if j.name == "main_info":
							if str(j.topic).startswith("'creator'"):
								authorId = j.topic[11:]
								break
				else:
					checker += 1

			if int(ctx.author.id) == int(authorId):
				if checker == len(database.categories):
					await ctx.send("Probably you entered **invalid** name as there are no available cluster with such name.")
				else:

					msg = await ctx.channel.send('Please **confirm** your action with following reaction')
					await msg.add_reaction("✅")
					await msg.add_reaction("❌")

					def check(reaction, user):
						return user == message.author

					try:
						reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
			        
					except asyncio.TimeoutError:
						await ctx.send("Unfortunately you **didn't confirm** your action, which means that **cluster won't be deleted**.")
			        
					else:
						if(reaction.emoji == '❌'):
							await ctx.send("You **cancelled** this operation, which means that **cluster won't be deleted**.")

						elif int(ctx.author.id) == int(authorId):
							for z in database.categories:
								if z.id == categoryId:
									for l in z.channels:
										await l.delete()
									await z.delete(	)

							await ctx.send("Cluster with name you entered was successfully **deleted**.\n||P.S. All actions are irretrievable||")
			else:
				await ctx.send("Only creator of the cluster with entered name can delete it, while you are not one.")

def setup(client):
	client.add_cog(Connection(client))