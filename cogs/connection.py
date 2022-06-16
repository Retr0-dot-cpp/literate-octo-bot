import discord
from discord.ext import commands
from discord.ext.commands import errors
from discord import errors as dpy_errors

class Connection(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.database = None

	@commands.Cog.listener() 
	async def on_ready(self):
		self.database = self.client.get_guild(986282733561073706)
        server = database.categories[0]
        mainChannel = server.channels[0]

        connectionAmount = len(database.categories)-1
        
        await mainChannel.delete()
        await server.create_text_channel(name=f"connections-{connectionAmount}")

        print(f"[CONNECTION] {connectionAmount} applications are currently connected to the database")

	@commands.command()
	async def updateConnection(self, ctx):
		
		connectionAmount = -1

		for i in self.database.categories:
			connectionAmount += 1

		server = self.database.categories[0]
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
			
			checker = 0

			for i in self.database.categories:
				if i.name == name:
					await ctx.send("Unfortunately for now you can't create cluster with following name as it is already existing.")
					break
				else:
					checker += 1

			if checker == len(self.database.categories):
				cluster = await self.database.create_category(name=name)
				mainChannel = await cluster.create_text_channel(name="info")
				noteChannel = await cluster.create_text_channel(name="notes")
				fileChannel = await cluster.create_text_channel(name="files")

				await ctx.send("Cluster with following name was successfully created. To create \ncollections, try using `$createCollection command`")
				await mainChannel.edit(topic=f"'creator': {ctx.author.id}")

	@commands.command()
	async def deleteCluster(self, ctx, name=None):	
		if name is None:
			await ctx.send("You must enter name for the cluster you want to delete.")
		else:
			checker = 0
			authorId = 0
			categoryId = None
			message = ctx.message

			for i in self.database.categories:
				if i.name == name:
					categoryId = i.id

					for j in i.channels:
						if j.name == "info":
							if str(j.topic).startswith("'creator'"):
								authorId = j.topic[11:]
								break
				else:
					checker += 1

			if int(ctx.author.id) == int(authorId):
				if checker == len(self.database.categories):
					await ctx.send("Probably you entered invalid name as there are no available cluster with such name.")
				else:

					msg = await ctx.channel.send('Please confirm your action with pressing on following reaction')
					await msg.add_reaction("✅")
					await msg.add_reaction("❌")

					def check(reaction, user):
						return user == message.author

					try:
						reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
			        
					except asyncio.TimeoutError:
						await msg.edit(content="Unfortunately you didn't confirm your action, which means that cluster won't be deleted.")
			        
					else:
						if reaction.emoji == '❌':
							await msg.edit(content="You canceled your actions, which means that cluster won't be deleted.")

						elif int(ctx.author.id) == int(authorId):
							for z in self.database.categories:
								if z.id == categoryId:
									for l in z.channels:
										await l.delete()
									await z.delete(	)

							await msg.edit(content="Cluster with name you entered was successfully deleted.")
					await msg.clear_reactions()
			else:
				await ctx.send("Only creator of the cluster with entered name can delete it, while you are not one.")

	@commands.command()
	async def insertNote(self, ctx, cluster=None, name=None, *, content=None):
		if cluster is None:
			await ctx.send("Please enter a valid name for cluster you want to update with your note, in the following form: `$insertNote <cluster> <name> <content>`")
		if name is None:
			await ctx.send("Please enter a valid name for your note in this form: `$insertNote <cluster> <name> <content>`")
		elif content is None:
			await ctx.send("Please enter content of your note in the following form: `$insertNote <cluster> <name> <content>`")
		elif len(name) > 48:
			await ctx.send("Unfortunately for now we are not able to create a note with name which has length more than 48 symbols. Try decreasing it to finish your operation.")
		elif len(content) > 1952:
			await ctx.send("Unfortunately for now we are not able to create a note with content which has length more than 1952 symbols as discord has limits. Try decreasing it to finish your operation.")
		else:
			count = 0
			for i in self.database.categories:
				if i.name == cluster:

					secondCount = 0
					thirdCount = 0

					if i.channels[1].topic:
						topicLines = str(i.channels[1].topic).split("\n")
						for line in topicLines:
							try:
								var = eval(line)
								checker = var[name]
							except KeyError:
								secondCount += 1

							thirdCount += 1

					if secondCount == thirdCount:
						msg = await i.channels[1].send(f"'{name}': '{content}'")

						if i.channels[1].topic:
							await i.channels[1].edit(topic=(i.channels[1].topic + "\n" + "{'" + name + "':" + str(msg.id) + "}"))
						else:
							await i.channels[1].edit(topic=("{'" + name + "':" + str(msg.id) + "}"))

						await ctx.send("Your note was successfully added to the cluster with entered name.")
						break
					else:
						await ctx.send("Note with following name is already existing, try using another one.")
				
				else:
					count += 1

			if count == len(self.database.categories):
				await ctx.send("Name of cluster you entered does not exist in the databse.")
			
def setup(client):
	client.add_cog(Connection(client))