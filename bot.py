import os
import discord
from discord import app_commands
import subprocess
import config

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

    args = ["python", "main.py"]
    if server:
        args.append(server)
    if mode:
        args.append(mode)

    proc = subprocess.run(args, capture_output=True)
    if proc.returncode == 0:
        await interaction.followup.send(file=discord.File("poster_output/poster_latest.png"))
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

client.run(os.getenv("DISCORD_BOT_TOKEN"))
