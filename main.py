import discord
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
nickname_queue = []

@bot.event
async def on_ready():
    print(f'Bot online: {bot.user.name}')
    update_nicknames.start()

@tasks.loop(seconds=60)
async def update_nicknames():
    if nickname_queue:
        guild_id = Your_discord_server_id
        guild = bot.get_guild(guild_id)

        member = nickname_queue.pop(0)
        highest_role = max(member.roles, key=lambda r: r.position)
        new_nickname = f'{member.name}[{highest_role.name}]'

        print(f"Modifica del nickname per {member.name} a {new_nickname}")

        try:
            await member.edit(nick=new_nickname)
            print(f"Nickname modificato con successo per {member.name}")
        except discord.Forbidden:
            print(f"Non posso modificare il nickname di {member.name}. Controlla i permessi.")
        except discord.HTTPException as e:
            print(f"Errore HTTP durante l'aggiornamento del nickname di {member.name}: {e}")

@bot.command()
async def start(ctx):
    guild_id = 977243549953323068
    guild = bot.get_guild(guild_id)

    # Aggiungi alla coda solo i membri con ruoli
    for member in guild.members:
        if member.roles:
            nickname_queue.append(member)

    print(f"Coda dei nickname: {[member.name for member in nickname_queue]}")

    update_nicknames.start()
    print('Aggiornamento nickname avviato!')
    await ctx.send('Aggiornamento nickname avviato!')

@bot.command()
async def stop(ctx):
    update_nicknames.stop()
    await ctx.send('Aggiornamento nickname fermato!')

bot.run('Your_token')
