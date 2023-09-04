from discord.ext import commands
import discord
from discord import Option
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

products = ['Nitro Links', '1m Nitro Tokens', '3m Nitro Tokens']

class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Check stock of nitro tokens/nitro links.', name='stock')
    async def stock(self, interaction: discord.Interaction, product: Option(str, "Product that you want to check stock of", choices=products, required=True)):
        if product == 'Nitro Links':
            file = open(config['nitro_links_file'], "r").readlines()
            embed = discord.Embed(title='Stock', description=f'You currently have ``{len(file)}`` nitro links in stock.', color=config['embed_color'])

            await interaction.respond(embed=embed)
        elif product == '1m Nitro Tokens':
            file = open(config['nitro_tokens_1m_file'], "r").readlines()
            embed = discord.Embed(title='Stock', description=f'You currently have ``{len(file)}`` 1 month nitro tokens in stock.', color=config['embed_color'])

            await interaction.respond(embed=embed)
        elif product == '3m Nitro Tokens':
            file = open(config['nitro_tokens_3m_file'], "r").readlines()
            embed = discord.Embed(title='Stock', description=f'You currently have ``{len(file)}`` 3 month nitro tokens in stock.', color=config['embed_color'])

            await interaction.respond(embed=embed)
            
        if config['command_logging'] == True:
            channel = self.bot.get_channel(int(config['command_logs_channel']))
            if product == 'Nitro Links':
                embed = discord.Embed(title='/stock', description=f'Checked stock of nitro links', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
            elif product == '1m Nitro Tokens':
                embed = discord.Embed(title='/stock', description=f'Checked stock of 1m nitro tokens.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
            elif product == '3m Nitro Tokens':
                embed = discord.Embed(title='/stock', description=f'Checked stock of 3m nitro tokens.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}") 
            await channel.send(embed=embed)