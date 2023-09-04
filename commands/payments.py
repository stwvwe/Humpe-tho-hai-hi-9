from discord.ext import commands
import discord
from discord import Option
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

class Payments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Check our payment methods', name='payments')
    async def payments(self, interaction: discord.Interaction):
        embed = discord.Embed(title='Payment Methods', color=config['embed_color'])
        if config['paypal_enabled'] == True:
            embed.add_field(name="Paypal", value=f"```{config['paypal']}```", inline=False)
        if config['cashapp_enabled'] == True:
            embed.add_field(name="Cashapp", value=f"```{config['cashapp']}```", inline=False)
        if config['btc_enabled'] == True:
            embed.add_field(name="BTC Address", value=f"```{config['btc']}```", inline=False)
        if config['eth_enabled'] == True:
            embed.add_field(name="ETH Address", value=f"```{config['eth']}```", inline=False)
        if config['ltc_enabled'] == True:
            embed.add_field(name="LTC Address", value=f"```{config['ltc']}```", inline=False)
                   
        await interaction.respond(embed=embed, ephemeral=True)

        if config['command_logging'] == True:
            channel = self.bot.get_channel(int(config['command_logs_channel']))
            embed = discord.Embed(title='/payments', description=f'Checked payment methods.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
            await channel.send(embed=embed)
