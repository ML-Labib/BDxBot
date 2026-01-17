import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values
from google.sheet import get_csv_form_sheet
import asyncio
import json


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
        data = get_csv_form_sheet(sheet_url)
        status_code, reader = data

        if status_code != 200:
            await interaction.followup.send(f"❌{reader}", ephemeral=True)
            return

        for teams in reader:
            print(teams["Team_name"])

        await interaction.followup.send("Tournament started!", ephemeral=True)

    @app_commands.command(name="end_tournament", description="End the current tournament")
    async def end_tournament(self, interaction: discord.Interaction):
        await interaction.response.send_message("Tournament ended!", ephemeral=True)
