import os
import re
import discord

from dotenv import load_dotenv
from extractor import get_rune, get_emoji

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guild_typing = True
intents.guild_reactions = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Ya funco bien")

def get_champion_name(message):
    content:str = message.content
    lista_partida = content.split(" ", maxsplit=1)
    if re.match(r'^\w+ \w+$', lista_partida[-1]) or re.match(r"'.*'", lista_partida[-1]):
        lista_partida[-1] = lista_partida[-1].replace(" ", "").replace("'", "")
    return lista_partida.pop(-1)

def test_comand(message):
    return f"Estoy de 10, gracias. {get_emoji('Okay')}"

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!rune'):
        if message.content.strip() == "!rune":
            await message.channel.send(f"Por favor ingrese un nombre de campeón válido. {get_emoji('NowSeeHere')}")
        else:
            champion_name = get_champion_name(message)
            runes = get_rune(champion_name)
            if runes is not None:
                await message.channel.send(runes)
            else:
                await message.channel.send(f"No pudimos encontrar las runas que solicitaste, por favor revisa que el nombre este bien escrito. {get_emoji('BeeSad')}")

    if message.content.startswith("!test"):
        ok = test_comand(message)
        await message.channel.send(ok)

TOKEN = os.environ.get("DISCORD_TOKEN")
client.run(TOKEN)
