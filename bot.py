import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import random
from google.cloud import texttospeech
import asyncio
import random
import requests


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='$')
queue = asyncio.Queue()


async def player(channel, member, is_bye):
    source = f'{member.id}.mp3'
    if is_bye:
        source = 'bye' + source
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(source=source),
            after=lambda l: vc.stop())
    while vc.is_playing():
        await asyncio.sleep(0.5)
    await vc.disconnect()


async def worker():
    while True:
        r = await queue.get()
        channel = r[0]
        member = r[1]
        is_bye = r[2]
        try:
            await asyncio.wait_for(player(channel, member, is_bye), timeout=5)
        except asyncio.TimeoutError:
            print('time out')
        print('task done')
        queue.task_done()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='на тебя осуждающе'))


@bot.command(name='addall')
async def addall(ctx: commands.Context):
    member = ctx.author
    if member.display_name != 'sony':
        return
    for mmbr in member.guild.members:
        if member == bot.user:
            continue
        ttsclient = texttospeech.TextToSpeechClient()
        if not os.path.isfile(f'{mmbr.id}.mp3'):
            voice = texttospeech.types.VoiceSelectionParams(
                language_code='ru-RU',
                name='ru-RU-Standard-B',
                ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                pitch=1,
                speaking_rate=1.07)

            synthesis_input = texttospeech.types.SynthesisInput(
                text=f'{mmbr.display_name} присоединился')

            response = ttsclient.synthesize_speech(
                synthesis_input, voice, audio_config)

            with open(f'{mmbr.id}.mp3', 'wb') as out:
                out.write(response.audio_content)
            await ctx.send('записано')
        if not os.path.isfile(f'bye{mmbr.id}.mp3'):
            voice = texttospeech.types.VoiceSelectionParams(
                language_code='ru-RU',
                name='ru-RU-Standard-B',
                ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                pitch=1,
                speaking_rate=1.07)
            synthesis_input = texttospeech.types.SynthesisInput(
                text=f'{mmbr.display_name} вышел')

            response = ttsclient.synthesize_speech(
                synthesis_input, voice, audio_config)

            with open(f'bye{mmbr.id}.mp3', 'wb') as out:
                out.write(response.audio_content)
            await ctx.send('записано')


@bot.command('greet')
async def greet(ctx: commands.Context, name, text):
    for role in ctx.author.roles:
        if role.name =='Данжен Мастер':
            break
    else:
        await ctx.send('тебе нельзя')
        return
    message = ctx.message
    member = get(ctx.guild.members, display_name=name)
    if not member:
        await ctx.send('нет такого участника')
    ttsclient = texttospeech.TextToSpeechClient()
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ru-RU',
        name='ru-RU-Standard-B',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        pitch=1,
        speaking_rate=1.07)
    synthesis_input = texttospeech.types.SynthesisInput(
        text=text.replace('~name', member.display_name))
    response = ttsclient.synthesize_speech(
        synthesis_input, voice, audio_config)
    with open(f'{member.id}.mp3', 'wb') as out:
        out.write(response.audio_content)
    await message.add_reaction('👌')


@bot.command('bye')
async def bye(ctx: commands.Context, name, text):
    for role in ctx.author.roles:
        if role.name =='Данжен Мастер':
            break
    else:
        await ctx.send('тебе нельзя')
        return
    message = ctx.message
    member = get(ctx.guild.members, display_name=name)
    if not member:
        await ctx.send('нет такого участника')
    ttsclient = texttospeech.TextToSpeechClient()
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ru-RU',
        name='ru-RU-Standard-B',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        pitch=1,
        speaking_rate=1.07)
    synthesis_input = texttospeech.types.SynthesisInput(
        text=text.replace('~name', member.display_name))
    response = ttsclient.synthesize_speech(
        synthesis_input, voice, audio_config)
    with open(f'bye{member.id}.mp3', 'wb') as out:
        out.write(response.audio_content)
    await message.add_reaction('👌')


@bot.command(name='greetmp3')
async def greetmp3(ctx: commands.Context, name):
    for role in ctx.author.roles:
        if role.name =='Данжен Мастер':
            break
    else:
        await ctx.send('тебе нельзя')
        return
    message = ctx.message
    member = get(ctx.guild.members, display_name=name)
    file_url = ctx.message.attachments[0].url
    r = requests.get(file_url)
    with open(f'{member.id}.mp3', 'wb') as out:
        out.write(r.content)
    await message.add_reaction('👌')



@bot.command(name='byemp3')
async def byemp3(ctx: commands.Context, name):
    for role in ctx.author.roles:
        if role.name =='Данжен Мастер':
            break
    else:
        await ctx.send('тебе нельзя')
        return
    message = ctx.message
    member = get(ctx.guild.members, display_name=name)
    file_url = ctx.message.attachments[0].url
    r = requests.get(file_url)
    with open(f'bye{member.id}.mp3', 'wb') as out:
        out.write(r.content)
    await message.add_reaction('👌')


@bot.command(name='greetme')
async def greetme(ctx: commands.Context):
    member = ctx.author
    message = ctx.message
    ttsclient = texttospeech.TextToSpeechClient()
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ru-RU',
        name='ru-RU-Standard-B',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        pitch=1,
        speaking_rate=1.07)
    synthesis_input = texttospeech.types.SynthesisInput(
        text=f"{' '.join(message.content.split()[1:])}".replace('~name', member.display_name))
    response = ttsclient.synthesize_speech(
        synthesis_input, voice, audio_config)
    with open(f'{member.id}.mp3', 'wb') as out:
        out.write(response.audio_content)
    await message.add_reaction('👌')



@bot.command(name='byeme')
async def byeme(ctx: commands.Context):
    member = ctx.author
    message = ctx.message
    ttsclient = texttospeech.TextToSpeechClient()
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ru-RU',
        name='ru-RU-Standard-B',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        pitch=1,
        speaking_rate=1.07)
    synthesis_input = texttospeech.types.SynthesisInput(
        text=f"{' '.join(message.content.split()[1:])}".replace('~name', member.display_name))
    response = ttsclient.synthesize_speech(
        synthesis_input, voice, audio_config)
    with open(f'bye{member.id}.mp3', 'wb') as out:
        out.write(response.audio_content)
    await message.add_reaction('👌')


@bot.command(name='changelog')
async def changelog(ctx: commands.Context):
    await ctx.message.delete()
    if ctx.author.id != 451290458065338368:
        return
    await ctx.send('> теперь данжен мастеры могут ставить другим свои mp3')


@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return
    elif not before.channel and after.channel:
        channel = after.channel
        if os.path.isfile(f'{member.id}.mp3'):
            await queue.put((channel, member, False))
    elif before.channel and not after.channel:
        channel = before.channel
        if os.path.isfile(f'bye{member.id}.mp3'):
            await queue.put((channel, member, True))
    elif before.channel and after.channel and before.channel != after.channel:
        channel = before.channel
        if os.path.isfile(f'bye{member.id}.mp3'):
            await queue.put((channel, member, True))
        channel = after.channel
        if os.path.isfile(f'{member.id}.mp3'):
            await queue.put((channel, member, False))


bot.loop.create_task(worker())
bot.run(TOKEN)
