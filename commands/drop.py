from discord.ext import commands
import discord
from discord import Option
import yaml
import os

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

products = ['Nitro Links', '1m Nitro Tokens', '3m Nitro Tokens']

class Drop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Drop goods to user's dm", name='drop')
    async def drop(self, interaction: discord.Interaction, product: Option(str, "Product that you want to restock alert", choices=products, required=True), amount: Option(int, "How many good's do you want to drop to the user.", required=True), user: discord.User):
        if not (str(interaction.author.id) in open("whitelist.txt", "r").read().splitlines()) and str(interaction.author.id) != config['bot_owner']:
            embed = discord.Embed(title='Error', description=f'You are not whitelisted to use this command.', color=config['embed_error_color'])
            await interaction.respond(embed=embed, ephemeral=True)
        else:
            channel = self.bot.get_channel(int(config['restock_channel']))
            if product == 'Nitro Links':
                with open(config['nitro_links_file'], "r+") as f:
                    nitro_list = f.readlines()
                    if len(nitro_list) < int(amount):
                        embed = discord.Embed(title='Error', description=f'You do not have that many nitro gift links in stock.', color=config['embed_error_color'])
                        await interaction.respond(embed=embed, ephemeral=True)
                        return
                    
                nitro_send_list = nitro_list[:amount]; f.seek(0); f.truncate();f.writelines(nitro_list[amount:])
                dm_channel = await user.create_dm()
                nitro_send_list = [link.strip() for link in nitro_send_list]
                nitro_send_message = "\n".join(nitro_send_list)

                with open('output.txt', 'w') as file:
                    file.write(nitro_send_message)

                with open(f'output.txt', 'rb') as file:
                    embed = discord.Embed(title='Drop', description=f'{interaction.author.mention} sent you ``{amount}`` nitro gift links', color=config['embed_color'])
                    await dm_channel.send(embed=embed); await dm_channel.send(file=discord.File(file))

                os.remove('output.txt')

                embed = discord.Embed(title='Success', description=f'Successfully sent {amount} nitro gift links to {user.mention}', color=config['embed_color'])
                await interaction.respond(embed=embed)
            elif product == '1m Nitro Tokens':
                with open(config['nitro_tokens_1m_file'], "r+") as f:
                    nitro_tokens_list = f.readlines()
                    if len(nitro_tokens_list) < int(amount):
                        embed = discord.Embed(title='Error', description=f'You do not have that many 1m nitro tokens in stock.', color=config['embed_error_color'])
                        await interaction.respond(embed=embed, ephemeral=True)
                        return
                    
                nitro_tokens_send_list = nitro_tokens_list[:amount]; f.seek(0); f.truncate();f.writelines(nitro_tokens_list[amount:])
                dm_channel = await user.create_dm()
                nitro_tokens_send_list = [link.strip() for link in nitro_tokens_send_list]
                nitro_tokens_send_message = "\n".join(nitro_tokens_send_list)

                with open('output.txt', 'w') as file:
                    file.write(nitro_tokens_send_message)

                with open(f'output.txt', 'rb') as file:
                    embed = discord.Embed(title='Drop', description=f'{interaction.author.mention} sent you ``{amount}`` 1m nitro tokens', color=config['embed_color'])
                    await dm_channel.send(embed=embed); await dm_channel.send(file=discord.File(file))

                os.remove('output.txt')

                embed = discord.Embed(title='Success', description=f'Successfully sent {amount} 1m nitro tokens to {user.mention}', color=config['embed_color'])
                await interaction.respond(embed=embed)
            elif product == '3m Nitro Tokens':
                with open(config['nitro_tokens_3m_file'], "r+") as f:
                    nitro_tokens_list = f.readlines()
                    if len(nitro_tokens_list) < int(amount):
                        embed = discord.Embed(title='Error', description=f'You do not have that many 3m nitro tokens in stock.', color=config['embed_error_color'])
                        await interaction.respond(embed=embed, ephemeral=True)
                        return
                    
                nitro_tokens_send_list = nitro_tokens_list[:amount]; f.seek(0); f.truncate();f.writelines(nitro_tokens_list[amount:])
                dm_channel = await user.create_dm()
                nitro_tokens_send_list = [link.strip() for link in nitro_tokens_send_list]
                nitro_tokens_send_message = "\n".join(nitro_tokens_send_list)

                with open('output.txt', 'w') as file:
                    file.write(nitro_tokens_send_message)

                with open(f'output.txt', 'rb') as file:
                    embed = discord.Embed(title='Drop', description=f'{interaction.author.mention} sent you ``{amount}`` 3m nitro tokens', color=config['embed_color'])
                    await dm_channel.send(embed=embed); await dm_channel.send(file=discord.File(file))

                os.remove('output.txt')

                embed = discord.Embed(title='Success', description=f'Successfully sent {amount} 3m nitro tokens to {user.mention}', color=config['embed_color'])
                await interaction.respond(embed=embed)

            if config['command_logging'] == True:
                channel = self.bot.get_channel(int(config['command_logs_channel']))
                if product == 'Nitro Links':
                    embed = discord.Embed(title='/drop', description=f'Sent {amount} nitro gift links to {user.mention}', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                elif product == '1m Nitro Tokens':
                    embed = discord.Embed(title='/drop', description=f'Sent {amount} 1m nitro tokens to {user.mention}', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                elif product == '3m Nitro Tokens':
                    embed = discord.Embed(title='/drop', description=f'Sent {amount} 3m nitro tokens to {user.mention}', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                await channel.send(embed=embed)