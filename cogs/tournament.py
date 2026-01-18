import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values
from google.sheet import get_csv_form_sheet

#load .env variables
config = dotenv_values(".env")
ADMIN_ROLE_ID = config["ADMIN_ROLE_ID"]
ADMIN_ROLE = config["ADMIN_ROLE"]

class Tournament(commands.GroupCog, group_name="tournament"):
    def __init__(self, bot: commands.Bot, tournament_parser: dict):
        super().__init__()
        self.bot = bot
        self.profile = tournament_parser


    @app_commands.command(name="create", description="Create a new tournament from a Google Sheet link")
    async def create(self, interaction: discord.Interaction, gsheet_link: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        data = get_csv_form_sheet(gsheet_link)
        status_code, reader = data

        if status_code != 200:
            await interaction.followup.send(f"❌{reader}", ephemeral=True)
            return
        self.profile.new_profile(reader)

        await interaction.followup.send("Tournament created successfully!", ephemeral=True)

