import discord
from discord import app_commands
from discord.ext import commands
from dotenv import dotenv_values

#load .env variables
config = dotenv_values(".env")
ADMIN_ROLE = config["ADMIN_ROLE"]

class Teams(commands.GroupCog, group_name="teams"):
    def __init__(self, bot: commands.Bot, profile: dict, config: dict) -> None:
        super().__init__()
        self.bot = bot
        self.profile = profile
        self.config = config

    @app_commands.command(name="status", description="List all teams in the current tournament")
    async def list_teams(self, interaction: discord.Interaction):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return

        teams: str = self.profile.all_teams_status()
        if not teams:
            await interaction.response.send_message("❌No teams found in the current tournament.", ephemeral=True)
            return

        await interaction.response.send_message(f"✅Teams in the current tournament:\n{teams}", ephemeral=True)


    @app_commands.command(name="create", description="Create Vc, moss channel and role for a team")
    async def create_team_resources(self, interaction: discord.Interaction):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        

        if self.config.get_vc_category() == "" or self.config.get_moss_category() == "":
            await interaction.response.send_message("⚠️Configuration incomplete.")
            return

        await interaction.response.defer(ephemeral=True)
        #create role
        guild: discord.Guild = interaction.guild
        tournament_role: discord.Role = discord.utils.get(guild.roles, name="Tournament")
        for team_name, team_info in self.profile.get_all_teams().items():
            role: discord.Role = discord.utils.get(guild.roles, name=team_name)

            if role is None:
                role = await guild.create_role(name = team_name, reason="Created by BDX bot.")
                self.profile.set_role_id(team_info, role.id)

            for player_key, player_info in team_info.get("players", {}).items():
                if player_info["role_given"]:
                    continue

                member: discord.Member = guild.get_member_named(player_info["name"])
                if member is None:
                    continue
                try:
                    await member.add_roles(role, tournament_role)
                    self.profile.update_role_given(team_info, player_info['name'], True)
                    print(f"{member.display_name} role given")
                except Exception as e:
                    print(f"{member.display_name} role failed to give")

            #create VS's
            vc_cat = guild.get_channel(int(self.config.get_vc_category()))
            moss_cat = guild.get_channel(int(self.config.get_moss_category()))
            
            if team_info["vc_id"] == "":
                overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False),
                role: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)}

                try:
                    vc = await guild.create_voice_channel(name = f"⚔️┊{team_info["lobby_number"]}┊{team_name}",
                                                    overwrites=overwrites,
                                                    category = vc_cat,
                                                    user_limit = 6)

                    self.profile.set_vc_id(team_info, vc.id)
                except Exception as e:

                    print(f"---------⚔️┊{team_info["lobby_number"]}┊{team_name} Failed: {e}")

            
            if team_info["moss_id"] == "":
                overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                role: discord.PermissionOverwrite(view_channel=True, read_messages=True, send_messages=True)
            }
                try: 
                    text_channel = await guild.create_text_channel(
                        name=f"📁┊{team_info["lobby_number"]}┊{team_name} Moss",
                        overwrites=overwrites,
                        category=moss_cat)
                    
                    self.profile.set_moss_id(team_info, text_channel.id)
                except Exception as e:
                        print(f"--------📁┊{team_info["lobby_number"]}┊{team_name} Moss Failed: {e}")
                
        await interaction.followup.send("Role, Vc and moss channel created successfully.")
    
    @app_commands.command(name="add", description="Add a new team to the tournament")
    async def add_team(self, interaction: discord.Interaction, team_name: str, lobby: str,  cptn: str, p2: str, p3: str, p4: str, p5: str, p6: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return

        is_already_exist = self.profile.get_team(team_name)
        if is_already_exist is not None:
            await interaction.response.send_message(f"❌Team '{team_name}' already exists.", ephemeral=True)
            return
        
        else:
            success = self.profile.add_team(team_name, lobby, cptn, p2, p3, p4, p5, p6)
            if success:
                await interaction.response.send_message(f"✅Team '{team_name}' added successfully.", ephemeral=True)
                return
        await interaction.response.send_message(f"❌Failed to add team '{team_name}'.", ephemeral=True)


    @app_commands.command(name="add_player", description="Add new player to a team")
    async def add_player(self, interaction: discord.Interaction, team_name: str, player_name: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return

        team = self.profile.get_team(team_name)
        if team is None:
            await interaction.response.send_message(f"❌Team '{team_name}' does not exist.", ephemeral=True)
            return

        success = self.profile.add_player(team, player_name)
        if success:
            await interaction.response.send_message(f"✅Player '{player_name}' added to team '{team_name}' successfully.", ephemeral=True)
            return
        await interaction.response.send_message(f"❌Failed to add player '{player_name}' to team '{team_name}'.", ephemeral=True)
        return


    @app_commands.command(name="remove", description="Remove a team from the tournament")
    async def remove_team(self, interaction: discord.Interaction, team_name: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer( ephemeral=True)
        guild: discord.Guild = interaction.guild

        team = self.profile.get_team(team_name)
        if team is None:
            await interaction.followup.send(f"❌Team '{team_name}' does not exist.", ephemeral=True)
            return
        
        role: discord.Role = discord.utils.get(guild.roles,  name=team_name)
        for player_key, player_info in team.get("players", {}).items():
            if player_info["role_given"] and role is not None:
                member = guild.get_member_named(player_info["name"])

                if member is None:
                    continue
                member.remove_roles(role)

        success = self.profile.remove_team(team_name)
        if success:
            await interaction.followup.send(f"✅Team '{team_name}' removed successfully.", ephemeral=True)
            return
        await interaction.followup.send(f"❌Failed to remove team '{team_name}'.", ephemeral=True)


    @app_commands.command(name="remove_player", description="Remove a single player from a team.")
    async def remove_player(self, interaction: discord.Interaction, team_name: str, player_name: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        
        team = self.profile.get_team(team_name)
        if team is None:
            await interaction.response.send_message(f"❌Team '{team_name}' does not exist.", ephemeral=True)
            return
        
        success = self.profile.remove_player(team, player_name)

        if success:
            guild = interaction.guild
            role = discord.utils.get(guild.roles, name=team_name)
            tournament_role = discord.utils.get(guild.roles, name="Tournament")
            member = guild.get_member_named(player_name)
            if role is None or member is None:
                await interaction.response.send_message(f"❌Player '{player_name}' does not exist.", ephemeral=True)
                return 
            
            await member.remove_roles(role)
            try:
                await member.remove_roles(tournament_role)
            except Exception as e:
                print(e)
            await interaction.response.send_message(f"✅Player '{player_name}' has been Removed.", ephemeral=True)
            return
        await interaction.response.send_message(f"❌Player '{player_name}' does not exist.", ephemeral=True)


    @app_commands.command(name="cleanup", description="Clean the channels")
    async def cleanup(self, interaction: discord.Interaction):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        if interaction.user.id == int(self.config.get_authorized_cleaner_1()) or interaction.user.id == int(self.config.get_authorized_cleaner_2()):
            auth = self.config.get_authorized()

            if len(auth) == 0:
    
                self.config.append_authorized(interaction.user.id)
                await interaction.followup.send("⚠️Wating for another authorizer's commad. ")
                return
            
            if interaction.user.id in auth and len(auth) == 1:
                await interaction.followup.send("⚠️Wating for another authorizer's commad. ")
                return
            
            if interaction.user.id not in auth and len(auth) == 1:
                guild = interaction.guild
                tournament_role: discord.Role = discord.utils.get(guild.roles, name="Tournament")
                honorary_role: discord.Role = discord.utils.get(guild.roles, name = "Honorary Fighter") 

                for team_name, team_info in self.profile.get_all_teams().items():
                    #moving from tournament to Honorary Fighter
                    for player_key, player_info in team_info.get("players", {}).items():
                        member: discord.Member = guild.get_member_named(player_info['name'])
                        if member:
                            await member.add_roles(honorary_role)
                            await member.remove_roles(tournament_role)
                            
                    #delete everything
                    vc_id = team_info["vc_id"]
                    moss_id = team_info["moss_id"]

                    vc = guild.get_channel(int(vc_id))
                    moss = guild.get_channel(int(moss_id))
                    role = discord.utils.get(guild.roles, name=team_name)

                    if vc:
                        await vc.delete()
                    if moss:
                        await moss.delete()
                    if role:
                        await role.delete()

                self.profile.reset_teams()
                self.config.reset_auth()

                await interaction.followup.send(f"✅Cleanup successful.")
                return
        await   interaction.followup.send("❌Unknown authorizer.")
        return


    @app_commands.command(name="send_announcement", description="Send the vc and moss channel to the players.")
    async def send_annoucement(self, interaction: discord.Integration):

        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)

        guild: discord.Guild = interaction.guild
        for team_name, team_info in self.profile.get_all_teams().items():
            for player_key, player_info in team_info.get("players", {}).items():
                content = f"Thank you for registering in our tournament.\nTeam: **{team_name}** and lobby number: **{team_info["lobby_number"]}**\nTeam Voice channel: <#{team_info["vc_id"]}>.\nPlease submit your moss file **individually** here: <#{team_info["moss_id"]}>\n"
                if not player_info["notified"]:
                    member: discord.Member = guild.get_member_named(player_info["name"])
                    if member:
                        await member.send(f"{content} || {member.mention} ||", )
                        self.profile.update_notified(player_info, True)
        
        await interaction.followup.send("✅All players have been notified.")


    @app_commands.command(name="send_text", description="Send custom text to all team member.")
    async def send_text(self, interaction: discord.Integration, header: str, body: str):
        if not any(role.name == ADMIN_ROLE for role in interaction.user.roles):
            await interaction.response.send_message("❌You do not have permission to use this command.", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)

        guild: discord.Guild = interaction.guild
        for team_name, team_info in self.profile.get_all_teams().items():
            for player_key, player_info in team_info["players"].items():
                member: discord.Member = guild.get_member_named(player_info["name"])
                if member:
                    await member.send(f"**{header}**\n{body} \n|| {member.mention} ||", )

            moss_id = team_info.get("moss_id", "")
            moss_channel: discord.TextChannel = guild.get_channel(int(moss_id))
            if moss_channel:
                await moss_channel.send(f"**{header}:\n----------------**")
        await interaction.followup.send("✅All players have been notified.")



