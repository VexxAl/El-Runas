import os

import discord
from discord.enums import ContentFilter
from dotenv import load_dotenv

from extractor import get_rune

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print("Ya funco bien")

def get_champion_name(message):
    content:str = message.content
    lista_partida = content.split(" ")
    lista_partida.pop(0)
    lista_partida.pop(-1)
    return " ".join(lista_partida)

def get_line(message):
    content:str = message.content
    return content.split(" ")[-1]

def test_comand(message):
    return "Estoy de 10, gracias. <:BonePlating:921497418787328040>"

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!runa'):
        if message.content.strip() == "!runa":
            await message.channel.send("Por favor ingrese un nombre de campeón válido y su respectiva posición")
        else:
            champion_name = get_champion_name(message)
            line = get_line(message)
            runes = get_rune(champion_name, line)
            if runes is not None:
                await message.channel.send(runes)
            else:
                await message.channel.send("No pudimos encontrar las runas que solicitaste, por favor revisa que el nombre y la linea esten bien escritas.")

    if message.content.startswith("!test"):
        ok = test_comand(message)
        await message.channel.send(ok)
    

#keep_alive()
TOKEN = os.environ.get("DISCORD_TOKEN")
client.run(TOKEN)
