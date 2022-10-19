import discord
import asyncio
import os

from datetime import datetime, timedelta
from discord.ext import commands

import identifier
import Database_Model as dbc

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", description="Description à venir", intents=intents)

########################################################################################################################


@bot.event
async def on_ready():
    print("Ready to serve !")
    await scheduled_reminder()


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


@bot.command()
async def clear(ctx, amount: int):
    msgs = [message async for message in ctx.channel.history(limit = amount+1)] #await not possible because cannot flatten async_generator
    for msg in msgs:
        await msg.delete()


########################################################################################################################


async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')


async def addList(ctx):

    def msgCheck(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    try:
        msgAnswer = await bot.wait_for("message", timeout = 10, check = msgCheck)
    except:
        await ctx.send("Faute de réponse, la procédure a été interrompue par timeout.")

    userCheck = await ctx.send(f"Vous voulez créer la liste : {msgAnswer.content}, confirmez vous ?")
    await userCheck.add_reaction("✅")
    await userCheck.add_reaction("❎")

    def reactCheck(reaction, user):
        return ctx.message.author == user and userCheck.id == reaction.message.id and (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❎")
    try:
        reactAnswer, user = await bot.wait_for("reaction_add", timeout = 20, check = reactCheck)
        if reactAnswer.emoji == ("❎"):
            await ctx.send("Vous avez annulé la création de la liste")
            await ctx.message.delete()
        else:
            await ctx.send("La liste a bien été créée")
            dbc.createList(['codicam'],[msgAnswer.content],[''])
    except:
        await ctx.send("Une erreur est survenue, votre choix n'a pas pu être pris en compte")


async def scheduled_reminder():
    while True:
        now = datetime.now()
        next = now + timedelta(days=7)
        next.replace(hour=10, minute=00)
        waiting_time = (next-now).total_seconds()
        await asyncio.sleep(waiting_time)

        channel = bot.get_channel(767812057243713566)

        await channel.send("Hey @everyone, on est mardi ! Réunion hebdomadaire au Fablab  à 18h !! Venez avancer vos projets "
                           "et discuter !")


########################################################################################################################


# @bot.command()
# async def create(ctx, asso, *projectTitle):
#     listTitle = ' '.join(projectTitle)
#     assoText = ' '.join(asso)
#     embed = discord.Embed(title = listTitle, description = 'toDoNotes\n\n', colour=0xff6500)
#     embed.set_author(name = ctx.author.name)
#
#     embed.add_field(name = 'Tâche à faire numéro 1', value = 'Tâche à faire effectivement', inline = True)
#
#     embed.set_footer(text = assoText)
#     await ctx.send(embed = embed)


# @bot.command()
# async def test(ctx, *, listtitle):
#     embed = discord.Embed(title = listtitle,  )
#
#     await ctx.send(args)

async def exec():
    dbc.createTables()
    await load()
    await bot.start(identifier.token)
asyncio.run(exec())
