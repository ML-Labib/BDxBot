import discord
from discord import app_commands, Integration
from discord.ext import commands
from dotenv import dotenv_values

from cogs.tournament import Tournament
from cogs.config import BotConfiguration
from cogs.team import Teams

from parser.configParser import ConfigParser
from parser.tournamentParser import TournamentParser

#load .env variables
config = dotenv_values(".env")
BOT_TOKEN = config["BOT_TOKEN"]

class TournamentBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        self.guilds_id = discord.Object(id=1431861918246899775)

        self.config_parser = ConfigParser()
        self.tournament_parser = TournamentParser()

        super().__init__(command_prefix="ml", intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
  

    async def setup_hook(self):
        await self.add_cog(Tournament(self, self.tournament_parser))
        await self.add_cog(BotConfiguration(self, self.config_parser))
        await self.add_cog(Teams(self, self.tournament_parser, self.config_parser))
        try: 
            # self.tree.clear_commands(guild=self.guilds_id)

            # 2. Copy the "Global" commands (like your Tournament cog) to the specific Guild
            self.tree.copy_global_to(guild=self.guilds_id)

            # 3. Sync
            synced = await self.tree.sync(guild=self.guilds_id)
            print(f'Synced {len(synced)} command(s) to the guild {self.guilds_id.id}.')
            
        except Exception as e:
            print(f"Sync error: {e}")
        print("Cogs loaded successfully.")



if __name__ == "__main__":
    bot = TournamentBot()
    bot.run(BOT_TOKEN)