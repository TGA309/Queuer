import discord
import discord.colour
from discord.ext import commands, tasks
from secrets import randbelow
import os
import asyncpg
import re

intents = discord.Intents.default()
intents.members = True

class StringToBinary():

    def string_binary(ctx, arg):
        s1 = arg
        s2 = re.sub(re.compile(r'\s+'), '', s1)
        arr1 = []

        for i in s2:
            arr1.append(bin(ord(i))[2:].zfill(8))

        s2 =' '.join(map(str, arr1))
        return s2

StringToBinary_obj = StringToBinary()

# Prefixes

async def get_prefix(bot, message):

    DATABASE_URL = os.environ['DATABASE_URL']

    conn = await asyncpg.connect(DATABASE_URL, ssl = 'require')

    gid = message.guild.id

    prefix = await conn.fetch("SELECT prefix FROM serverprefixes WHERE id = $1", gid)

    pr = str(prefix)
    pr2 = pr[17]

    await conn.close()
    return pr2

bot = commands.Bot(command_prefix = get_prefix, intents=intents)

@bot.event
async def on_message(msg):

    if msg.guild is None:
        if isinstance(msg.channel, discord.channel.DMChannel) and msg.author != bot.user:
            await msg.channel.send("Commands do not work in DMs.")

    else:
        try:
            if bot.user.mentioned_in(msg):

                gid = msg.guild.id

                DATABASE_URL = os.environ['DATABASE_URL']

                conn = await asyncpg.connect(DATABASE_URL, ssl = 'require')

                prefix = await conn.fetch("SELECT prefix FROM serverprefixes WHERE id = $1", gid)

                pr = str(prefix)
                pr2 = pr[17]

                await conn.close()

                if prefix:
                    await msg.reply(f"My prefix for this server is `{pr2}`", mention_author = False)


        except:
            pass
        await bot.process_commands(msg)

@bot.event
async def on_guild_join(guild):

    gid = guild.id

    DATABASE_URL = os.environ['DATABASE_URL']

    conn = await asyncpg.connect(DATABASE_URL, ssl = 'require')

    await conn.execute("DELETE FROM serverprefixes WHERE id = $1", gid)
    await conn.execute("INSERT INTO serverprefixes (id, prefix) VALUES ($1, '~')", gid)

    await conn.close()
    
    for channel in guild.text_channels:
        
        if channel.permissions_for(guild.me).send_messages:
            
            await channel.send('Hey there! Type `~help` to get started with the bot.')
            
        break

@bot.event
async def on_guild_remove(guild):

    gid = guild.id

    DATABASE_URL = os.environ['DATABASE_URL']

    conn = await asyncpg.connect(DATABASE_URL, ssl = 'require')

    await conn.execute("DELETE FROM serverprefixes WHERE id = $1", gid)

    await conn.close()

@bot.command(name = 'StringToBinary', aliases=['stb'], description="Converts the given string into binary.")
async def stb_(ctx, *, arg):
    """Converts the given string into binary."""
    await ctx.send (StringToBinary_obj.string_binary(arg))

# Loading Cogs
@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    """Command to load cogs.
    
       Need administrative permissions to use.   
    """
    bot.load_extension(f'cogs.{extension}')
    print ("Loaded Cogs")


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    """Command to unload cogs.
    
       Need administrative permissions to use.   
    """
    bot.unload_extension(f'cogs.{extension}')
    print ("Unoaded Cogs")

@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    """Command to reload cogs.
    
       Need administrative permissions to use.   
    """
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    print ("Reloaded Cogs")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print('I have logged in as {0.user}'.format(bot))
    ch_pr.start()

# Status Change
@tasks.loop(seconds = 15)
async def ch_pr():

    statuses = ["Do not watch!!", "ඞ Amogus Drip ඞ", "ඞ sUssy Drip ඞ", "ඞ sUs t0wn ඞ", "Pls don't watch!", "Idek at this point..", "monke!!!!!", "O̶͊̽m̷̾͌ơ̷̑s̸͒̕h̶͙̄ȋ̷̊r̶̄́ỏ̵̓i̵̔̅.̶͂̏.̴̛̾.̶͌̌.̴͒̚"]

    urls = [f"https://www.youtube.com/watch?v=dQw4w9WgXcQ", f"https://www.youtube.com/watch?v=T59N3DPrvac", f"https://www.youtube.com/watch?v=8-NcrRzH0vA", f"https://www.youtube.com/watch?v=CK69zfhGtE8", f"https://www.youtube.com/watch?v=fC7oUOUEEi4", f"https://www.youtube.com/watch?v=OL52lvx5P9I", f"https://www.youtube.com/watch?v=qQhfjqMa6pg", f"https://www.youtube.com/watch?v=UJd8a9fxncE"]

    index = randbelow(8)

    statuspr = statuses[index]
    urlpr = urls[index]

    await bot.change_presence(activity = discord.Streaming(name = statuspr, url = urlpr, platform = "YouTube"))

bot.run('<YourBotToken>')
