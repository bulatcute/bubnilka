import os
import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    pass


@client.event
async def on_voice_state_update(member, before, after):
    if member == client.user:
        return
    elif not before.channel and after.channel:
        channel = after.channel
        print(len(channel.members))
        if len(channel.members) == 1:
            await channel.connect()
        else:
            print(member.display_name, 'зашел')
    elif before.channel and not after.channel:
        vc = before.channel.guild.voice_client
        channel = before.channel
        print(member.display_name, 'вышел')
        if len(channel.members) == 1:
            await vc.disconnect()

client.run(TOKEN)
