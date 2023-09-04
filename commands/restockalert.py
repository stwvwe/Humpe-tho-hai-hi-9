from discord.ext import commands
import discord
from discord import Option
import yaml
import requests

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

products = ['Nitro Links', '1m Nitro Tokens', '3m Nitro Tokens']

class Restockalert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Sends out an embed to restock channel.', name='restocksalert')
    async def restockalert(self, interaction: discord.Interaction, product: Option(str, "Product that you want to restock alert", choices=products, required=True), stock: discord.Option(str, "How much many goods are you restocking", required=True), price: discord.Option(str, "Whats the price per good.", required=True),  autobuylink: discord.Option(str, "Auto buy url (link to your sellix/sellapp/sellpass product)", required=True)):
        if not (str(interaction.author.id) in open("whitelist.txt", "r").read().splitlines()) and str(interaction.author.id) != config['bot_owner']:
            embed = discord.Embed(title='Error', description=f'You are not whitelisted to use this command.', color=config['embed_error_color'])
          
            await interaction.respond(embed=embed, ephemeral=True)
        else:
            channel = self.bot.get_channel(int(config['restock_channel']))
            if product == 'Nitro Links':
                embed = discord.Embed(title='Restock alert', description=f'🛒 ~ Product: ``Nitro Links``\n💸 ~ Price: ``${price}/per``\n📦 ~ Stock: ``{stock}``\n💫 ~ Autobuy: [Click here to buy!]({autobuylink})', color=config['embed_color'])

                await interaction.respond(f"Restock alert sent to <#{config['restock_channel']}>", ephemeral=True)
                await channel.send(f"{config['restock_alert_ping']}", embed=embed)
            elif product == '1m Nitro Tokens':
                embed = discord.Embed(title='Restock alert', description=f'🛒 ~ Product: ``1m Nitro Tokens``\n💸 ~ Price: ``${price}/per``\n📦 ~ Stock: ``{stock}``\n💫 ~ Autobuy: [Click here to buy!]({autobuylink})', color=config['embed_color'])

                await interaction.respond(f"Restock alert sent to <#{config['restock_channel']}>", ephemeral=True)
                await channel.send(f"{config['restock_alert_ping']}", embed=embed)
            elif product == '3m Nitro Tokens':
                embed = discord.Embed(title='Restock alert', description=f'🛒 ~ Product: ``3m Nitro Tokens``\n💸 ~ Price: ``${price}/per``\n📦 ~ Stock: ``{stock}``\n💫 ~ Autobuy: [Click here to buy!]({autobuylink})', color=config['embed_color'])

                await interaction.respond(f"Restock alert sent to <#{config['restock_channel']}>", ephemeral=True)
                await channel.send(f"{config['restock_alert_ping']}", embed=embed)

            if config['command_logging'] == True:
                channel = self.bot.get_channel(int(config['command_logs_channel']))
                if product == 'Nitro Links':
                    embed = discord.Embed(title='/restockalert', description=f'Restock alert sent for ``{int(stock)}`` nitro links.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                elif product == '1m Nitro Tokens':
                    embed = discord.Embed(title='/restockalert', description=f'Restock alert sent for ``{int(stock)}`` 1m nitro tokens.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                elif product == '3m Nitro Tokens':
                    embed = discord.Embed(title='/restockalert', description=f'Restock alert sent for ``{int(stock)}`` 3m nitro tokens.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}") 
                await channel.send(embed=embed)