from discord.ext import commands
import discord
from discord import Option
import yaml
import os
import requests
from datetime import datetime, timezone
import concurrent.futures

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

check_options = ['Nitro Links']

checked_nitros = []
valid_nitros = []
boost_nitros = 0
basic_nitros = 0
classic_nitros = 0
invalid_nitros = 0
used_nitros = 0
unchecked_nitros = 0

def reset(type):
    global checked_nitros
    global valid_nitros
    global boost_nitros
    global basic_nitros
    global classic_nitros
    global invalid_nitros
    global used_nitros
    global unchecked_nitros

    if type == 'Nitro Links':
        checked_nitros = []
        valid_nitros = []
        boost_nitros = 0
        basic_nitros = 0
        classic_nitros = 0
        invalid_nitros = 0
        used_nitros = 0
        unchecked_nitros = 0

def nitro_checker(session, nitrolink):
    try:
        global checked_nitros
        global valid_nitros
        global boost_nitros
        global basic_nitros
        global classic_nitros
        global invalid_nitros
        global used_nitros
        global unchecked_nitros

        with open(config['proxies_file'], 'r') as file:
            proxy = file.readline()

        proxies = {'https': f'http://{proxy}', 'http': f'http://{proxy}'}
        nitrocode = nitrolink.split("/")[-1]
        response = session.get(f"https://discord.com/api/v9/entitlements/gift-codes/{nitrocode}?with_application=false&with_subscription_plan=true", proxies=proxies)
        data = response.json()

        if response.status_code == 404:
            checked_nitros.append(f"{nitrolink} | Invalid")
            invalid_nitros += 1
        elif "uses" in data:
            redeemed = data['uses']
            if redeemed == 1:
                checked_nitros.append(f"{nitrolink} | Alredy redeemed")
                used_nitros += 1
            elif redeemed == 0:
                if data["store_listing"]["sku"]["name"] == 'Nitro':
                    expires = data['expires_at']; current_datetime = datetime.now(timezone.utc); expires_datetime = datetime.fromisoformat(expires).astimezone(timezone.utc); timeleft = round((expires_datetime - current_datetime).total_seconds() / 3600)
                    checked_nitros.append(f"{nitrolink} | Nitro Boost | {timeleft}h Left"); boost_nitros += 1; valid_nitros.append(f"{nitrolink}")
                
                elif data["store_listing"]["sku"]["name"] == 'Nitro Basic':
                    expires = data['expires_at']; current_datetime = datetime.now(timezone.utc); expires_datetime = datetime.fromisoformat(expires).astimezone(timezone.utc); timeleft = round((expires_datetime - current_datetime).total_seconds() / 3600)
                    checked_nitros.append(f"{nitrolink} | Nitro Basic | {timeleft}h Left"); basic_nitros += 1; valid_nitros.append(f"{nitrolink}")
                
                elif data["store_listing"]["sku"]["name"] == 'Nitro Classic':
                    expires = data['expires_at']; current_datetime = datetime.now(timezone.utc); expires_datetime = datetime.fromisoformat(expires).astimezone(timezone.utc); timeleft = round((expires_datetime - current_datetime).total_seconds() / 3600)

                    checked_nitros.append(f"{nitrolink} | Nitro Classic | {timeleft}h Left"); classic_nitros += 1; valid_nitros.append(f"{nitrolink}")
                else:
                    checked_nitros.append(f"{nitrolink} | Unknown"); unchecked_nitros += 1

        elif response.status_code == 429:
            checked_nitros.append(f"{nitrolink} | Unchecked | Proxy ratelimited")
            unchecked_nitros += 1
            return False
        else:
            checked_nitros.append(f"{nitrolink} | Unchecked | Unknown")
            unchecked_nitros += 1
            return False

        return True
    except:
        checked_nitros.append(f"{nitrolink} | Unchecked | Proxy fail")
        unchecked_nitros += 1
        return False

