from discord.ext import commands
import discord
from discord import Option
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Check functionality of all commands.', name='help')
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="All bot's commands", description=f'``/stock`` - Check stock of our nitro links/nitro tokens\n``/restock`` - Restock nitro links/nitro tokens to your bot using paste.ee\n``/restockalert`` - Sends out alert that you have restocked in your restock channel\n``/whitelist`` - Whitelisting a user will grant him access to all commands\n``/payments`` - Shows all our payment methods\n``/help`` - Sends out this help embed', color=config['embed_color'])
        
        await interaction.respond(embed=embed, ephemeral=True)
        if config['command_logging'] == True:
            channel = self.bot.get_channel(int(config['command_logs_channel']))
            embed = discord.Embed(title='/help', description=f'Checked all commands functionality.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
            await channel.send(embed=embed)