import discord
from discord.ui import Select, View, select
from discord.ext import commands
import Database_Model as dbc


class selectAssoMenu(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Fabr'Icam", value="1"),
            discord.SelectOption(label="Cod'Icam", value="2"),
            discord.SelectOption(label="Styl'Icam", value="3"),
            discord.SelectOption(label="Robot'Icam", value="4"),
        ]
        super().__init__(placeholder="Choisis ton asso", max_values=1, min_values=1, options = options)

    async def callback(self, interaction: discord.Interaction):
        print(self.values)
        if self.values[0] == "1":
            print("esesfdes")
            await interaction.response.send_message(f'Eh oui, moi aussi je prends')


class selectView(View):
    def __init__(self, *, timeout = 100):
        super().__init__(timeout = timeout)
        self.add_item(selectAssoMenu())


class selectMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Drop down menu cog loaded")

    @commands.command()
    async def select(self, ctx):
        await ctx.send("Choisis l'asso dont tu veux voir les listes", view = selectView())


async def setup(bot):
    await bot.add_cog(selectMenu(bot))