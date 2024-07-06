import discord
from discord.ext import commands
from discord import Member
from discord.ui import Select
from tokens import *
from score import scores, words, scoreboard
from hang import hangmanc,points,hangmansql
from table2ascii import table2ascii as t2a, PresetStyle
from channel_ids import IdClass,IdClass_new  # DONE
import random
import json
import linecache
import os
person=FRIENDS_LIST
dumb_words=DUMB_LIST
emoji_min=[u"\U0001F1E9",'🆙']
c_list=[";hello",";hangman",";hm",";kick",";punch",";slap",";poke",";jklm",";dum"]
game_stat={"g_id":{"word":"","lisguess":[],"wrong":0}}
counting_image_links = ["https://static1.cbrimages.com/wordpress/wp-content/uploads/2020/05/Hitmonchan.jpg",'https://image.tensorartassets.com/cdn-cgi/image/q=85,w=500/model_showcase/633542774903536154/07c56f38-e0fb-02d2-42d5-d746f6c4678a.jpeg','https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/025.png','https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/107.png']

idc = IdClass()
cidc= IdClass_new()
sb = scoreboard()

all_channels = cidc.get_table()
# print("\n\n all channel : \n",all_channels)
counting_channel_id = {g_data[0]:g_data[1] for g_data in all_channels}
# print("\n \n counting channel id \n \n",counting_channel_id)
hangman_channel_id={g_data[0]:g_data[2] for g_data in all_channels}
ttt_channel_id= {g_data[0]:g_data[3] for g_data in all_channels}
last_number_dict = {g_data[0] : g_data[4] for g_data in all_channels}
last_counter_dict = {g_data[0]: g_data [5] for g_data in all_channels}
disabled_commands = {g_data[0]:json.loads(g_data[6]) for g_data in all_channels}



def get_random_word():
    max_lines = sum(1 for line in open('dict.txt','r',encoding='utf-8'))
    rand_line = random.randint(1, max_lines)
    random_word = linecache.getline('dict.txt', rand_line).strip()
    return random_word

# new_word = get_random_word()

client=commands.Bot(command_prefix=(';','v;'),intents=discord.Intents.all())
client.remove_command('help')


#----------------------------------------------------------------------
@client.command()
async def load_extension(ctx, extension_name):
    if extension_name in client.extensions:
        await ctx.send(f"Extension '{extension_name}' is already loaded.")
    else:
        try:
            client.load_extension(extension_name)
            await ctx.send(f"Extension '{extension_name}' loaded successfully.")
        except commands.ExtensionError as e:
            await ctx.send(f"Error loading extension '{extension_name}': {e}")

#----------------------------------------------------------------------
@client.event
async def on_ready():
    
    print("bot ready\n----------")
    # await client.change_presence(activity=discord.Game("hitMIN"))#, activity=discord.Game("hitMIN")
# ------------------------------------------------------------------------

#COGS=================================================
    await client.load_extension("cogs.actions")
    print('actions loaded')

    await client.load_extension("cogs.jklm")
    print('jklm loaded')

    await client.load_extension("cogs.uttt")
    print("utt loaded")
#--------------------------------------------------------
@client.event
async def on_guild_join(guild):
    channels = guild.channels
    text_channels = [channel for channel in channels if isinstance(channel, discord.TextChannel)]
    counting = [c_name for c_name in text_channels if "counting" in c_name.name]
    hangman = [c_name for c_name in text_channels if "hangman" in c_name.name]
    ttt = [c_name for c_name in text_channels if "tic-tac-toe" in c_name.name]
    countin_ch_id = None
    if len(counting) > 0:
        countin_ch_id=counting[0].id
        counting_channel_id[guild.id] = counting[0].id
        await counting[0].send("Using this channel for counting 1")
    else:
        categories = guild.categories
        category_list = [category for category in categories]
        bot_cat = [cat_name for cat_name in category_list if "bot" in cat_name.name]
        if len(bot_cat) > 0:
            channel_name = "counting"
            cat = bot_cat[0]
            counting_channel = await guild.create_text_channel(name=channel_name, category=cat)
            countin_ch_id=counting_channel.id
            counting_channel_id[guild.id] = counting_channel.id
        else:
            channel_name = "counting"
            cat = await guild.create_category("funbot fun game")
            counting_channel = await guild.create_text_channel(name=channel_name, category=cat)
            countin_ch_id = counting_channel.id
            counting_channel_id[guild.id] = counting_channel.id

    if len(hangman) > 0:
        hangman_ch_id=hangman[0].id
        hangman_channel_id[guild.id] = hangman[0].id
        await hangman[0].send("Using this channel for hangman 1")
    else:
        categories = guild.categories
        category_list = [category for category in categories]
        bot_cat = [cat_name for cat_name in category_list if "bot" in cat_name.name or "game" in cat_name.name]
        if len(bot_cat) > 0:
            channel_name = "hangman"
            cat = bot_cat[0]
            hangman_channel = await guild.create_text_channel(name=channel_name, category=cat)
            hangman_ch_id = hangman_channel.id
            hangman_channel_id[guild.id] = hangman_ch_id
        else:
            channel_name = "hangman"
            cat = await guild.create_category("funbot fun game")
            hangman_channel = await guild.create_text_channel(name=channel_name, category=cat)
            hangman_ch_id = hangman_channel.id
            hangman_channel_id[guild.id] = hangman_ch_id

    if len(ttt) > 0:
        ttt_ch=ttt[0].id
        ttt_channel_id[guild.id]=ttt_ch
        await ttt[0].send("Using this channel for ttt 1")
    else:
        categories = guild.categories
        category_list = [category for category in categories]
        bot_cat = [cat_name for cat_name in category_list if "bot" in cat_name.name or "game" in cat_name.name]
        if len(bot_cat) > 0:
            channel_name = "tic tac toe"
            cat = bot_cat[0]
            ttt_channel = await guild.create_text_channel(name=channel_name, category=cat)
            ttt_ch = ttt_channel.id
            ttt_channel_id[guild.id]=ttt_ch
        else:
            channel_name = "tic tac toe"
            cat = await guild.create_category("funbot fun game")
            ttt_channel = await guild.create_text_channel(name=channel_name, category=cat)
            ttt_ch = ttt_channel.id
            ttt_channel_id[guild.id]=ttt_ch

    last_number_dict[guild.id]=0
    last_counter_dict[guild.id]=None
    disabled_commands[guild.id]=[]
    print("id=",guild.id,"count=",countin_ch_id,"hang=",hangman_ch_id,"ttt=",ttt_ch)
    cidc.add_guilds(gid=guild.id,count=countin_ch_id,hang=hangman_ch_id,ttt=ttt_ch)

