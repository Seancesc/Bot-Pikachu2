import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random

# Setting up intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

# Create bot
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# ======================
# CREATE POKEMON
# ======================
@bot.command()
async def go(ctx):
    author = ctx.author.name

    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)

        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        elif chance == 3:
            pokemon = Fighter(author)

        await ctx.send(await pokemon.info())

        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed(title="Your Pokémon")
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to upload Pokémon image.")
    else:
        await ctx.send("You've already created your own Pokémon.")

# ======================
# ATTACK
# ======================
@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None

    if not target:
        await ctx.send("Mention pengguna yang ingin kamu serang.")
        return

    if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
        attacker = Pokemon.pokemons[ctx.author.name]
        enemy = Pokemon.pokemons[target.name]

        result = await attacker.attack(enemy)
        await ctx.send(result)
    else:
        await ctx.send("Kedua peserta harus memiliki Pokémon.")

# ======================
# INFO
# ======================
@bot.command()
async def info(ctx):
    if ctx.author.name in Pokemon.pokemons:
        pok = Pokemon.pokemons[ctx.author.name]

        await ctx.send(await pok.info())

        image_url = await pok.show_img()
        if image_url:
            embed = discord.Embed(title="Pokémon Info")
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Kamu belum punya Pokémon. Gunakan `!go`.")

# ======================
# START
# ======================
@bot.command()
async def start(ctx):
    await ctx.send(
        "👋 Hi, I am a Pokémon game bot!\n"
        "Commands:\n"
        "`!go` → create Pokémon\n"
        "`!info` → view Pokémon info\n"
        "`!attack @user` → battle"
    )

# Run bot
bot.run(token)

