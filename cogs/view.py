import discord
from discord.ui import select, View
from discord.ext import commands
import Database_Model as dbc


class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Menu cog loaded')

    @commands.command()
    async def lists(self, ctx, asso):
        asso = [asso]
        em = discord.Embed(title=f'Voici les listes de {str(asso)}\n"<<----------------->>"\n', colour=0xff6500)
        em.set_author(name=ctx.author.name)

        lists = dbc.fetchLists(asso)
        print(lists)
        for eachlist in lists:
            em.add_field(name=f'{str(eachlist[0])}\n', value="-------------------", inline = False)

        em.set_footer(text=str(asso))
        await ctx.send(embed=em, view = view)


async def setup(bot):
    await bot.add_cog(Menu(bot))
