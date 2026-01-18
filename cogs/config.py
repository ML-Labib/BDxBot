import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values

#load .env variables
config = dotenv_values(".env")
ADMIN_ROLE = config["ADMIN_ROLE"]

class BotConfiguration(commands.GroupCog, group_name="config"):
    def __init__(self, bot: commands.Bot, config: dict):
        super().__init__()
        self.bot = bot
        self.config = config

    # @app_commands.guilds(1431861918246899775)
    @app_commands.command(name="moss_category", description="Set the category for MOSS submissions channels")
    async def moss_category(self, interaction: discord.Interaction, category_id: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        self.config.set_moss_category(category_id)
        await interaction.response.send_message("✅MOSS category set successfully.", ephemeral=True)


    @app_commands.command(name="vc_category", description="Set the category for voice channels")
    async def vc_category(self, interaction: discord.Interaction, category_id: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        self.config.set_vc_category(category_id)
        await interaction.response.send_message("✅Voice channel category set successfully.", ephemeral=True)

    @app_commands.command(name="set_first_cleaner", description="Set the first authorized cleaner")
    async def set_first_cleaner(self, interaction: discord.Interaction, user_id: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        result = self.config.set_authorized_cleaner_1(user_id)
        if not result:
            await interaction.response.send_message("❌This user is already set as the second authorized cleaner.", ephemeral=True)
            return
        await interaction.response.send_message("✅Authorized cleaner 1 set successfully.", ephemeral=True)

    @app_commands.command(name="set_second_cleaner", description="Set the second authorized cleaner")
    async def set_second_cleaner(self, interaction: discord.Interaction, user_id: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        result = self.config.set_authorized_cleaner_2(user_id)
        if not result:
            await interaction.response.send_message("❌This user is already set as the first authorized cleaner.", ephemeral=True)
            return
        await interaction.response.send_message("✅Authorized cleaner 2 set successfully.", ephemeral=True)

    @app_commands.command(name="show_config", description="Show the current bot configuration")
    async def show_config(self, interaction: discord.Interaction):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        config_text = self.config.show_config()
        await interaction.response.send_message(f"{config_text}", ephemeral=True)

    @app_commands.command(name="reset_config", description="Reset the bot configuration to default")
    async def reset_config(self, interaction: discord.Interaction):  
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        self.config.reset_config()
        await interaction.response.send_message("✅Configuration reset to default successfully.", ephemeral=True)