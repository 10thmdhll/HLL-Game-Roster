import os
import discord
from discord import app_commands
import subprocess
import config
from dotenv import load_dotenv

load_dotenv()

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.tree.sync()
        print("Slash commands synced.")

client = MyClient()

@client.tree.command(name="roster", description="Generate and post the current roster.")
@app_commands.describe(
    server="Select the HLL server to pull from",
    mode="Choose 'one_team' or 'two_teams'"
)
async def roster(
    interaction: discord.Interaction,
    server: str = None,
    mode: str = "two_teams"
):
    await interaction.response.defer()

    if server and server not in config.SERVERS:
        await interaction.followup.send(f"Invalid server: {server}")
        return

    if mode not in getattr(config, "ROSTER_MODES", ["one_team", "two_teams"]):
        await interaction.followup.send(f"Invalid mode: {mode}")
        return

    args = ["python", "main.py"]
    if server:
        args.append(server)
    if mode:
        args.append(mode)

    proc = subprocess.run(args, capture_output=True)
    if proc.returncode == 0:
        if os.path.exists("poster_output/poster_latest.png"):
            embed = discord.Embed(
                title="Roster Generated",
                description=f"Server: `{server}`\nMode: `{mode}`",
                color=0x00ffcc
            )
            embed.set_image(url="attachment://poster_latest.png")
            file = discord.File("poster_output/poster_latest.png", filename="poster_latest.png")
            await interaction.followup.send(embed=embed, file=file)
        else:
            await interaction.followup.send("Roster image could not be generated.")

    else:
        error_msg = proc.stderr.decode().strip().splitlines()[-1] if proc.stderr else "Unknown error."
        await interaction.followup.send(f"Roster generation failed: `{error_msg}`")

@roster.autocomplete("server")
async def server_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name=name, value=name)
        for name in config.SERVERS.keys()
        if current.lower() in name.lower()
    ]

@roster.autocomplete("mode")
async def mode_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    options = getattr(config, "ROSTER_MODES", ["one_team", "two_teams"])
    return [
        app_commands.Choice(name=opt.replace("_", " ").title(), value=opt)
        for opt in options
        if current.lower() in opt.lower()
    ]

token = os.getenv("DISCORD_BOT_TOKEN")
if not token:
    raise ValueError("DISCORD_BOT_TOKEN is not set in your environment or .env file.")
client.run(token)
