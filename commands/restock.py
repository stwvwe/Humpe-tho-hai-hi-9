from discord.ext import commands
import discord
from discord import Option
import yaml
import requests

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

products = ['Nitro Links', '1m Nitro Tokens', '3m Nitro Tokens']

class Restock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Restocks nitro tokens/nitro links using paste.ee.', name='restock')
    async def restock(self, interaction: discord.Interaction, product: Option(str, "Product that you want to restock", choices=products, required=True), code: discord.Option(str, "Paste.ee url (Example: https://paste.ee/p/ygWIX)", required=True)):
        if not (str(interaction.author.id) in open("whitelist.txt", "r").read().splitlines()) and str(interaction.author.id) != config['bot_owner']:
            embed = discord.Embed(title='Error', description=f'You are not whitelisted to use this command.', color=config['embed_error_color'])
          
            await interaction.respond(embed=embed, ephemeral=True)
        else:
            if product == 'Nitro Links':
                code = code.replace("https://paste.ee/p/", "")
                headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}; restocked_strings = requests.get(f"https://paste.ee/d/{code}", headers=headers).text
                
                file = config['nitro_links_file']; f = open(file, "a", encoding="utf-8"); f.write(f"{restocked_strings}\n"); f.close()
                restocked_strings_list = restocked_strings.split("\n")
                embed = discord.Embed(title='Stock', description=f'Successfully restocked ``{len(restocked_strings_list)}`` nitro links.', color=config['embed_color'])

                await interaction.respond(embed=embed)
            elif product == '1m Nitro Tokens':
                code = code.replace("https://paste.ee/p/", "")
                headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}; restocked_strings = requests.get(f"https://paste.ee/d/{code}", headers=headers).text
                
                file = config['nitro_tokens_1m_file']; f = open(file, "a", encoding="utf-8"); f.write(f"{restocked_strings}\n"); f.close()
                restocked_strings_list = restocked_strings.split("\n")
                embed = discord.Embed(title='Stock', description=f'Successfully restocked ``{len(restocked_strings_list)}`` 1m nitro tokens.', color=config['embed_color'])

                await interaction.respond(embed=embed)
            elif product == '3m Nitro Tokens':
                code = code.replace("https://paste.ee/p/", "")
                headers={"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}; restocked_strings = requests.get(f"https://paste.ee/d/{code}", headers=headers).text
                
                file = config['nitro_tokens_3m_file']; f = open(file, "a", encoding="utf-8"); f.write(f"{restocked_strings}\n"); f.close()
                restocked_strings_list = restocked_strings.split("\n")
                embed = discord.Embed(title='Stock', description=f'Successfully restocked ``{len(restocked_strings_list)}`` 3m nitro tokens.', color=config['embed_color'])

                await interaction.respond(embed=embed)

            if config['command_logging'] == True:
                channel = self.bot.get_channel(int(config['command_logs_channel']))
                if product == 'Nitro Links':
                    embed = discord.Embed(title='/restock', description=f'Restocked ``{len(restocked_strings_list)}`` nitro links.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                elif product == '1m Nitro Tokens':
                    embed = discord.Embed(title='/restock', description=f'Restocked ``{len(restocked_strings_list)}`` 1m nitro tokens.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                elif product == '3m Nitro Tokens':
                    embed = discord.Embed(title='/restock', description=f'Restocked ``{len(restocked_strings_list)}`` 3m nitro tokens.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}") 
                await channel.send(embed=embed)