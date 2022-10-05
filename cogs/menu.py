import discord
from discord.ui import select, View
from discord.ext import commands
import Database_Model as dbc


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=100):
        super().__init__(timeout=timeout)

    @discord.ui.button(label = "Create", style = discord.ButtonStyle.blurple)
    async def createBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('creating a new list ...')

    @discord.ui.button(label = "Quit", style = discord.ButtonStyle.danger)
    async def quitBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()


class Menuu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Menu cog loaded')

    @commands.command()
    async def menu(self, ctx, asso, *projectTitle):
        listTitle = ' '.join(projectTitle)
        assoText = ' '.join(asso)

        em = discord.Embed(title = 'neondzedn', description = 'toDoNotes\n\n', colour=0xff6500)
        em.set_author(name = ctx.author.name)

        em.add_field(name = 'Association', value = 'Tâche à faire effectivement', inline = True)

        em.set_footer(text = assoText)
        await ctx.send(embed = em, view = Buttons())


class selectAssoMenu(View):

    @discord.ui.select(
        placeholder = 'Choisis une asso',
        options=[
            discord.SelectOption(label="Fabr'Icam", value="1"),
            discord.SelectOption(label="Cod'Icam", value="2"),
            discord.SelectOption(label="Styl'Icam", value="3"),
            discord.SelectOption(label="Robot'Icam", value="4"),
        ]
    )

    async def select_callback(self, select, interaction):
        select.disabled = True
        match select.values[0]:
            case "1":
                lists = dbc.fetchLists("Fabricam")
                await interaction.response.send_message('sded')
            case "2":
                lists = dbc.fetchLists("Codicam")
            case"3":
                lists = dbc.fetchLists("Stylicam")
            case"4":
                lists = dbc.fetchLists("Roboticam")


class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Drop down menu cog loaded")

    @commands.command()
    async def select(self, ctx):
        await ctx.send("Choisis l'asso dont tu veux voir les listes", view = selectAssoMenu())


async def setup(bot):
    await bot.add_cog(Menu(bot))
