import discord
from discord import app_commands, Integration

from discord.ext import commands
from dotenv import dotenv_values
from cogs.Tournament import Tournament

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

        super().__init__(command_prefix="ml", intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

        print('------')


    async def setup_hook(self):
        await self.add_cog(Tournament(self))
        await self.tree.sync(guild=self.guilds_id)

    # async def on_message(self, message):
    #     if message.author.bot:
    #         return
    #     else:
    #         await message.channel.send(f"Hello {message.author.mention}, you said: {message.content}")

if __name__ == "__main__":
    bot = TournamentBot()
    bot.run(BOT_TOKEN)