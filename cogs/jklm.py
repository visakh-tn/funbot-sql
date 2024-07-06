import discord
from discord.ext import commands
from discord import Member
from tokens import *
from score import scores
from channel_ids import IdClass_new  # DONE
import random
import json
person=['rex','min','mel','homuli','tzu']

class jklm(commands.Cog):
    def __init__(self,client:commands.Bot):
            self.client=client
    # #JKLM ----------------------------------------------
    @commands.command(name='jklm', brief='shows active rooms from jklm.fun', help=''';jklm <language> <game(bp or ps)>.
                    shows only rooms with 3 or more players''')
    async def jklm(self,ctx,args1='ENG',args2='BP'):
#----------- CHECKING IF COMMAND IS DISABLED -----------------------------------------------------------------
        cidc= IdClass_new()
        all_channels = cidc.get_table()
        disabled_commands = {g_data[0]:json.loads(g_data[6]) for g_data in all_channels}
        if "jklm" in disabled_commands[str(ctx.guild.id)]:
            return
        
#-------------------------------------------------------------------------------------------------------
        eng=['ENGLISH','ENG']
        fr=['FRENCH','FR']
        esp=['SPANISH','ESP','ESPANOL']
        bp=['BOMBPARTY','BP']
        ps=['POPSAUCE','PS']
        game=''
        arg1=args1.upper()
        arg2=args2.upper()
        if(arg1 in eng and arg2 in bp):
            game=scores.jklm('ENG','BP')
        elif(arg1 in fr and arg2 in bp):
            game=scores.jklm('FR','BP')
        elif(arg1 in esp and arg2 in bp):
            game=scores.jklm('ESP','BP')
        elif(arg1 in eng and arg2 in ps):
            game=scores.jklm('ENG','PS')
        elif(arg1 in fr and arg2 in ps):
            game=scores.jklm('FR','PS')
        elif(arg1 in esp and arg2 in ps):
            game=scores.jklm("ESP","PS")
        embd=discord.Embed(title="JKLM",url='https://jklm.fun/',colour=0x05D5FA)
        embd.add_field(name=arg1+' '+arg2, value=game, inline=False)
        embd.set_thumbnail(url='https://jklm.fun/images/icon512.png')
        embd.set_footer(text=f"remember to use {str(random.choice(person))} words 😇")
        if game != 'empty':
            if(len(game)>3):
                await ctx.send(embed=embd)
            else:
                await ctx.send('no rooms with atlest 2 players')
        else:
            await ctx.send("unable to fetch data")
async def setup(client:commands.Bot):
    await client.add_cog(jklm(client))