# --------------------------------------------------------
@client.event
async def on_message(message):
    if message.guild is None:
        return

    if message.content.upper() in dumb_words:
        await message.channel.send(f"u get dum word penalty, <@{message.author.id}>.")
        sb.add_point((message.author.id),"dum",pname=message.author.name)

        
    #---------------------------------------------------------------------------------------------------------------
    
    elif message.channel.id == counting_channel_id[message.guild.id]:
        try:
            if "counting" in disabled_commands[message.guild.id] or "number" in disabled_commands[message.guild.id]:
                return
        except:
            disabled_commands[message.guild.id]=[]  # ---- ON_MESSAGE EXECUTES BEFORE ON_JOIN SO HAVE TO ADD DISABLED_COMMANDS LIST TO AVOID ERROR OF NOT HAVING GUILD IN THE DISABLED_COMMANDS (KeyError)
        try:
            num = float(message.content)
            num = round(num)
            if num == last_number_dict[message.guild.id] + 1:
                if message.author.id == last_counter_dict[message.guild.id]:
                    await message.add_reaction('🛑')
                    return
                last_number_dict[message.guild.id] = last_number_dict[message.guild.id] + 1
                last_counter_dict[message.guild.id] = message.author.id
                cidc.update_guilds(message.guild.id,"last_number",last_number_dict[message.guild.id])
                cidc.update_guilds(message.guild.id,"last_counter",message.author.id)
                sb.add_point(pid=message.author.id,col_name="c_right")
                await message.add_reaction('✅')
                if num < 1000:
                    if num%100==0:
                        sb.add_point(pid=message.author.id,col_name="c_100")
                        await message.add_reaction('💯')
                else:
                    if num%1000==0:
                        sb.add_point(pid=message.author.id,col_name="c_1k")
                        await message.add_reaction('🎖️')
                return
            else:
                last_number_dict[message.guild.id] = 0
                last_counter_dict[message.guild.id] = None

                cidc.update_guilds(message.guild.id,"last_number",0)
                cidc.update_guilds(message.guild.id,"last_counter",None)
                await message.add_reaction('❌')
                sb.add_point(pid=message.author.id,col_name="c_wrong")
                embd = discord.Embed(title="Broken counting streak",
                                     description=f"<@{message.author.id}> 🫵 broke the streak, start from 0",
                                     colour=0x05D5FA)
                embd.set_thumbnail(
                    url='https://image.tensorartassets.com/cdn-cgi/image/q=85,w=500/model_showcase/633542774903536154/07c56f38-e0fb-02d2-42d5-d746f6c4678a.jpeg')
                await message.channel.send(embed=embd)
                return
        except:
            pass

    elif message.channel.id == hangman_channel_id[message.guild.id]:
        if message.content[0] == ";" or message.content[0] == ";v":
            await client.process_commands(message)
            return
        try:
            if "hangman" in disabled_commands[message.guild.id] or "hm" in disabled_commands[message.guild.id]:
                return
        except:
            disabled_commands[message.guild.id]=[]  # ---- ON_MESSAGE EXECUTES BEFORE ON_JOIN SO HAVE TO ADD DISABLED_COMMANDS LIST TO AVOID ERROR OF NOT HAVING GUILD IN THE DISABLED_COMMANDS (KeyError)
        
        if message.channel.id != hangman_channel_id[message.guild.id]:
            return

        # await client.change_presence( activity=discord.Game("hangman"))
        # message.content="this ?"# is a sentence with spaces"
        split_word = message.content.split(" ",3)
        guess = None
        if len(split_word) == 1:
            if split_word[0].isalpha():
                guess = split_word[0].strip()
                guess=guess.upper()
            else:
                pass
        elif(len(split_word))==2:
            if not split_word[1].isalpha():
                if split_word[0].isalpha():
                    guess = split_word[0].strip()
                    guess = guess.upper()
                else:
                    pass
            else:
                pass
        if guess == None:
            return
        global lisguess,word,wrong
        hsql = hangmansql()
        hangman_stat = hsql.get_hangman(message.guild.id)
        if hangman_stat == None:
            return
        word = hangman_stat["word"]
        lisguess = hangman_stat["lisguess"]
        wrong = hangman_stat["wrongs"]

        # ADD EMBED TO THE WRONG GUESSES ALERT.
        # --------------------------------------

        if(wrong>=5):
            embd = discord.Embed(title="5/5 wrong guess",description=f"the word was '{word}'\n\t\t GAME OVER",colour=0x05D5FA)
            embd.set_thumbnail(url=random.choice(counting_image_links))
            await message.channel.send(embed=embd)
            # await message.channel.send(f'```, the word was "{word}"\n\t\t GAME OVER```') # THIS SHOULD BE AN EMBD✅
            word=''
            lisguess=[]
            wrong=0
            hsql.reset_game(message.guild.id)
            return

        if(len(word)<2):
            await message.channel.send("Start a new game (;hangman)")
            return
        if(not guess.isalpha()):
            await message.channel.send('invalid entry, try again')
            return
        if(len(guess)>1):
            if(guess==word):
                
                if(guess==word):
                    flag=0
                    for i in lisguess:
                        if not(i.isalpha()):   
                            flag+=1
                    if len(word)<=7:
                        if flag>(len(word)//2):
                            point=10
                        else:
                            point =3
                    else:
                        if flag>(len(word)//3):
                            point=10
                        else:
                            point=3
                
                embd = discord.Embed(title="Correct guess",description=f"Good job, you guessed it right ({point} points)",colour=0x05D5FA)
                embd.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlA_A_yMkrOLNCc9GmZUuQiVS2qsnha8EceQ&s')
                await message.channel.send(embed=embd)
                # await message.channel.send(f"good job, you guessed it right ({point} points)")
                sb.add_point(message.author.id,"hangman",value=point,pname=message.author.name)
                lisguess=[]
                word=''
                wrong=0
                hsql.reset_game(message.guild.id)
                return
            else:
                #CHECK IF THE LENGTH OF GUESS IS SAME AS LENGTH OF WORD
                if len(guess) != len(word):
                    return                

                wrong+=1
                point=-1
                sb.add_point(message.author.id,"hangman",value=point,pname=message.author.name)
                hsql.update_hangman(message.guild.id,"wrongs",wrong)
                await message.channel.send(f"```wrong guess {wrong}/5 ({point} points)```")
                if wrong==5:
                    embd = discord.Embed(title="5/5 wrong guess",description=f"the word was '{word}'\n\t\t GAME OVER",colour=0x05D5FA)
                    embd.set_thumbnail(url='https://image.tensorartassets.com/cdn-cgi/image/q=85,w=500/model_showcase/633542774903536154/07c56f38-e0fb-02d2-42d5-d746f6c4678a.jpeg')
                    await message.channel.send(embed=embd)
                    # await message.channel.send(f'```5/5 wrong guess, the word was "{word}"\n\t\t GAME OVER```')
                    word=''
                    lisguess=[]
                    wrong=0
                    hsql.reset_game(message.guild.id)
                    return
                return
        if(guess in lisguess):
            await message.channel.send('already guessed')
            return
        elif(guess in word):
            k=0
            point=1
            sb.add_point(message.author.id,"hangman",point,message.author.name)
            for j in word:
                if j == guess:
                    lisguess[k]=j
                    l=lisguess
                k+=1
            hsql.update_hangman(message.guild.id,"lisguess",json.dumps(l))

            await message.channel.send(f"`{' '.join(lisguess)}` ({point} points)")
        elif(guess.isalpha() and guess not in word):
            wrong=wrong+1
            point=-1
            sb.add_point(message.author.id,"hangman",point,message.author.name)
            hsql.update_hangman(message.guild.id,"wrongs",wrong)
            await message.channel.send(f"wrong guess ({wrong}/5) ({point} points)")
            
            if wrong==5:
                    await message.channel.send(f'```5/5 wrong guess, the word was "{word}"\n\t\t GAME OVER```')
                    word=''
                    lisguess=[]
                    wrong=0
                    hsql.reset_game(message.guild.id)
                    return
            await message.channel.send(f"`{' '.join(lisguess)}`")
            return
        guess_word=''.join(lisguess)
        if guess_word==word:
            point=3
            sb.add_point(message.author.id,"hangman",point,message.author.name)
            await message.channel.send(f"Yay!! u guessed it right ({point} points)")
            word=''
            lisguess=[]
            wrong=0
            hsql.reset_game(message.guild.id)
            return
    
    #-------------------------------------------------
    await client.process_commands(message)
#HELLO ----------------------------------------
@client.command(aliases=['hello', 'hi', 'hola'])
async def greet(ctx):
    await ctx.send("hello! I am Funbot")

#---- CHANGE CHANNEL ---------------------------------------------------

@client.command()
async def change_channel(ctx, arg1=None, *, arg2=None):

#--------- CHECKING IF USER IS ADMIN OR MOD -------------------------------------------------------------------------------
    if any(role.name in ['Admin', 'Moderator'] for role in ctx.author.roles)  or ctx.author.id == OWNERID:
        pass
    else:
        await ctx.send(" Command reserved for only admins and mods ")
        return
#----------------------------------------------------------------------------------------
    
    commands_list = ["hangman", "ut", "t", "hm", "counting"]
    if arg1 is None or arg2 is None:
        await ctx.send("enter command name and channel name ;change_channel <command name> <channel name>")
        return
    else:
        channels = ctx.guild.channels
        text_channels = [channel for channel in channels if isinstance(channel, discord.TextChannel)]
        channel_list = [c_name for c_name in text_channels if
                        str(arg2) in c_name.name or arg2.replace(" ", "-") in c_name.name]
        if len(channel_list) > 0:
            if str(arg1) in commands_list:
                if arg1 == "hangman" or arg1 == "hm":
                    cidc.update_guilds(ctx.guild.id,"hangman_ch",channel_list[0].id)
                    return
                elif arg1 == "ut" or arg1 == "t":
                    cidc.update_guilds(ctx.guild.id,"ttt_ch",channel_list[0].id)
                    return
                elif arg1 == "counting" or arg1 == "number":
                    cidc.update_guilds(ctx.guild.id,"count_ch",channel_list[0].id)
            else:
                await ctx.send(
                    "You change channel of only the games and counting ||please let the bot roam freely in other rooms 🥹||")
                return
#---- DISABLE COMMAND -----------------------------------------------------

@client.command()
async def disable_command(ctx, *, arg1=None):

#--------- CHECKING IF USER IS ADMIN OR MOD -------------------------------------------------------------------------------

    if any(role.name in ['Admin', 'Moderator'] for role in ctx.author.roles)  or ctx.author.id == OWNERID:
        pass
    else:
        await ctx.send(" Command reserved for only admins and mods ")
        return

#----------------------------------------------------------------------------------------

    commands_list = ["hangman", "ut", "t", "hm", "counting", ";jklm", "kick", "slap", "punch", "poke", "d", "dum",
                     "echo", "number"]
    if arg1 is None:
        await ctx.send("Enter the command in the format ;disable_command <command name>")
        return
    if arg1 in commands_list:
        await ctx.message.add_reaction('✔️')
        if arg1 in disabled_commands[ctx.guild.id]:
            await ctx.message.add_reaction('👎')
            await ctx.send("Command is already disabled")
            return
        else:
            if arg1 in ["hangman", "hm"]:
                disabled_commands[ctx.guild.id].append("hangman")
                disabled_commands[ctx.guild.id].append("hm")
                cidc.update_guilds(ctx.guild.id,"disabled_comm",json.dumps(disabled_commands[ctx.guild.id]))
                return
            elif arg1 in ["ut", "t"]:
                disabled_commands[ctx.guild.id].append("ut")
                disabled_commands[ctx.guild.id].append("t")
                cidc.update_guilds(ctx.guild.id,"disabled_comm",disabled_commands[ctx.guild.id])
                return
            elif arg1 in ["counting", "number"]:
                disabled_commands[ctx.guild.id].append("counting")
                disabled_commands[ctx.guild.id].append("number")
                cidc.update_guilds(ctx.guild.id,"disabled_comm",disabled_commands)
                return

            disabled_commands[ctx.guild.id].append(arg1)
            cidc.update_guilds(ctx.guild.id,"disabled_comm",disabled_commands)
            return

    else:
        await ctx.message.add_reaction('👎')
        await ctx.send("command not supported check ;help to see all commands")
        return

#---- ENABLE COMMAND  -----------------------------------------------------

@client.command()
async def enable_command(ctx, *, arg1=None):

#------ CHECKING IF USER IS ADMIN OR MOD ----------------------------------------------------------------------------------
    if any(role.name in ['Admin', 'Moderator'] for role in ctx.author.roles) or ctx.author.id == OWNERID:
        pass
    else:
        await ctx.send(" Command reserved for only admins and mods ")
        return
#----------------------------------------------------------------------------------------

    if arg1 is None:
        await ctx.send("Enter the command in the format ;enable_command <command name>")
        return
    commands_list = ["hangman", "ut", "t", "hm", "counting", ";jklm", "kick", "slap", "punch", "poke", "d", "dum",
                     "echo", "number"]
    if arg1 in commands_list:
        await ctx.message.add_reaction('✔️')
        if arg1 not in disabled_commands[ctx.guild.id]:
            await ctx.send("Command is already enabled")
            return
        else:
            if arg1 in ["hangman", "hm"]:
                disabled_commands[ctx.guild.id].remove("hangman")
                disabled_commands[ctx.guild.id].remove("hm")
                cidc.update_guilds(ctx.guild.id,"disabled_comm",disabled_commands)
                return
            if arg1 in ["ut", "t"]:
                disabled_commands[ctx.guild.id].remove("ut")
                disabled_commands[ctx.guild.id].remove("t")
                cidc.update_guilds(ctx.guild.id,"disabled_comm",disabled_commands)
                return
            if arg1 in ["counting", "number"]:
                disabled_commands[ctx.guild.id].remove("counting")
                disabled_commands[ctx.guild.id].remove("number")
                cidc.update_guilds(ctx.guild.id,"disabled_comm",disabled_commands)
                return

            disabled_commands[ctx.guild.id].remove(arg1)
            cidc.update_guilds(ctx.guild.id,"disabled_comm",disabled_commands)
            return
    else:
        await ctx.send("Not a valid a command")
#---- NUMBER COMMAND ----------------------------------------------------
@client.command(aliases=["num"])
async def number(ctx):
    if "counting" in disabled_commands[ctx.guild.id] or "number" in disabled_commands[ctx.guild.id]:
        return
    if ctx.channel.id != counting_channel_id[ctx.guild.id]:
        return

    else:
        embd = discord.Embed(title="counting", colour=0x05D5FA)
        embd.add_field(name="last number", value=last_number_dict[ctx.guild.id])
        embd.add_field(name="last counter", value=f"<@{last_counter_dict[ctx.guild.id]}>")
        await ctx.send(embed=embd)
        return

#---- HANGMAN GAME -------------------------------------------------------

@client.command()
async def hangman(ctx):

    if "hangman" in disabled_commands[ctx.guild.id] or "number" in disabled_commands[ctx.guild.id]:
        return
    if ctx.channel.id != hangman_channel_id[ctx.guild.id]:
        return

    hsql = hangmansql()
    hangman_stat = hsql.get_hangman(ctx.guild.id)
    if hangman_stat == None:
        hsql.create_game(ctx.guild.id)
    hangman_stat = hsql.get_hangman(ctx.guild.id)
    word = hangman_stat["word"]
    lisguess = hangman_stat["lisguess"]
    if word == None:
        new_word=get_random_word()
        word=new_word
        lisguess=[]
        for i in word:
            lisguess.append('_')
        await ctx.send(f"`{' '.join(lisguess)}, ({len(word)} letters)`")
        hsql.create_game(ctx.guild.id,word,lisguess,0)
        return

    if(len(word)>2):
        await ctx.send(f":rolling_eyes: uh...\nGAME IN PROGRESS, use ;hm <guess> to play```{' '.join(lisguess)}, ({len(word)} letters)```")
        return
    new_word=get_random_word()
    word=new_word
    lisguess=[]
    for i in word:
        lisguess.append('_')
    await ctx.send(f"`{' '.join(lisguess)}, ({len(word)} letters)`")
    hsql.create_game(ctx.guild.id,word,lisguess,0)
# ======================================================================
    
@client.command()
async def hm(ctx,arg=''):

    if "hangman" in disabled_commands[ctx.guild.id]:
        return
    if ctx.channel.id != hangman_channel_id[ctx.guild.id]:
        return

    # await client.change_presence( activity=discord.Game("hangman"))
    args=arg.upper()
    guess=args
    global lisguess,word,wrong
    hsql = hangmansql()
    hangman_stat = hsql.get_hangman(ctx.guild.id)
    word = hangman_stat["word"]
    lisguess = hangman_stat["lisguess"]
    wrong = hangman_stat["wrongs"]
    if(wrong>=5):
        await ctx.send(f'```5/5 wrong guess, the word was "{word}"\n\t\t GAME OVER```')
        word=''
        lisguess=[]
        wrong=0
        hsql.reset_game(ctx.guild.id)
        return

    if(len(word)<2):
        await ctx.send("Start a new game (;hangman)")
        return
    if(not guess.isalpha()):
        await ctx.send('invalid entry, try again')
        return
    if(len(guess)>1):
        if(guess==word):
            
            if(guess==word):
                flag=0
                for i in lisguess:
                    if not(i.isalpha()):   
                        flag+=1
                if len(word)<=7:
                    if flag>(len(word)//2):
                        point=10
                    else:
                        point =3
                else:
                    if flag>(len(word)//3):
                        point=10
                    else:
                        point=3
            await ctx.send(f"good job, you guessed it right ({point} points)")
            sb.add_point(ctx.author.id,"hangman",value=point,pname=ctx.author.name)
            lisguess=[]
            word=''
            wrong=0
            hsql.reset_game(ctx.guild.id)
            return
        else:
            wrong+=1
            point=-1
            sb.add_point(ctx.author.id,"hangman",value=point,pname=ctx.author.name)
            hsql.update_hangman(ctx.guild.id,"wrongs",wrong)
            await ctx.send(f"wrong guess {wrong}/5 ({point} points)")
            if wrong==5:
                await ctx.send(f'```5/5 wrong guess, the word was "{word}"\n\t\t GAME OVER```')
                word=''
                lisguess=[]
                wrong=0
                hsql.reset_game(ctx.guild.id)
                return
            return
    if(guess in lisguess):
        await ctx.send('already guessed')
        return
    elif(guess in word):
        k=0
        point=1
        sb.add_point(ctx.author.id,"hangman",point,ctx.author.name)
        for j in word:
            if j == guess:
                lisguess[k]=j
                l=lisguess
            k+=1
        hsql.update_hangman(ctx.guild.id,"lisguess",json.loads(l))

        await ctx.send(f"`{' '.join(lisguess)}` ({point} points)")
    elif(guess.isalpha() and guess not in word):
        wrong=wrong+1
        point=-1
        sb.add_point(ctx.author.id,"hangman",point,ctx.author.name)
        hsql.update_hangman(ctx.guild.id,"wrongs",wrong)
        await ctx.send(f"wrong guess ({wrong}/5) ({point} points)")
        
        if wrong==5:
                await ctx.send(f'```5/5 wrong guess, the word was "{word}"\n\t\t GAME OVER```')
                word=''
                lisguess=[]
                wrong=0
                hsql.reset_game(ctx.guild.id)
                return
        await ctx.send(f"`{' '.join(lisguess)}`")
        return
    guess_word=''.join(lisguess)
    if guess_word==word:
        point=3
        sb.add_point(ctx.author.id,"hangman",point,ctx.author.name)
        await ctx.send(f"Yay!! u guessed it right ({point} points)")
        word=''
        lisguess=[]
        wrong=0
        hsql.reset_game(ctx.guild.id)
        return
#--------------------------------------------------------
@client.command(name="d", brief="shows meaning of the word entered", help=";d <word> shows meaning from merriam webster dictionary(free version)")
async def d(ctx, arg1=None):
    if arg1==None:
        await ctx.send("Enter the word to search meaning (`;d <word>`)")
    meaning,wsite=words.meaning(arg1)
    if wsite==1:
        embd=discord.Embed(title="Merriam Webster",url='https://merriam-webster.com/',colour=0x05D5FA)
        embd.add_field(name=arg1, value=meaning[:800], inline=False)
        embd.set_thumbnail(url='https://merriam-webster.com/assets/mw/static/social-media-share/mw-logo-245x245@1x.png')
    if wsite==2:
        embd=discord.Embed(title="Urban Dictionary", url='https://www.urbandictionary.com/',color=0x05D5FA)
        embd.add_field(name=arg1, value=meaning[:800], inline=False)
        embd.set_thumbnail(url='https://asset.brandfetch.io/idDKU5RwKB/idAtwngHxG.png')
    if wsite==0:
        embd=discord.Embed(title="Bruh..",color=0xF22C2C)
        embd.add_field(name=arg1,value=str(meaning[0])+"😭",inline=False)

    embd.set_footer(text=f"feel free to give suggestions and feedbacks(use ;feedback) 😇") 
    await ctx.send(embed=embd)   

# -------------------------------------------------------
    
@client.command(aliases = ["feedback","fb","suggestion"])
async def take_fb(ctx,*,message):
    with open('feedback.txt', 'a') as file:
            file.write('- '+str(ctx.message.author.name) +' - ' +message + '\n')
            file.close()
    user = await client.fetch_user(int(OWNERID))
    await user.send(f'feedback from : {str(ctx.message.author.name)} = {message}')
    await ctx.send("thank you for the feedback")

#------------------------------------------------------------------------------------------

@client.command()
async def echo(ctx):
    msg=ctx.message.content
    await ctx.send(msg[5:])

#-------------------------------------------------------------------------------------------

@client.command()
async def hmscore(ctx,*,member:discord.Member=None):
    if(member==None):
        member=ctx.author

    score = sb.get_score(member.id)
    if score:
        await ctx.send(f"{member} has {score} points in hangman")
    else:
        await ctx.send(f"{member} has not played the game yet, use ```;hangman``` to start game 🙂")

#---------------------------------------------------------------------------------------------------------------        

@client.command(aliases=["top","scoreboard","lb","sb"])
async def leaderboard(ctx,arg=None,arg2=None):
    game_list=["ut","ttt","tic","count","number","counting"]
    if arg:
        arg=arg.lower()
    if arg2:
        arg2=arg2.lower()
    guild_members_list = [member.id for member in ctx.guild.members]
    if arg in game_list:
        if arg == "count" or arg == "number" or arg == "counting":
            #return count score ----   score_dict = sb.highscore()
            col = None
            if arg2:
                if arg2 == "100" or arg2 == "100s":
                    col = "c_100"
                elif arg2 == "wrong" or arg2 == "wrongs":
                    col = "c_wrong"
                elif arg2 == "1000" or arg2 == "1000s" or arg2 == "1k":
                    col = "c_1k"
                else:
                    col = "c_right"
            else:
                col = "c_right"
            score_data = sb.highscore("count",col=col)
            score=[]
            for data in score_data:
                if int(data[0]) in guild_members_list:
                    score.append(data)
            sort_score = enumerate(score,1)
            score_list = []
            for ranked in sort_score:
                a=[]
                a.append(ranked[0])
                for i in ranked[1]:
                    a.append(i)
                b= int(a[1])
                user_name = str(ctx.guild.get_member(b))
                if len(user_name) > 13:
                    user_name = user_name[:10] + "..."
                if user_name is None:
                    try:
                        user_name = await str(ctx.guild.fetch_member(b))
                        if len(user_name) > 13:
                            user_name = user_name[:10] + "..."
                    except:
                        user_name = "Unknown"
                a[1]=str(f"{user_name}")
                score_list.append(a)
                if len(score_list)==5:
                    break
            out = t2a(header=["#","PLAYER","✅", "❌","100s","1Ks"],body=score_list)
            discord_table = f"```\n{out}\n```"
            embed = discord.Embed(title="Server Leaderboard : Counting", description=discord_table, color=0x00ff00)
            embed.set_footer(text="For global leaderboard commands ```;gtop```` or ```;glb``` or ```;sb``` 😇")
            await ctx.send(embed=embed)
        elif arg == "ut" or arg == "ttt" or arg == "tic":
            #return tic tac toe score
            col = "t_win"
            if arg2:
                if arg2 == "loss" or arg2 == "losses" or arg2 == "los":
                    col = "t_loss"
                elif arg2 == "games" or arg2 == "game" or arg2=="gam":
                    col = "t_games"
                elif arg2 == "win%" or arg2 == "wins%" or arg2 == "winper" or arg2 == "%":
                    col = "t_win*100.0/t_games"
                else:
                    col = "t_win"
            else:
                col = "t_win"

            score_data = sb.highscore("ut",col=col)
            score=[]
            for data in score_data:
                if int(data[0]) in guild_members_list:
                    score.append(data)
            sort_score = enumerate(score,1)
            score_list = []
            for ranked in sort_score:
                a=[]
                a.append(ranked[0])
                for i in ranked[1]:
                    a.append(i)
                b= int(a[1])
                user_name = str(ctx.guild.get_member(b))
                if len(user_name) > 13:
                    user_name = user_name[:10] + "..."
                if user_name is None:
                    try:
                        user_name = await str(ctx.guild.fetch_member(b))
                        if len(user_name) > 13:
                            user_name = user_name[:10] + "..."
                    except:
                        user_name = "Unknown"
                a[1]=str(f"{user_name}")
                score_list.append(a)
                if len(score_list)==5:
                    break
            out = t2a(header=["#","USER","W","L","GAMES","WIN%"],body=score_list)
            discord_table = f"```\n{out}\n```"
            embed = discord.Embed(title="Server Leaderboard : Ultimate Tic-Tac-Toe", description=discord_table, color=0x00ff00)
            embed.set_footer(text="For global leaderboard commands ```;gtop```` or ```;glb``` or ```;sb``` 😇")
            await ctx.send(embed=embed)
    else:
        col = None
        if arg == "dum" or arg == "dumb" or arg == "dums":
            score_data = sb.highscore("dum",order="ASC")
            score = list(enumerate(score_data,1))
            score_list=[]
            for player in score:
                a= []
                a.append(player[0])
                for i in player[1]:
                    a. append(i)
                b=int(player[1][0])
                if b not in guild_members_list:
                    continue
                user_name = str(ctx.guild.get_member(b))
                if len(user_name)> 13:
                    user_name = user_name[:10] + "..."
                if user_name is None:
                    try:
                        user_name = await str(ctx.guild.fetch_member(b))
                        if len(user_name) > 13:
                            user_name = user_name[:10] + "..."
                    except:
                        user_name = "Unknown"
                a[1]=str(f"{user_name}")
                score_list.append(a)
                if len(score_list) == 5:
                    break
            out = t2a(header=["#","USER","DUMS"],body=score_list)
            discord_table = f"```\n{out}\n```"
            embed = discord.Embed(title="Server Leaderboard : Dumbness Counter", description=discord_table, color=0x00ff00)
            embed.set_footer(text="For global leaderboard commands ```;gtop```` or ```;glb``` or ```;sb``` 😇")
            await ctx.send(embed=embed)
        else:
            score_data = sb.highscore("hangman",col=col)
            score=[]
            for data in score_data:
                if int(data[0]) in guild_members_list:
                    score.append(data)
            sort_score = enumerate(score,1)
            score_list = []
            for ranked in sort_score:
                a=[]
                a.append(ranked[0])
                for i in ranked[1]:
                    a.append(i)
                b= int(a[1])
                user_name = str(ctx.guild.get_member(b))
                if len(user_name) > 13:
                    user_name = user_name[:10] + "..."
                if user_name is None:
                    try:
                        user_name = await str(ctx.guild.fetch_member(b))
                        if len(user_name) > 13:
                            user_name = user_name[:10] + "..."
                    except:
                        user_name = "Unknown"
                a[1]=str(f"{user_name}")
                score_list.append(a)
                if len(score_list)==5:
                    break
            out = t2a(header=["#","PLAYER","POINTS"],body=score_list)
            discord_table = f"```\n{out}\n```"
            embed = discord.Embed(title="Global Leaderboard: Hangman", description=discord_table, color=0x00ff00)
            embed.set_footer(text="For server leaderboard commands ```;gtop```` or ```;glb``` or ```;gsb``` 😇")
            await ctx.send(embed=embed)
        pass

# ----------------------------------------------------------------------------------

@client.command(aliases=["globaltop","gtop","globalscoreboard","gscoreboard","glb","gsb","globalsb","globallb"])
async def globalleaderboard(ctx,arg=None,arg2=None):
    game_list=["ut","ttt","tic","count","number","counting"]
    if arg:
        arg=arg.lower()
    if arg2:
        arg2=arg2.lower()
    guild_members_list = [member.id for member in ctx.guild.members]
    if arg in game_list:
        if arg == "count" or arg == "number" or arg == "counting":
            #return count score ----   score_dict = sb.highscore()
            col = None
            if arg2:
                if arg2 == "100" or arg2 == "100s":
                    col = "c_100"
                elif arg2 == "wrong" or arg2 == "wrongs":
                    col = "c_wrong"
                elif arg2 == "1000" or arg2 == "1000s" or arg2 == "1k":
                    col = "c_1k"
                else:
                    col = "c_right"
            else:
                col = "c_right"
            score_data = sb.highscore("count",col=col)
            score = list(enumerate(score_data,1))
            score_list=[]
            for player in score:
                a= []
                a.append(player[0])
                for i in player[1]:
                    a. append(i)
                b=int(player[1][0])
                if b not in guild_members_list:
                    continue
                user_name = str(ctx.guild.get_member(b))
                if len(user_name) > 13:
                    user_name = user_name[:10] + "..."
                if user_name is None:
                    try:
                        user_name = await str(ctx.guild.fetch_member(b))
                        if len(user_name) > 13:
                            user_name = user_name[:10] + "..."
                    except:
                        user_name = "Unknown"
                a[1]=str(f"{user_name}")
                score_list.append(a)
                if len(score_list) == 5:
                    break
            out = t2a(header=["#","PLAYER","✅", "❌","100s","1Ks"],body=score_list)
            discord_table = f"```{out}\n```"
            embed = discord.Embed(title="Global Leaderboard : Counting", description=discord_table, color=0x00ff00)
            embed.set_footer(text="For server leaderboard commands ```;top```` or ```;lb``` or ```;sb``` 😇")
            await ctx.send(embed=embed)
            pass
        elif arg == "ut" or arg == "ttt" or arg == "tic":
            #return tic tac toe score
            col = "t_win"
            if arg2:
                if arg2 == "loss" or arg2 == "losses" or arg2 == "los":
                    col = "t_loss"
                elif arg2 == "games" or arg2 == "game" or arg2=="gam":
                    col = "t_games"
                elif arg2 == "win%" or arg2 == "wins%" or arg2 == "winper" or arg2 == "%":
                    col = "t_win*100.0/t_games"
                else:
                    col = "t_win"
            else:
                col = "t_win"

            score_data = sb.highscore("ut",col=col)
            score = list(enumerate(score_data,1))
            score_list=[]
            for player in score:
                a= []
                a.append(player[0])
                for i in player[1]:
                    a. append(i)
                b=int(player[1][0])
                if b not in guild_members_list:
                    continue
                user_name = str(ctx.guild.get_member(b))
                if len(user_name) > 13:
                    user_name = user_name[:10] + "..."
                if user_name is None:
                    try:
                        user_name = await str(ctx.guild.fetch_member(b))
                        if len(user_name) > 13:
                            user_name = user_name[:10] + "..."
                    except:
                        user_name = "Unknown"
                a[1]=str(f"{user_name}")
                score_list.append(a)
                if len(score_list) == 5:
                    break
            out = t2a(header=["#","USER","W","L","GAMES","WIN%"],body=score_list)
            discord_table = f"```{out}\n```"
            embed = discord.Embed(title="Global Leaderboard: Ultimate Tic-Tac-Toe", description=discord_table, color=0x00ff00)
            embed.set_footer(text="For server leaderboard commands ```;top```` or ```;lb``` or ```;sb``` 😇")
            await ctx.send(embed=embed)
            pass
    else:
        #return hangman scores
        col = None
        if arg == "dum" or arg == "dumb" or arg == "dums":
            score_data = sb.highscore("dum",order="ASC")
            score = list(enumerate(score_data,1))
            score_list=[]
            for player in score:
                a= []
                a.append(player[0])
                for i in player[1]:
                    a. append(i)
                b=int(player[1][0])
                if b not in guild_members_list:
                    continue
                user_name = str(ctx.guild.get_member(b))
                if len(user_name) > 13:
                    user_name = user_name[:10] + "..."
                if user_name is None:
                    try:
                        user_name = await str(ctx.guild.fetch_member(b))
                        if len(user_name) > 13:
                            user_name = user_name[:10] + "..."
                    except:
                        user_name = "Unknown"
                a[1]=str(f"{user_name}")
                score_list.append(a)
                if len(score_list) == 5:
                    break
            out = t2a(header=["#","USER","DUMS"],body=score_list)
            discord_table = f"```\n{out}\n```"
            embed = discord.Embed(title="Global Leaderboard: Dumbness Counter", description=discord_table, color=0x00ff00)
            embed.set_footer(text="For server leaderboard commands ```;top```` or ```;lb``` or ```;sb``` 😇")
            await ctx.send(embed=embed)
        else:
            score_data = sb.highscore("hangman",col=col)
            score = list(enumerate(score_data,1))
            score_list=[]
            for player in score:
                a= []
                a.append(player[0])
                for i in player[1]:
                    a. append(i)
                b=int(player[1][0])
                if b not in guild_members_list:
                    continue
                user_name = str(ctx.guild.get_member(b))
                if len(user_name) > 13:
                    user_name = user_name[:10] + "..."
                if user_name is None:
                    try:
                        user_name = await str(ctx.guild.fetch_member(b))
                        if len(user_name) > 13:
                            user_name = user_name[:10] + "..."
                    except:
                        user_name = "Unknown"
                a[1]=str(f"{user_name}")
                score_list.append(a)
                if len(score_list) == 5:
                    break
            out = t2a(header=["#","PLAYER","✅", "❌","100s","1Ks"],body=score_list)
            discord_table = f"```\n{out}\n```"
            embed = discord.Embed(title="Global Leaderboard: Hangman", description=discord_table, color=0x00ff00)
            embed.set_footer(text="For server leaderboard commands ```;top```` or ```;lb``` or ```;sb``` 😇")
            await ctx.send(embed=embed)
        pass


    
#-----------------------------------------------

@client.command(aliases = ["score","mytop"])
async def myscore(ctx,arg=None):
    user = ctx.author.id
    if arg:
        arg=arg.lower()
    if arg == "ut" or arg == "tic":
        ut = [0,0,0,0]
        raw= sb.my_score(user,arg="ut")
        if raw:
            ut= [raw[0],raw[1],raw[2],raw[3]]
        ut_table = t2a(header=["WINS","LOSSES","GAMES","WIN %"],body=[ut])
        discord_table = f"```{ut_table}```"
        embed = discord.Embed(title="Your scores in the Ultimate Tic-Tac-Toe", description=discord_table, color=0x00ff00)
        embed.set_footer(text="😇")
        embed.set_thumbnail(url=random.choice(counting_image_links))
        await ctx.send(embed=embed)
    elif arg == "count" or arg == "counting":
        raw= sb.my_score(user,arg="count")
        counting = [0,0,0,0]
        if raw:
            counting =[raw[0],raw[1],raw[2],raw[3]]
        counting_table = t2a(header=["RIGHTS", "WRONGS","100s","1000s"],body=[counting])
        discord_table = f"```{counting_table}```"
        embed = discord.Embed(title="Your scores in the Counting Game", description=discord_table, color=0x00ff00)
        embed.set_footer(text="😇")
        embed.set_thumbnail(url=random.choice(counting_image_links))
        await ctx.send(embed=embed)
    elif arg == "all" or arg == "a":
        a= sb.my_score(user,arg="all")
        hang_dum = [0,0]
        ut = [0,0,0,0]
        counting = [0,0,0,0]
        if a:
            hang_dum = [a[5],a[0]]
            ut= [a[6],a[7],a[8],a[9]]
            counting =[a[1],a[2],a[3],a[4]]
        hd_table = t2a(header=["HANGMAN", "DUMBNESS LEVEL"],body=[hang_dum])
        ut_table = t2a(header=["WINS","LOSSES","GAMES","WIN %"],body=[ut])
        counting_table = t2a(header=["RIGHTS", "WRONGS","100s","1000s"],body=[counting])
        hd_formatted = f"```{hd_table}```"
        ut_formatted = f"```{ut_table}```"
        count_formatted = f"```{counting_table}```"
        embed = discord.Embed(title="Your scores in all the games",description="\n\n",color=0x2724ED)
        embed.add_field(name="Your scores in the Hangman Game and Dumbness level", value=hd_formatted, inline=False)
        embed.add_field(name="Your scores in the Counting Game", value=count_formatted, inline=False)
        embed.add_field(name="Your scores in the Ultimate Tic-Tac-Toe Game", value=ut_formatted, inline=False)
        embed.set_footer(text="😇")
        embed.set_thumbnail(url=random.choice(counting_image_links))
        await ctx.send(embed=embed)
        
    else:
        raw= sb.my_score(user,arg="hang")
        hang_dum=[0,0]
        if raw:
            hang_dum = [raw[0],raw[1]]
        hd_table = t2a(header=["HANGMAN", "DUMBNESS LEVEL"],body=[hang_dum])
        discord_table = f"```{hd_table}```"
        embed = discord.Embed(title="Your scores in the Hangman Game and Dumbness Level", description=discord_table, color=0x00ff00)
        embed.set_footer(text="😇")
        embed.set_thumbnail(url=random.choice(counting_image_links))

        await ctx.send(embed=embed)
#--------------------------------------------------------------------------------------
@client.command()
async def getfb(ctx):
    user = await client.fetch_user(int(OWNERID))
    with open("feedback.txt", 'rb') as f:
        fileToSend = discord.File(f, filename='file.txt')
    await user.send('👀')
    await user.send(f"Here is your file:", file=fileToSend)
    await ctx.send("sent DM")

#--------------------------------------------------------------------------------------
@client.command()
async def getdb(ctx):
    my = int(OWNERID)
    if ctx.author.id != my:
        return    
    user = await client.fetch_user(int(OWNERID))
    with open("funbot.db", 'rb') as f:
        database = discord.File(f, filename='data.db')
    await user.send('👀')
    await user.send(f"Here is your file:", file=database)
    await ctx.send("sent DM")


#--------------------------------------------------------------------------------------
    
@client.command()
async def help(ctx,*,arg=None):
    
    if arg==None:
        embd=discord.Embed(title="Funbot help menu",description="The bot uses command prefixes `;` and `v;`\nuse ;help <command> for further information",colour=0x05D5FA)
        embd.add_field(name="GAMES", value="`;ut, ;t, ;endut` (Ultimate tic-tac-toe)\n`;hangman ;hm ;hmscore` (Hangman)\n", inline=False)
        embd.add_field(name="JKLM", value="`;jklm`", inline=False)
        embd.add_field(name="COUNTING", value="`;number`", inline=False)
        embd.add_field(name="ACTIONS", value="`;kick, ;slap, ;punch, ;poke`", inline=False)
        embd.add_field(name="MISCELLANEOUS", value="`;lb`(server leaderboard),\n`;glb`(global leaderboard),\n`;d`(dictionary meaning), \n`;echo` (repeats your message),\n`;feedback` (sends feedback to dev(;fb or ;suggestion))\n`;disable_command` (only for admin and mods)\n`;enable_command` (only for admin and mods)\n`;change_channel` (only for admin and mods) ", inline=False)
    else:
        if arg=='ut'or arg==';ut':
            embd=discord.Embed(title="Funbot help menu",description="Ultimate tic-tac-toe",colour=0x05D5FA)
            embd.add_field(name=";ut", value="this command allows the player to start a new game and to show existing game.\n\nhow to use :\n `;ut` (shows ongoing game)\n `;ut @opponent` (starts a new game with opponent) ;endut to end existing game", inline=False)
        elif arg=='t' or arg==';t':
            embd=discord.Embed(title="Funbot help menu",description="Ultimate tic-tac-toe",colour=0x05D5FA)
            embd.add_field(name=";t", value="This command allows the player to place their mark in the game board.\nThe command behaves differently depending on the game situation.\n\nInput is taken in the following format: \n\t if game number is defined with green boundary player enters location `;t <location(1-9)>`\n\tIf multiple game boxes are marked green \n`;t <game_number(1-9)><location(1-9)>`", inline=False)
            embd.add_field(name=" ",value="Don't worry the bot will prompt you to enter commands if u do it wrong by any chance 😊",inline=False)
        if arg=='hangman' or arg==';hangman':
            embd=discord.Embed(title="Funbot help menu",description="Hangman",colour=0x05D5FA)
            embd.add_field(name=";hangman",value="This command starts a new game of hangman or it shows the existing game ")
        if arg=='hm' or arg==';hm':
            embd=discord.Embed(title="Funbot help menu",description="Hangman",colour=0x05D5FA)
            embd.add_field(name=';hm',value='(You can opt to not use command and just type guess or letter in the chat)\nThis command allows the user to place their guess in the game,\nYou can either guess letters or a whole word.\nUsed as follows: `;hm <guess_word>` or `;hm <letter>` ',inline=False)
        if arg=="gtop" or arg==';gtop' or arg==';gtop' or arg==';glb' or arg=='glb' or arg==';gsb' or arg=='gsb':
            embd=discord.Embed(title="Funbot help menu",description="Global Leaderboard",colour=0x05D5FA)
            embd.add_field(name=';gtop',value="Shows the global leaderboard but only shows the name of people in server along with their global ranking for privacy reasons. \nUsed as follows: `;gtop <game> <category>`. Alternate command names `;glb`,`;gsb` \nAvailable games: `hangman or hang, counting or count, dum or dumb and ut or ttt or tic (for universal tic-tac-toe)` and categories of games are in ;lb help")
        if arg=='jklm' or arg==';jklm':
            embd=discord.Embed(title="Funbot help menu",description="JKLM.FUN",colour=0x05D5FA)
            embd.add_field(name=";jklm",value="Shows the game rooms in jklm.fun with atleast 3 players in it. By default it shows english: bombparty rooms,\ncan be used as follows to show rooms of different languages and popsauce game too.`;jklm <language> <game_name>` (as of now the languages are english/eng, espanol/spanish/esp, french/fr  and game_names are bombparty/bp, popsauce/ps)")
        if arg==";kick" or arg=="kick" or arg==";slap" or arg=="slap" or arg==";punch" or arg=="punch" or arg=="poke" or arg==";poke":
            embd=discord.Embed(title="Funbot help menu",description="Action",colour=0x05D5FA)
            embd.add_field(name=f"{arg}",value=f"😒 Sends gifs, ||the fact that i had to write this part of the code is stupid||\nUse: ;{arg.strip(';')} @username \n||bro don't use em, these are really dumb||")
        if arg==";d" or arg=="d":
            embd=discord.Embed(title="Funbot help menu",description="Meaning",colour=0x05D5FA)
            embd.add_field(name=";d",value="Shows meaning of a word used with the command. \nUsed as follows: `;d <word>`\n\n currently uses free version of merriam webster")
        if arg==";leaderboard" or arg=="leaderboard" or arg==";lb" or arg==";sb" or arg=="top" or arg=="scoreboard" or arg=="lb" or arg=="sb" or arg==";top":
            embd=discord.Embed(title="Funbot help menu",description="Server leaderboard",colour=0x05D5FA)
            embd.add_field(name=";leaderboard",value='Shows servers local leaderboard. \nUsed as follows: `;leaderboard <game> <category>` Alternate command name `;top`,`;lb`,`;sb`,`;scoreboard`\nSub-categories of each game: `ut(games,wins,loss,win% or %)`, `count(rights,wrongs,100,1000)` No sub-category in (hangman,dum)')
        if arg==";echo" or arg=="echo":
            embd=discord.Embed(title="Funbot help menu",description="Echo ",colour=0x05D5FA)
            embd.add_field(name=";echo",value="This command makes the bot to repeat any message passed with the command.\nUsed as follows: `;echo <message you want the bot to repeat>`")
        if arg==';feedback' or arg=='feedback' or arg=='fb' or arg==';fb' or arg=='suggestion' or arg==';suggestion':
            embd=discord.Embed(title="Funbot help menu",description="Feedback",colour=0x05D5FA)
            embd.add_field(name=';feedback',value="Send feedback to the developer, (hopefully i will solve the issues)\n\nUsed as follows: `;feedback <enter the feedback and suggestions u have related to Funbot>`. Alternate command name `;fb` or `;suggestion`",inline=False)
        if arg=='number' or arg==';number':
            embd=discord.Embed(title="Funbot help menu",description="counting",colour=0x05D5FA)
            embd.add_field(name=";number",value="This command shows the last correctly counted number and the user who has made the count\nUsed as follows: `;number` ")
        if arg=='disable_command' or arg==';disable_command':
            embd=discord.Embed(title="Funbot help menu",description="Disabling commands of the bot",colour=0x05D5FA)
            embd.add_field(name=";disable_command",value="This command disables specified command\nUsed as follows: `;disable_command <command name>`\nonly admin and moderators can use this command and this disables all the related commands too")
        if arg=='enable_command' or arg==';enable_command':
            embd=discord.Embed(title="Funbot help menu",description="Enabling commands of the bot",colour=0x05D5FA)
            embd.add_field(name=";enable_command",value="This command enables specified command\nUsed as follows: `;enable_command <command name>`\nonly admin and moderators can use this command and this enables all related other realted commands too")
        if arg=='change_channel' or arg==';change_channel':
            embd=discord.Embed(title="Funbot help menu",description="Disabling commands of the bot",colour=0x05D5FA)
            embd.add_field(name=";change_channel",value="This command changes the channel associated with the command (games and counting)\nUsed as follows: `;change_channel <command_name> <channel_name> \nonly admin and moderators can use this command ")
        if arg=='endut' or arg==';endut':
            embd=discord.Embed(title="Funbot help menu",description="ends the current ultimate tic-tac-toe game",colour=0x05D5FA)
            embd.add_field(name=";endut",value="This command ends the ongoing ultimate tic-tac-toe game. If the player next to play uses the command it is forefeit and they loose the game. \nUsed as follows: `;endut` \nonly admin, moderators and two players of ongoing game can use this command.")


    embd.set_thumbnail(url='https://image.tensorartassets.com/cdn-cgi/image/q=85,w=500/model_showcase/633542774903536154/07c56f38-e0fb-02d2-42d5-d746f6c4678a.jpeg')
    embd.set_footer(text=f"feel free to give suggestions and feedbacks(use ;feedback) 😇") 
    await ctx.send(embed=embd)  

#--------------------------------------------------------------------------------------- 
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # await ctx.send("Sorry, I don't recognize that command.")
        pass
    else:
        print(f"An error occurred: {error}")
#----------------------------------------- 


client.run(TOKEN_TEST)