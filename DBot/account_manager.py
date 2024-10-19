import json
import os
from typing import Final
import discord
from discord.ext import commands
from discord import app_commands
import asyncio


intents = discord.Intents.default()
intents.message_content = True  
intents.reactions = True
intents.members = True
intents.messages = True 

bot = commands.Bot(command_prefix="!", intents=intents)

def read_data(user, key):
    with open("user_data.json", 'r') as file:
        data = json.load(file)
    print(f"Data for {user}: {data[user]}") 
    return data[user][key]  

def create_account(username):
    if os.path.exists("user_data.json"):
        with open("user_data.json", 'r') as file:
            accounts = json.load(file)
    else:
        accounts = {}

    if username in accounts:
        print("Account exists")
        
    else:
        accounts[username] = {
            "scale": 10.0,
            "matches": 0
        }
        with open("user_data.json", 'w') as file:
            json.dump(accounts, file)
        print("Account created")

def edit_account(user, key, new_data):
    with open("user_data.json", 'r') as file:
        data = json.load(file)
    if user in data:
        if key in data[user]:
            data[user][key] = new_data
            with open("user_data.json", 'w') as file:
                json.dump(data, file, indent=4)
        else:
            print(f"Key '{key}' not found.")
    else:
        print(f"user '{user}' not found.")


def compile_top():
    with open('user_data.json') as file:
        data = json.load(file)
    
    scale_list = [(account_name, account_info['scale']) for account_name, account_info in data.items()]
    scale_list.sort(key=lambda x: x[1], reverse=True)
    return scale_list[:10]  

async def fetch_top_users(guild_id, bot):
    top_10_users = compile_top()
    user = 0

    def ordinal(n):
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return suffix

    output = []
    for index, (account_name, scale) in enumerate(top_10_users, start=1):
        if str(account_name).startswith("<@") and str(account_name).endswith(">") and str(account_name).startswith("<@&") == False:
            user_id = int(account_name[2:-1]) 
            print(user_id)
            try:
                guild = bot.get_guild(guild_id)
                user = guild.get_member(user_id)
                output.append(f"{index}{ordinal(index)}: {user.display_name} | {int(scale * 100) / 100}")
                # if str(account_name).startswith("<@&"):
                #     output.append(f"{index}{ordinal(index)}: User not found | {int(scale * 100) / 100}")
                #     print(f"{account_name} not viable user")
            except Exception as e:
                output.append(f"{index}{ordinal(index)}: User not found | {int(scale * 100) / 100}")
                print(e)
        # else:
        #     output.append(f"{index}{ordinal(index)}: {user} | {int(scale * 100) / 100}")
    return output


# create_account("test1")
# create_account("test2")
# create_account("test3")
# create_account("test4")
# create_account("test5")
# create_account("test6")
# create_account("test7")
# create_account("test8")
# create_account("test9")
# create_account("test10")

