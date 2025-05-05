import discord
from discord.ext import commands
import subprocess

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(
    name="roster",
    description="Generate and post the current roster."
)
@app_commands.describe(
    choice="Server",
    description="Pick which HLL Server to look for players"
)
async def roster(ctx, server: str = None, mode: str = "two_teams"):
    await ctx.defer()
    args = ["python", "main.py"]
    if server:
        args.append(server)
    if mode:
        args.append(mode)

    proc = subprocess.run(args, capture_output=True)
    if proc.returncode == 0:
        await ctx.send(file=discord.File("poster_output/poster_latest.png"))
    else:
        await ctx.send(f"Roster generation failed. Error: {proc.stderr.decode()}")

bot.run("YOUR_DISCORD_BOT_TOKEN")
