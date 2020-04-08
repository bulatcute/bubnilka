import os
import discord
from dotenv import load_dotenv
import random
from google.cloud import texttospeech
import asyncio

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
        
        ttsclient = texttospeech.TextToSpeechClient()

        voice = texttospeech.types.VoiceSelectionParams(
            language_code='ru-RU',
            name='ru-RU-Standard-B',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            pitch=-3.2)

        synthesis_input = texttospeech.types.SynthesisInput(text=f"{member.display_name} залетел")

        response = ttsclient.synthesize_speech(synthesis_input, voice, audio_config)

        with open('output.mp3', 'wb') as out:
            out.write(response.audio_content)
        vc = await channel.connect()
        print(vc.is_connected())

        vc.play(discord.FFmpegPCMAudio(executable='D:/Downloads/ffmpeg-20200403-52523b6-win64-static/bin/ffmpeg.exe', source='output.mp3'), after=lambda e: print('done', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()
        print(member.display_name, 'зашел')
        await vc.disconnect()

    elif before.channel and not after.channel:
        channel = before.channel
        
        ttsclient = texttospeech.TextToSpeechClient()

        voice = texttospeech.types.VoiceSelectionParams(
            language_code='ru-RU',
            name='ru-RU-Standard-B',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            pitch=-3.2)

        synthesis_input = texttospeech.types.SynthesisInput(text=f"{member.display_name} вылетел")

        response = ttsclient.synthesize_speech(synthesis_input, voice, audio_config)

        with open('output.mp3', 'wb') as out:
            out.write(response.audio_content)
        vc = await channel.connect()
        print(vc.is_connected())

        vc.play(discord.FFmpegPCMAudio(executable='D:/Downloads/ffmpeg-20200403-52523b6-win64-static/bin/ffmpeg.exe', source='output.mp3'), after=lambda e: print('done', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        vc.stop()
        print(member.display_name, 'вышел')
        await vc.disconnect()
        

client.run(TOKEN)
