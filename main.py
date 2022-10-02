import discord
from discord.ext import commands
from discord_slash import ButtonStyle
from discord_slash.utils.manage_components import *

token = "MTAyNjE5MzA3MTE2MDk1NDk4NA.Ggcw4x.FkOOqF_pnfgJg5rshtr3M1bKq4QdlVc-PYviA0"
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", description="Description à venir", intents=intents)

########################################################################################################################


@bot.event
async def on_ready():
    print("Ready to serve !")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    else:
        triggerList = ["Yo","Salut","Bonjour","Hello"]
        answerList = ["Yo mon pote","Salut mon pote","Bonjour mon pote","Hello mon pote"]
        if message.content in triggerList:
            index=0
            while message.content != triggerList[index]:
                index+=1
            await message.channel.send(answerList[index])
        else:
            pass
    await bot.process_commands(message)


########################################################################################################################


@bot.command()
async def hello(ctx):
    await ctx.send("Hello there !")


@bot.command()
async def clear(ctx, amount: int):
    msgs = [message async for message in ctx.channel.history(limit = amount+1)] #await not possible because cannot flatten async_generator
    for msg in msgs:
        await msg.delete()


@bot.command()
async def temp(ctx):
    await ctx.send("temp cmd to keep emoji reaction reaction to msg")

    def msgCheck(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    try:
        msgAnswer = await bot.wait_for("message", timeout = 10, check = msgCheck)
    except:
        await ctx.send("Faute de réponse, la procédure a été interrompue par timeout.")

    userCheck = await ctx.send(f"Votre réponse était {msgAnswer.content}, confirmez vous ?")
    await userCheck.add_reaction("✅")
    await userCheck.add_reaction("❎")

    def reactCheck(reaction, user):
        return ctx.message.author == user and userCheck.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❎")
    try:
        reactAnswer, user = await bot.wait_for("reaction_add", timeout = 10, check = reactCheck)
        if reactAnswer.emoji == ("❎"):
            await ctx.send("Vous avez annulé la sélection")
        else:
            await ctx.send("Votre confirmation a été prise en compte")
    except:
        await ctx.send("Une erreur est survenue, votre choix n'a pas pu être pris en compte")


########################################################################################################################


@bot.command()
async def create(ctx, asso, *projectTitle):
    listTitle = ' '.join(projectTitle)
    assoText = ' '.join(asso)
    embed = discord.Embed(title = listTitle, description = 'toDoNotes\n\n', colour=0xff6500)
    embed.set_author(name = ctx.author.name)

    embed.add_field(name = 'Tâche à faire numéro 1', value = 'Tâche à faire effectivement', inline = True)

    embed.set_footer(text = assoText)
    await ctx.send(embed = embed)


@bot.command()
async def lists(ctx):
    buttons = [
        create_button(
            style = ButtonStyle.blue,
            label = "<<",
            custom_id = "précédent",
        ),
        create_button(
            style=ButtonStyle.danger,
            label="Quitter",
            custom_id="non",
        ),
        create_button(
            style = ButtonStyle.blue,
            label = ">>",
            custom_id = "suivant",
        )
    ]
    action_row = create_actionrow(*buttons)
    userAction = await ctx.send("Voilà les différentes listes de choses à faire", components=[action_row])










# @bot.command()
# async def test(ctx, *, listtitle):
#     embed = discord.Embed(title = listtitle,  )
#
#     await ctx.send(args)



bot.run(token)
