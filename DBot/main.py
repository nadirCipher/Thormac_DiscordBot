from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands
from responses import Match_Input
import asyncio
from responses import Score_finder
from data_manager import compile_top
from discord import *
from data_manager import fetch_top_users

# Load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Bot permission setup
intents = discord.Intents.default()
intents.message_content = True  
intents.reactions = True
intents.members = True
intents.messages = True 

guild_id = 1292586058961129578
GUILD_ID = discord.Object(id=guild_id)

bot = commands.Bot(command_prefix="!", intents=intents)

# Messages
''' i followed a totorial for this lmao
@bot.tree.command(name="hello", description="Say hello", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message("hi there!")

@bot.tree.command(name="printer", description="ill print what ever you say", guild=GUILD_ID)
async def say_hello(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(printer)
'''
@bot.tree.command(name="find_score", description="whos score do ya wana know?")
async def say_hello(interaction: discord.Interaction, user: str):
    await interaction.response.send_message(Score_finder(user))

# @bot.tree.command(name="top_ten", description="prints the top 10 list", guild=GUILD_ID)
# async def top_ten(interaction: discord.Interaction):
#     top_list = str(compile_top()).replace("`","")
#     message = await interaction.response.send_message("...")
#     await message.edit(content=f"{top_list}")
import traceback
@bot.tree.command(name="top_ten", description="prints the top 10 list")
async def top_ten(interaction: discord.Interaction):
    guild = interaction.guild
    print(f"Guild type: {type(guild)}")  # Check the type of guild
    print(f"Guild ID: {guild.id}")

    guild_id = guild.id
    print(guild_id)
    top_list = await fetch_top_users(guild_id, bot) 
    formatted = "\n".join(top_list)
    formatted = "```" + formatted + "```"
    await interaction.response.send_message(formatted, ephemeral=False)

@bot.tree.command(name="input_match", description="Input a match to update your thormac scale!")#, guild=GUILD_ID
async def confirm_match(interaction: discord.Interaction, winner: str, looser: str, match_confirmer: discord.User):
    if winner[2] == "&" and looser[2] == "&" and match_confirmer[2] == "&":
        await interaction.response.send_message("One of those is a role!", ephemeral=True)
        return
    await interaction.response.send_message(
        f"{match_confirmer.mention}, please check your DMs to confirm the match between the winner {winner} and the loser {looser}."
    )

    try:
        confirmation_message = await match_confirmer.send(
            f"{match_confirmer.mention}, type 'yes' to confirm the match between {winner} and {looser}."
        )
        print(f'DM sent to {match_confirmer}!')

        # waits for response
        def check(msg):
            return msg.author.id == match_confirmer.id and isinstance(msg.channel, discord.DMChannel)
        msg = await bot.wait_for('message', timeout=600.0, check=check)
        if msg.content.lower() == "yes":
            result = Match_Input(winner, looser, match_confirmer)
            if isinstance(result, tuple):
                scale_winner, scale_looser, winner, looser = result
                await interaction.followup.send(f"{winner}'s scale: {scale_winner}, {looser}'s scale: {scale_looser}")
            else:
                await interaction.followup.send(result)
        else:
            await interaction.followup.send(f"{match_confirmer.mention}, confirmation not received.")

    except asyncio.TimeoutError:
        await interaction.followup.send(f"{match_confirmer.mention}, you took too long to respond!")
    except discord.Forbidden:
        print(f'I cannot DM {match_confirmer.name}. They might have DMs disabled.')
        await interaction.followup.send(f'I cannot DM {match_confirmer.name}. They might have DMs disabled.')

# Bot start-up
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running v.{discord.__version__}')

    # #This was for testing on one server 
    # try:
    #     GUILD1 = discord.Object(id=1292586058961129578)
    #     GUILD2 = discord.Object(id=1281810739509858374)
    #     synced = await bot.tree.sync(guild=GUILD1)
    #     synced = await bot.tree.sync(guild=GUILD2)
    # except Exception as e:
    #     print(f"Error syncing commands: {e}")

    for guild in bot.guilds:
        print(f'Fetching members for guild: {guild.name} (ID: {guild.id})')

        # Fetch all members in the guild
        async for member in guild.fetch_members(limit=None):
            # Here, the member will be added to the cache automatically
            print(f'Added {member.name} to cache (ID: {member.id})')

# Main entry point
def main() -> None:
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
