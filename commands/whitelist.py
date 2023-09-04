from discord.ext import commands
import discord
from discord import Option
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Whitelist a user with ease.', name='whitelist')
    async def whitelist(self, interaction: discord.Interaction, user: discord.Option(discord.Member, "Member to whitelist", required=True)):
        if str(interaction.author.id) != config['bot_owner']:
            embed = discord.Embed(title='Error', description=f'You are not whitelisted to use this command.', color=config['embed_error_color'])
          
            await interaction.respond(embed=embed, ephemeral=True)

        else:
            if not (str(user.id) in open("whitelist.txt", "r").read().splitlines()) and str(user.id) != config['bot_owner']:
                with open("whitelist.txt", "a") as whitelist:
                    whitelist.write(str(user.id) + "\n")
                
                embed = discord.Embed(title='Success', description=f'Successfully whitelisted {user}.', color=config['embed_color'])
                await interaction.respond(embed=embed)

                if config['command_logging'] == True:
                    channel = self.bot.get_channel(int(config['command_logs_channel']))
                    embed = discord.Embed(title='/whitelist', description=f'{user} got whitelisted.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                    await channel.send(embed=embed)

            elif str(user.id) == config['bot_owner']:
                embed = discord.Embed(title='Error', description=f'You are alredy owner.', color=config['embed_error_color'])
                await interaction.respond(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title='Error', description=f'{user} is alredy whitelisted.', color=config['embed_error_color'])
                await interaction.respond(embed=embed, ephemeral=True)
            
            