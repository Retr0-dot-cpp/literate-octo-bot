import discord, os, random, ast
from discord.ext import commands

client = commands.Bot(command_prefix="$", intents=discord.Intents.all()) 
client.remove_command('help')

@client.command()
async def load(ctx, extension):
	if ctx.author.id in config.developers:
		try:
			client.load_extension(f"cogs.{extension}")
			await ctx.send("Cog has been succesfully laucnhed")
		except:
			await ctx.send(f"Cog {extension} was not found!")
	else:
		await ctx.send("You don't have enough permissions to use this command!")
		
@client.command() 
async def unload(ctx, extension):
	if ctx.author.id in config.developers:
		try:
			client.unload_extension(f"cogs.{extension}")
			await ctx.send("Ког успешно отгружен.")
		except:
			await ctx.send(f"Cog {extension} was not found!")
	else:
		await ctx.send("You don't have enough permissions to use this command!")
		
@client.command() 
async def reload(ctx, extension):
	if ctx.author.id in developers:
		try:
			client.unload_extension(f"cogs.{extension}")
			client.load_extension(f"cogs.{extension}")
			await ctx.send("Cog has been successfully reastarted.")
		except:
			await ctx.send(f"Cog {extension} was not found")
	else:
		await ctx.send("You don't have enough permissions to use this command!")

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@client.command(aliases=['ev', 'e'])
async def eval_fn(ctx, *, cmd):
	if ctx.author.id == 655348554918920234:
		if cmd.startswith('```py') and cmd.endswith('```'):
			cmd = cmd[5:-3]
		elif cmd.startswith('```') and cmd.endswith('```'):
			cmd = cmd[3:-3]

		fn_name = "_eval_expr"

		cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

		body = f"async def {fn_name}():\n{cmd}"

		parsed = ast.parse(body)
		body = parsed.body[0].body

		insert_returns(body)

		env = {
			'client': ctx.bot,
			'discord': discord,
			'commands': commands,
			'ctx': ctx,
			'guild': ctx.guild,
            '__import__': __import__
		}
		exec(compile(parsed, filename="<ast>", mode="exec"), env)

		result = (await eval(f"{fn_name}()", env))
	else:
		await ctx.send("Only Aprojs can use this command!")

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}") 

client.run(config.token) 
