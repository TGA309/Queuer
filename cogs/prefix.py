import asyncpg
from discord.ext import commands
import os

class prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['prefix'])
    @commands.has_permissions(administrator=True)
    async def changeprefix_(self, ctx, prefix):

        DATABASE_URL = os.environ['DATABASE_URL']

        conn = await asyncpg.connect(DATABASE_URL, ssl = 'require')

        if len(prefix) > 1:
            prel = prefix[0]

            gid = ctx.guild.id
    
            pre = await conn.fetch("SELECT prefix FROM serverprefixes WHERE id = $1", gid)

            if pre:
                await conn.execute("UPDATE serverprefixes SET prefix = $1 WHERE id = $2", prel, gid)
                await ctx.message.reply(f'Since the prefix of the bot can only be one character long, it has been updated to `{prel}`', mention_author = False)

        else:

            gid = ctx.guild.id
    
            pre = await conn.fetch("SELECT prefix FROM serverprefixes WHERE id = $1", gid)

            if pre:
                await conn.execute("UPDATE serverprefixes SET prefix = $1 WHERE id = $2", prefix, gid)
                await ctx.message.reply(f'The prefix of this server has been updated to `{prefix}`', mention_author =  False)

        await conn.close()

def setup(bot):
    bot.add_cog(prefix(bot))