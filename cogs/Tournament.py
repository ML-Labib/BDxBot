import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values
import asyncio

#load .env variables
config = dotenv_values(".env")
ADMIN_ROLE_ID = config["ADMIN_ROLE_ID"]
ADMIN_ROLE = config["ADMIN_ROLE"]

class Tournament(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="start_tournament", description="Start a new tournament")
    async def start_tournament(self, interaction: discord.Interaction, sheet_url: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        await asyncio.sleep(5)  # Simulate some processing time
        print(f"Tournament started with sheet URL: {sheet_url}")
        await interaction.followup.send("Tournament started!", ephemeral=True)

    @app_commands.command(name="end_tournament", description="End the current tournament")
    async def end_tournament(self, interaction: discord.Interaction):
        await interaction.response.send_message("Tournament ended!", ephemeral=True)
