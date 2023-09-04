import discord
from discord.ext import commands
import yaml
import time
import sys
import time
import os
import hashlib
from datetime import datetime

from commands.stock import *
from commands.restock import *
from commands.whitelist import *
from commands.check import *
from commands.restockalert import *
from commands.payments import *
from commands.help import *
from commands.drop import *

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

class Colors:
    GREEN = "\033[38;5;120m"
    ORANGE = "\033[38;5;220m"
    RED = "\033[38;5;203m"
    RESET = "\033[38;5;231m"
    GRAY = "\033[38;5;242m"

def timestamp():
    timestamp = f"{Colors.RESET}{Colors.GRAY}{datetime.now().strftime('%H:%M:%S')}{Colors.RESET}"
    return timestamp

activity = discord.Activity(type=discord.ActivityType.playing, name=config['bot_status'])
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, activity=activity, status=discord.Status.online, debug=True)

@bot.event
async def on_ready():
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Your bot is ready {Colors.GRAY}bot-user={Colors.RESET}{bot.user}')

def run_bot():
    bot.add_cog(Stock(bot))
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Successfully synced command {Colors.GRAY}command={Colors.RESET}/stock')
    time.sleep(0.1)
    bot.add_cog(Restock(bot))
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Successfully synced command {Colors.GRAY}command={Colors.RESET}/restock')
    time.sleep(0.1)
    bot.add_cog(Whitelist(bot))
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Successfully synced command {Colors.GRAY}command={Colors.RESET}/whitelist')
    time.sleep(0.1)
    bot.add_cog(Check(bot))
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Successfully synced command {Colors.GRAY}command={Colors.RESET}/check')
    time.sleep(0.1)
    bot.add_cog(Restockalert(bot))
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Successfully synced command {Colors.GRAY}command={Colors.RESET}/restockalert')
    time.sleep(0.1)
    bot.add_cog(Payments(bot))
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Successfully synced command {Colors.GRAY}command={Colors.RESET}/payments')
    time.sleep(0.1)
    bot.add_cog(Help(bot))
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Successfully synced command {Colors.GRAY}command={Colors.RESET}/help')
    time.sleep(0.1)
    bot.add_cog(Drop(bot))
    print(f'{timestamp()} {Colors.GREEN}INF {Colors.GRAY}> {Colors.RESET}Successfully synced command {Colors.GRAY}command={Colors.RESET}/drop')
    bot.run(config['bot_token'])

run_bot()