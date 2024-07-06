import discord
from discord.ext import commands
from discord import Member
import random
import json
from tokens import *
person= FRIENDS_LIST
dumb_words=['lol','rofl','lmao']
kicks=["kick.gif","kick1.gif","kick2.gif","kick3.gif","kick4.gif","kick5.gif","kick6.gif"]
pokes=["poke.gif","poke1.gif","poke2.gif","poke3.gif"]
slaps=["slap.gif","slap1.gif","slap2.gif","slap3.gif","slap4.gif","slap5.gif"]
punches=["punch1.gif","punch2.gif","punch3.gif","punch4.gif"]


class actions(commands.Cog):
    def __init__(self,client:commands.Bot):
            self.client=client


    #ACTION: KICK-----------------------------------------------
    @commands.command()
    async def kick(self,ctx,*,member:discord.Member):

#----------- CHECKING IF COMMAND IS DISABLED -----------------------------------------------------------------
        with open('channel_ids.json', 'r') as f:
            ids_list = json.load(f)
        disabled_commands = {g_id: ids_list[g_id].get("dis_command") for g_id in ids_list if"dis_command" in ids_list[g_id]}
        if "kick" in disabled_commands[str(ctx.guild.id)]:
            return
        
#-------------------------------------------------------------------------------------------------------

        img=str(random.choice(kicks))
        await ctx.send(file=discord.File(img))
        if(img=="kick6.gif"):
            await ctx.send("oopsie, bro completely missed it")
        else:
            await ctx.send(f" take that <@{member.id}>")

    #ACTION: PUNCH-----------------------------------------
    @commands.command()
    async def punch(self,ctx,*,member:discord.Member):

#----------- CHECKING IF COMMAND IS DISABLED -----------------------------------------------------------------
        with open('channel_ids.json', 'r') as f:
            ids_list = json.load(f)
        disabled_commands = {g_id: ids_list[g_id].get("dis_command") for g_id in ids_list if"dis_command" in ids_list[g_id]}
        if "punch" in disabled_commands[str(ctx.guild.id)]:
            return
        
#-------------------------------------------------------------------------------------------------------

        img=str(random.choice(punches))
        await ctx.send(file=discord.File(img))
        if(img=="punch4.gif"):
            await ctx.send("ouch, bro completely missed it")
        else:
            await ctx.send(f" take that <@{member.id}>")

    #ACTION: SLAP-------------------------------------------------
    @commands.command()
    async def slap(self,ctx,*,member:discord.Member):

#----------- CHECKING IF COMMAND IS DISABLED -----------------------------------------------------------------
        with open('channel_ids.json', 'r') as f:
            ids_list = json.load(f)
        disabled_commands = {g_id: ids_list[g_id].get("dis_command") for g_id in ids_list if"dis_command" in ids_list[g_id]}
        if "slap" in disabled_commands[str(ctx.guild.id)]:
            return
        
#-------------------------------------------------------------------------------------------------------

        img=str(random.choice(slaps))
        await ctx.send(file=discord.File(img))
        if(img=="slap5.gif"):
            await ctx.send("oopsie, bro completely missed it")
        else:
            await ctx.send(f" take that >:( <@{member.id}>")

    #ACTION: POKE--------------------------------------------------
    @commands.command()
    async def poke(self,ctx,*,member:discord.Member):

#----------- CHECKING IF COMMAND IS DISABLED -----------------------------------------------------------------
        with open('channel_ids.json', 'r') as f:
            ids_list = json.load(f)
        disabled_commands = {g_id: ids_list[g_id].get("dis_command") for g_id in ids_list if"dis_command" in ids_list[g_id]}
        if "kick" in disabled_commands[str(ctx.guild.id)]:
            return
        
#-------------------------------------------------------------------------------------------------------

        img=str(random.choice(pokes))
        await ctx.send(file=discord.File(img))
        if(img=="poke3.gif"):
            await ctx.send("uh oh, should not have poked")
async def setup(client:commands.Bot):
    await client.add_cog(actions(client))