class Check(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Check Nitro Tkns/Nitro Links', name='check')
    async def whitelist(self, interaction: discord.Interaction, type: Option(str, "Product that you want to check", choices=check_options, required=True)):
        await interaction.response.defer()
        if not (str(interaction.author.id) in open("whitelist.txt", "r").read().splitlines()) and str(interaction.author.id) != config['bot_owner']:
            embed = discord.Embed(title='Error', description=f'You are not whitelisted to use this command.', color=config['embed_error_color'])
          
            await interaction.response.send_message(embed=embed)
        else:
            if os.path.getsize(config['proxies_file']) == 0:
                embed = discord.Embed(title='Error', description=f'Proxies are required to run this command. ``{config["proxies_file"]}`` is empty.', color=config['embed_error_color'])
          
                await interaction.response.send_message(embed=embed)
            else:
                with open(config['proxies_file'], 'r') as file:
                    proxy = file.readline()
            
                try:
                    response = requests.get('https://google.com', proxies={'https': f'http://{proxy}', 'http': f'http://{proxy}'})
                except:
                    embed = discord.Embed(title='Error', description=f'Proxy failed, retry using command.', color=config['embed_error_color'])
          
                    await interaction.response.send_message(embed=embed)
                    return
                
                if response.status_code == 200:
                    if type == 'Nitro Links':
                        reset('Nitro Links')

                        embed = discord.Embed(description=f'Checking nitro nitro links, please wait.', color=config['embed_color'])
            
                        msg = await interaction.followup.send(embed=embed)

                        links = open(config['nitro_links_file'], "r").readlines()
                        links = [link.rstrip() for link in links]
                        num_threads = config['threads']
                        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
                            futures = []
                            start = datetime.now()
                            session = requests.Session()
                            for link in links:
                                futures.append(executor.submit(nitro_checker, session, link))
                            for future in concurrent.futures.as_completed(futures):
                                future.result()
                            session.close()
                        end = datetime.now()
                        elapsed = round((end - start).total_seconds(), 7)
                            
                        embed = discord.Embed(title='Success', description=f'Successfully checked ``{len(links)}`` nitro nitro links in ``{elapsed}s``', color=config['embed_color']); embed.set_footer(text="Saved only valid nitros to your stock.")
                        embed.add_field(name="Nitro Boost", value=f"``{boost_nitros}``", inline=True)
                        embed.add_field(name="Nitro Basic", value=f"``{basic_nitros}``", inline=True)
                        embed.add_field(name="Nitro Classic", value=f"``{classic_nitros}``", inline=True)
                        embed.add_field(name="Invalid Nitro", value=f"``{invalid_nitros}``", inline=True)
                        embed.add_field(name="Used Nitro", value=f"``{used_nitros}``", inline=True)
                        embed.add_field(name="Unchecked Nitro", value=f"``{unchecked_nitros}``", inline=True)

                        nitro_gift_links = '\n'.join(checked_nitros)

                        with open('output.txt', 'w') as file:
                            file.write(nitro_gift_links)

                        await msg.edit(embed=embed)

                        with open(f'output.txt', 'rb') as file:
                            await interaction.send(file=discord.File(file))

                        os.remove('output.txt')

                        with open(config['nitro_links_file'], 'w') as f:
                            for nitro in valid_nitros:
                                f.write(f'{nitro}\n')

                        if config['command_logging'] == True:
                            channel = self.bot.get_channel(int(config['command_logs_channel']))
                            embed = discord.Embed(title='/check', description=f'Successfully checked ``{len(links)}`` nitro gift links.', color=config['embed_color']); embed.set_footer(text=f"Command ran by {interaction.author.name}")
                            await channel.send(embed=embed)

                        reset('Nitro Links')
                            
                else:
                    embed = discord.Embed(title='Error', description=f'Your proxy does not work. Please retry /check command or use different proxy.', color=config['embed_error_color'])
          
                    await interaction.response.send_message(embed=embed)

            
