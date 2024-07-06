# -------------------------------------------------------

# -----------------------------------------------------
import discord
from discord.ext import commands
import json
import copy
from tokens import *
from PIL import Image
from io import BytesIO
from ttt import game_stat_ttt
from channel_ids import IdClass_new  # DONE
from score import scoreboard

# from test import TTT

#-----------------------------------------------------

class uttt(commands.Cog):
    def __init__(self,client:commands.Bot):
            self.client=client

    def getsquare(self):
        square=Image.new('RGB',(700,700),(220,220,200))
        gameboard=Image.open('gameboard.png')
        square.paste(gameboard,(50,50),gameboard)

        return square

    def locate(self,box_no):
        row=box_no//3
        col=box_no%3
        return (row,col)
    
    
    def display_ttt(self,game_dict,nbox,drawgame,xwin,owin,pgame):
        square=self.getsquare()
        box=[]
        nxgrid=self.locate(nbox)
        box_li=[[0,1,2],[3,4,5],[6,7,8]]
        x=50
        for i in range(3):
            y=50
            k=0
            for j in box_li[k]:
                box.append((x,y))
                y+=66
            k+=1
            x+=66
        games_list=list(game_dict.values())


        O66 = Image.open('O66.png').convert("RGBA")
        X66 = Image.open('X66.png').convert("RGBA")

        cell_size = 66
        games=[]
        for m in games_list:
            grid = Image.open('3x3grid.png').convert("RGBA")

            for i in range(3):
                for j in range(3):
                    if m[i][j] == 1:
                        grid.paste(X66, ((j * cell_size) + 3, (i * cell_size) + 5), mask=X66.split()[3])
                    elif m[i][j] == 2:
                        grid.paste(O66, ((j * cell_size) + 3, (i * cell_size) + 5), mask=O66.split()[3])
            games.append(grid)


        #----------------------------------------------------------------------------------------------------------------------------

        nextgrid = Image.open('3x3nextbox.png').convert("RGBA")

        grid_size=198
        k=0
        for i in range(3):
            for j in range(3):
                square.paste(games[k], ((j * grid_size) + 50, (i * grid_size) + 50), mask=games[k].split()[3])
                k+=1


        if nbox !=9:
            square.paste(nextgrid, ((nxgrid[1] * grid_size) + 50, (nxgrid[0] * grid_size) + 50), mask=nextgrid.split()[3])
    #-----------------------------------------------------------------------------------------------------------------------------------
        drawgrid=Image.open('3x3draw.png').convert("RGBA")

        for k in range(9):
            if k in drawgame:
                drawloc=self.locate(k)
                square.paste(drawgrid, ((drawloc[1] * grid_size) + 53, (drawloc[0] * grid_size) + 53), mask=drawgrid.split()[3])

    #---------------------------------------------------------------------------------------------------------------------------------
        #to mark the grid where X won
        xgrid=Image.open('X198.png').convert("RGBA")

        for k in range(9):
            if k in xwin:
                xloc=self.locate(k)
                square.paste(xgrid, ((xloc[1] * grid_size) + 50, (xloc[0] * grid_size) + 50), mask=xgrid.split()[3])

    # ---------------------------------------------------------------------------------------------------------------------------------
        # to mark the grid where O won
        ogrid = Image.open('O198.png').convert("RGBA")

        for k in range(9):
            if k in owin:
                oloc = self.locate(k)
                square.paste(ogrid, ((oloc[1] * grid_size) + 50, (oloc[0] * grid_size) + 50), mask=ogrid.split()[3])

    #------------------------------------------------------------------------------------------------------------------------------
        #to mark the grid where the game is PENDING for the user to select if nextbox is upto the player
        if nbox == 9:
            pgrid = Image.open('3x3nextbox.png').convert("RGBA")

            for k in range(9):
                if k in pgame:
                    ploc = self.locate(k)
                    square.paste(pgrid, ((ploc[1] * grid_size) + 52, (ploc[0] * grid_size) + 53), mask=pgrid.split()[3])

        return  square  


#--------------------------------------------------------------------------------------------------------------------  
    
    def display_current_game(self,game_dict,nbox,drawgame,xwin,owin,pgame):
        square=self.getsquare()
        box=[]
        nxgrid=self.locate(nbox)
        box_li=[[0,1,2],[3,4,5],[6,7,8]]
        x=50
        for i in range(3):
            y=50
            k=0
            for j in box_li[k]:
                box.append((x,y))
                y+=66
            k+=1
            x+=66
        games_list=list(game_dict.values())


        O66 = Image.open('O66.png').convert("RGBA")
        X66 = Image.open('X66.png').convert("RGBA")

        cell_size = 66
        games=[]
        for m in games_list:
            grid = Image.open('3x3grid.png').convert("RGBA")

            for i in range(3):
                for j in range(3):
                    if m[i][j] == 1:
                        grid.paste(X66, ((j * cell_size) + 3, (i * cell_size) + 5), mask=X66.split()[3])
                    elif m[i][j] == 2:
                        grid.paste(O66, ((j * cell_size) + 3, (i * cell_size) + 5), mask=O66.split()[3])
            games.append(grid)


        #----------------------------------------------------------------------------------------------------------------------------

        nextgrid = Image.open('3x3nextbox.png').convert("RGBA")

        grid_size=198
        k=0
        for i in range(3):
            for j in range(3):
                square.paste(games[k], ((j * grid_size) + 50, (i * grid_size) + 50), mask=games[k].split()[3])
                k+=1


        if nbox !=9:
            square.paste(nextgrid, ((nxgrid[1] * grid_size) + 50, (nxgrid[0] * grid_size) + 50), mask=nextgrid.split()[3])
    #-----------------------------------------------------------------------------------------------------------------------------------
        drawgrid=Image.open('3x3draw.png').convert("RGBA")

        for k in range(9):
            if k in drawgame:
                drawloc=self.locate(k)
                square.paste(drawgrid, ((drawloc[1] * grid_size) + 53, (drawloc[0] * grid_size) + 53), mask=drawgrid.split()[3])

    #---------------------------------------------------------------------------------------------------------------------------------
        #to mark the grid where X won
        xgrid=Image.open('X198.png').convert("RGBA")

        for k in range(9):
            if k in xwin:
                xloc=self.locate(k)
                square.paste(xgrid, ((xloc[1] * grid_size) + 50, (xloc[0] * grid_size) + 50), mask=xgrid.split()[3])

    # ---------------------------------------------------------------------------------------------------------------------------------
        # to mark the grid where O won
        ogrid = Image.open('O198.png').convert("RGBA")

        for k in range(9):
            if k in owin:
                oloc = self.locate(k)
                square.paste(ogrid, ((oloc[1] * grid_size) + 50, (oloc[0] * grid_size) + 50), mask=ogrid.split()[3])

    #------------------------------------------------------------------------------------------------------------------------------
        #to mark the grid where the game is PENDING for the user to select if nextbox is upto the player
        if nbox == 9:
            pgrid = Image.open('3x3nextbox.png').convert("RGBA")

            for k in range(9):
                if k in pgame:
                    ploc = self.locate(k)
                    square.paste(pgrid, ((ploc[1] * grid_size) + 50, (ploc[0] * grid_size) + 50), mask=pgrid.split()[3])

        return  square 


    # --------------------------------------------------------------------------------------------------------------
    def straight(self,li1):
        win = 0
        for i in range(3):
            if (li1[i][0] == li1[i][1] == li1[i][2] != 0):
                win = li1[i][1]
                return win
        for i in range(3):
            if (li1[0][i] == li1[1][i] == li1[2][i] != 0):
                win = li1[0][i]
                return win
        if (win == 0):
            return win


    def diagonal(self,li1):
        win = 0
        if (li1[0][0] == li1[1][1] == li1[2][2] != 0):
            win = li1[1][1]
            return win
        if (li1[0][2] == li1[1][1] == li1[2][0] != 0):
            win = li1[1][1]
            return win
        if (win == 0):
            return win


    def draw(self,li1):  # executes only if win conditions are 0
        dr = 3
        cont = 4
        if any(0 in check for check in li1):
            return dr  # not draw continue dr=3
        else:
            return cont  # draw dr=4


    def win(self,li1):
        a = self.straight(li1)
        b = self.diagonal(li1)
        dr = self.draw(li1)
        if (a):
            return a  # b wins
        elif (b):
            return b  # d wins
        elif (b == 0 and a == 0):
            if (dr == 4):
                return dr  # draw
            if dr == 3:
                return dr  # not draw


    # ------------------------------------------------------
    # ENTERS THE INPUT FROM PLAYERS TO THE
    def entry(self,mark, gno, loc):
        global game_dict
        g = copy.deepcopy(game_dict.get(f'game{gno}', []))
        if g[loc[0]][loc[1]] != 0:
            return False
        res = self.win(g)
        g[loc[0]][loc[1]] = mark

        if (res == 1 or res == 2 or res == 4):
            isplayable = False
        else:
            isplayable = True

        if (isplayable):
            game_dict[f"game{gno}"] = g
            return True
        else:
            return False


    # -------------------------------------------------------
    # FINDS THE NEXT BOX TO PLAY
    def nextbox(self,loc):
        global game_dict
        nbox = loc[0] * 3 + loc[1]
        g = game_dict.get(f"game{nbox}")
        res = self.win(g)
        if (res == 1 or res == 2 or res == 4):
            return 9
        else:
            return nbox

        # FULL BOARD RESULT COMPILATION
    def b_res(self):
        global game_dict, X_wins, O_wins, B_draw, pending_game
        X_wins=[]
        O_wins=[]
        B_draw=[]
        pending_game=[]
        for i in range(9):
            game = game_dict.get(f"game{i}")

            if self.win(game) == 1:
                if i not in X_wins:
                    X_wins.append(i)
            if self.win(game) == 2:
                if i not in O_wins:
                    O_wins.append(i)
            if self.win(game) == 4:
                if i not in B_draw:
                    B_draw.append(i)
            if self.win(game) == 3:
                if i not in pending_game:
                    pending_game.append(i)


    # ------------------------------------------------------

    # GAME FINAL RESULT
    def B_straight(self,X, O):
        horizontal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        vertical = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
        winner = 0
        for i in horizontal:
            if ((i[0] in X) and (i[1] in X) and (i[2] in X)):
                winner = 1
                break
            elif ((i[0] in O) and (i[1] in O) and (i[2] in O)):
                winner = 2
                break
        for i in vertical:
            if ((i[0] in X) and (i[1] in X) and (i[2] in X)):
                winner = 1
                break
            elif ((i[0] in O) and (i[1] in O) and (i[2] in O)):
                winner = 2
                break

        return winner


    # ---------------------------------------
    def B_diagonal(self,X, O):
        winner = 0
        diagonal = [[0, 4, 8], [2, 4, 6]]
        for i in diagonal:
            if ((i[0] in X) and (i[1] in X) and (i[2] in X)):
                winner = 1
                break
            elif ((i[0] in O) and (i[1] in O) and (i[2] in O)):
                winner = 2
                break
        return winner

#==========================================================================================================================        

    @commands.command(name="ut", brief="starts a new game of ultimate tic-tac-toe", help=";ut @username starts a new game with the mentioned username")
    async def ut(self,ctx,*,member:discord.Member=None):

#----------- CHECKING IF COMMAND IS DISABLED -----------------------------------------------------------------
        cidc = IdClass_new()
        sb = scoreboard()
        all_channels = cidc.get_table()

        ttt_channel_id= {g_data[0]:g_data[3] for g_data in all_channels}
        disabled_commands = {g_data[0]:json.loads(g_data[6]) for g_data in all_channels}

        if "ttt" in disabled_commands[ctx.guild.id] or "ut" in disabled_commands[ctx.guild.id]:
            return
        if ctx.channel.id != ttt_channel_id[ctx.guild.id]:
            return
        
#------------------------------------------------------------------------------------------------------------
        if member==None:
            if not (game_stat_ttt.isgameon(ctx.guild.id)):
                await ctx.send("There is no game in progress")
                return
            # ------------------------------------------------------------
            game_board=game_stat_ttt.get_game_dict(ctx.guild.id)
            np=game_stat_ttt.get_nxtplayer(ctx.guild.id)
            nb=game_stat_ttt.get_nxtbox(ctx.guild.id)
            pgame=game_stat_ttt.get_p_game(ctx.guild.id)
            xwin=game_stat_ttt.get_x_win(ctx.guild.id)
            owin=game_stat_ttt.get_o_win(ctx.guild.id)
            dgame=game_stat_ttt.get_d_game(ctx.guild.id)
            board_image=self.display_current_game(game_board,nb,dgame,xwin,owin,pgame)
            image_bytes = BytesIO()
            board_image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            embed = discord.Embed(title="Game board", description=" ",colour=0x05D5FA)
            embed.add_field(name=" ",value=f"next to play is <@{np}>")

            # Attach the image to the embed
            embed.set_image(url='attachment://board_image.png')

            # Create a Discord file object
            board_file = discord.File(image_bytes, filename='board_image.png')

            # Send the embed with the attached image to a Discord channel
            await ctx.send(embed=embed, file=board_file)
            #-----------------------------------------------------------------
            return
        
        if game_stat_ttt.is_new(ctx.guild.id):
            

            global p1,p2
            p1=ctx.author.id
            p2=member.id
            game_stat_ttt.add_new(ctx.guild.id,p1,p2)
            game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            game_dict = {"game0": game}
            for i in range(9):
                g = f"game{i}"
                if g in game_dict.keys():
                    continue
                else:
                    game_dict.update({g: game})
            
            await ctx.send(f"<@{p1}> is ❌ \n<@{p2}> is 🟢")
            sb.add_point(pid=p1,col_name="t_games")
            sb.add_point(pid=p2,col_name="t_games")
            global nxtplayer
            nxtplayer=p1

            board_image=self.display_ttt(game_dict,9,[],[],[],[])
            image_bytes = BytesIO()
            board_image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            embed = discord.Embed(title="Game board", description="Game initiated",colour=0x05D5FA)
            embed.add_field(name=" ",value=f"<@{nxtplayer}>, its your turn now")

            # Attach the image to the embed
            embed.set_image(url='attachment://board_image.png')

            # Create a Discord file object
            board_file = discord.File(image_bytes, filename='board_image.png')

            # Send the embed with the attached image to a Discord channel
            await ctx.send(embed=embed, file=board_file)
            
            game_stat_ttt.update_game_dict(ctx.guild.id,game_dict)
            game_stat_ttt.update_nxtplayer(ctx.guild.id,nxtplayer)
            # Send the image directly using discord.File
            # await ctx.send(file=discord.File(image_bytes, 'imag.png'))
            return
        else:
            if game_stat_ttt.isgameon(ctx.guild.id):
                await ctx.send("There is an ongoing currently please wait till the game finishes")  # CONVERT THIS TO EMBED
                await ctx.send("You can request the moderators, admins or one of the 2 players to end the game using command ;endut or ")
                
                return
            else:
                
                p1=ctx.author.id
                p2=member.id
                game_stat_ttt.add_new(ctx.guild.id,p1,p2)
                game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                game_dict = {"game0": game}
                for i in range(9):
                    g = f"game{i}"
                    if g in game_dict.keys():
                        continue
                    else:
                        game_dict.update({g: game})
                
                await ctx.send(f"<@{p1}> is ❌ \n<@{p2}> is 🟢")
                sb.add_point(pid=p1,col_name="t_games")
                sb.add_point(pid=p2,col_name="t_games")

                board_image=self.display_ttt(game_dict,9,[],[],[],[])
                image_bytes = BytesIO()
                board_image.save(image_bytes, format='PNG')
                image_bytes.seek(0)
                embed = discord.Embed(title="Game board", description="Game initiated",colour=0x05D5FA)
                nxtplayer=p1

                # Attach the image to the embed
                embed.set_image(url='attachment://board_image.png')
                embed.add_field(name=" ",value=f"<@{nxtplayer}>, its your turn now")

                # Create a Discord file object
                board_file = discord.File(image_bytes, filename='board_image.png')

                # Send the embed with the attached image to a Discord channel
                await ctx.send(embed=embed, file=board_file)
                
                
                game_stat_ttt.update_game_dict(ctx.guild.id,game_dict)
                game_stat_ttt.update_nxtplayer(ctx.guild.id,nxtplayer)
                # Send the image directly using discord.File
                # await ctx.send(file=discord.File(image_bytes, 'imag.png'))
                return


    
    @commands.command(name="t", brief="command to mark your symbol in the game", help=";t <game number(1-9)> <location(1-9)>. game number is needed only if there is a possibility of multiple possible game selection, else only location and the game number is indicated by the green box")
    async def t(self,ctx,args1=None,args2=None):
#----------- CHECKING IF COMMAND IS DISABLED -----------------------------------------------------------------
        cidc = IdClass_new()
        sb = scoreboard()
        all_channels = cidc.get_table()

        ttt_channel_id= {g_data[0]:g_data[3] for g_data in all_channels}
        disabled_commands = {g_data[0]:json.loads(g_data[6]) for g_data in all_channels}

        if "ttt" in disabled_commands[ctx.guild.id] or "ut" in disabled_commands[ctx.guild.id]:
            return    
#--------------------------------------------------------------------------------------------------

        p=ctx.author.id
        
        global nxtbox,nxtplayer,game_dict
        p1=game_stat_ttt.get_p1(ctx.guild.id)
        p2=game_stat_ttt.get_p2(ctx.guild.id)
        game_dict=game_stat_ttt.get_game_dict(ctx.guild.id)
        nxtbox=game_stat_ttt.get_nxtbox(ctx.guild.id)
        nxtplayer=game_stat_ttt.get_nxtplayer(ctx.guild.id)


        # TO CHECK IF THERE IS AN ONGOING GAME
        if not (game_stat_ttt.isgameon(ctx.guild.id)):
            await ctx.send("there is no game in progress, use ;ut @opponent for starting a new game")
            return
        # TO CHECK IF ITS THE RIGHT PLAYER IS MARKING 
        if p != nxtplayer:
            await ctx.send(f"It is not ur turn, its <@{nxtplayer}> 's turn")
            
            if p!=p1 and p!=p2:
                await ctx.send("pls wait for the game to finish and start a new game using ```;ut @opponent```")
                return
            return
        # CONFIRMING THE RIGHT PLAYER IS PLAYING
        if p == nxtplayer:
            # IF NEXT GAME IS NOT KNOWN, THEN THE PLAYER CAN CHOOSE THE BOX
            if nxtbox==9:
                # IN CASE OF EMPTY COMMAND
                if args1==None and args2==None:
                    await ctx.send("enter the command in this format: `;t <game_number>< ><location>` ")
                    return
                # PLAYER WILL HAVE TO GIVE GAME NUMBER AND LOCAITON
                elif args1==None or args2==None:
                    await ctx.send("enter the command in this format: `;t <game_number>< ><location>` ")
                    return
                else:
                    arg1=int(args1)
                    arg2=int(args2)
                    box_num=arg1-1
                    loc_p=self.locate(arg2-1)
                    if p==p1:
                        if self.entry(1,box_num,loc_p):
                            nxtbox=self.nextbox(loc_p)
                            nxtplayer=p2
                            game_stat_ttt.update_game_dict(ctx.guild.id,game_dict)
                            game_stat_ttt.update_nxtbox(ctx.guild.id,nxtbox)
                            game_stat_ttt.update_nxtplayer(ctx.guild.id,nxtplayer)
                    else:
                        if self.entry(2,box_num,loc_p):
                            nxtbox=self.nextbox(loc_p)
                            nxtplayer=p1
                            game_stat_ttt.update_game_dict(ctx.guild.id,game_dict)
                            game_stat_ttt.update_nxtbox(ctx.guild.id,nxtbox)
                            game_stat_ttt.update_nxtplayer(ctx.guild.id,nxtplayer)
            
            # IF THE NEXT BOX IS KNOWN, THE PLAYER NEEDS TO ENTER ONLY THE LOCATION 
            else:
                if args1==None and args2==None:              #checking for empty command
                    await ctx.send("enter the command in the format: `;t <location>`")
                    return
                elif args1!=None and args2!=None:            #next box is known so get only the locaiton
                    await ctx.send(f"the game number is {nxtbox +1}, please enter only the location (`;t <location>`)")
                    return
                else:
                    arg1=int(args1)

                    loc_p=self.locate(arg1-1)
                    box_num=nxtbox
                    if p==p1:
                        if self.entry(1,box_num,loc_p):
                            nxtbox=self.nextbox(loc_p)
                            nxtplayer=p2
                            game_stat_ttt.update_game_dict(ctx.guild.id,game_dict)
                            game_stat_ttt.update_nxtbox(ctx.guild.id,nxtbox)
                            game_stat_ttt.update_nxtplayer(ctx.guild.id,nxtplayer)
                        else:
                            await ctx.send("invalid entry")
                    else:
                        if self.entry(2,box_num,loc_p):
                            nxtbox=self.nextbox(loc_p)
                            nxtplayer=p1
                            game_stat_ttt.update_game_dict(ctx.guild.id,game_dict)
                            game_stat_ttt.update_nxtbox(ctx.guild.id,nxtbox)
                            game_stat_ttt.update_nxtplayer(ctx.guild.id,nxtplayer)
                        else:
                            await ctx.send("invalid entry")
        
        self.b_res()
        game_stat_ttt.update_x_win(ctx.guild.id,X_wins)
        game_stat_ttt.update_o_win(ctx.guild.id,O_wins)
        game_stat_ttt.update_d_game(ctx.guild.id,B_draw)
        game_stat_ttt.update_p_game(ctx.guild.id,pending_game)
        st_win=self.B_straight(X_wins,O_wins)
        d_win=self.B_diagonal(X_wins,O_wins)

        if st_win == 1 or d_win == 1:
            winner = 1
            
            board_image = self.display_ttt(game_dict, nxtbox, B_draw, X_wins, O_wins,pending_game)
            image_bytes = BytesIO()
            board_image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            embed = discord.Embed(title="Game board", description="marked",colour=0x05D5FA)
            embed.add_field(name=" ",value=f"<@{p1}> WINS LTES GOOOOOOOOOOOOOOO 🎂 🎊 🎉 ✨ 🙌 ")
            sb.add_point(pid=p1,col_name="t_win")
            sb.add_point(pid=p2,col_name="t_loss")

            # Attach the image to the embed
            embed.set_image(url='attachment://board_image.png')

            # Create a Discord file object
            board_file = discord.File(image_bytes, filename='board_image.png')

            # Send the embed with the attached image to a Discord channel
            await ctx.send(embed=embed, file=board_file)
            # await ctx.send(file=discord.File(image_bytes, 'img.png'))
            game_stat_ttt.reset_stat(ctx.guild.id)
            return
        if st_win == 2 or d_win == 2:
            winner = 2
            
            board_image = self.display_ttt(game_dict, nxtbox, B_draw, X_wins, O_wins,pending_game)
            image_bytes = BytesIO()
            board_image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            embed = discord.Embed(title="Game board", description="marked",colour=0x05D5FA)
            embed.add_field(name=" ",value=f"<@{p2}> WINS LTES GOOOOOOOOOOOOOOO 🎂 🎊 🎉 ✨ 🙌 ")
            sb.add_point(pid=p2,col_name="t_win")
            sb.add_point(pid=p1,col_name="t_loss")

            # Attach the image to the embed
            embed.set_image(url='attachment://board_image.png')

            # Create a Discord file object
            board_file = discord.File(image_bytes, filename='board_image.png')

            # Send the embed with the attached image to a Discord channel
            await ctx.send(embed=embed, file=board_file)
            # await ctx.send(file=discord.File(image_bytes, 'img.png'))
            game_stat_ttt.reset_stat(ctx.guild.id)
            return
        if st_win == 0 and d_win == 0:
            if len(pending_game) == 0:
                winner = 3
                
                board_image = self.display_ttt(game_dict, nxtbox, B_draw, X_wins, O_wins,pending_game)
                image_bytes = BytesIO()
                board_image.save(image_bytes, format='PNG')
                image_bytes.seek(0)
                embed = discord.Embed(title="Game board", description="marked",colour=0x05D5FA)
                embed.add_field(name="The game is DRAW",value=" ")

                # Attach the image to the embed
                embed.set_image(url='attachment://board_image.png')

                # Create a Discord file object
                board_file = discord.File(image_bytes, filename='board_image.png')

                # Send the embed with the attached image to a Discord channel
                await ctx.send(embed=embed, file=board_file)
                # await ctx.send(file=discord.File(image_bytes, 'img.png'))
                game_stat_ttt.reset_stat(ctx.guild.id)
                return
            winner = 4
        if len(pending_game) == 0:
            await ctx.send("game over")
            
            board_image = self.display_ttt(game_dict, nxtbox, B_draw, X_wins, O_wins,pending_game)
            image_bytes = BytesIO()
            board_image.save(image_bytes, format='PNG')
            image_bytes.seek(0)
            embed = discord.Embed(title="Game board", description="marked",colour=0x05D5FA)

            # Attach the image to the embed
            embed.set_image(url='attachment://board_image.png')
            embed.add_field(name="The game is DRAW",value=" ")

            # Create a Discord file object
            board_file = discord.File(image_bytes, filename='board_image.png')

            # Send the embed with the attached image to a Discord channel
            await ctx.send(embed=embed, file=board_file)
            # await ctx.send(file=discord.File(image_bytes, 'img.png'))
            game_stat_ttt.reset_stat(ctx.guild.id)
            return
        board_image = self.display_ttt(game_dict, nxtbox, B_draw, X_wins, O_wins,pending_game)
        image_bytes = BytesIO()
        board_image.save(image_bytes, format='PNG')
        image_bytes.seek(0)
        embed = discord.Embed(title="Game board", description="marked",colour=0x05D5FA)

        # Attach the image to the embed
        embed.set_image(url='attachment://board_image.png')
        embed.add_field(name=" ",value=f"<@{nxtplayer}>, it it your turn now")

        # Create a Discord file object
        board_file = discord.File(image_bytes, filename='board_image.png')

        # Send the embed with the attached image to a Discord channel
        await ctx.send(embed=embed, file=board_file)
        # await ctx.send(file=discord.File(image_bytes, 'img.png'))

    @commands.command()
    async def endut(self,ctx):
        sb = scoreboard()
        if any(role.name in ['Admin', 'Moderator'] for role in ctx.author.roles)  or ctx.author.id == OWNERID:
            game_stat_ttt.reset_stat(ctx.guild.id)
        else:
            p1=game_stat_ttt.get_p1(ctx.guild.id)
            p2=game_stat_ttt.get_p2(ctx.guild.id)
            nxtplayer=game_stat_ttt.get_nxtplayer(ctx.guild.id)

            if ctx.author.id == p1 or ctx.author.id == p2:
                if ctx.author.id == nxtplayer:
                    sb.add_point(pid=ctx.author.id,col_name="t_loss")
                    winner_id = p1 if p2!= ctx.author.id else p2
                    sb.add_point(pid=winner_id,col_name="t_win")
                game_stat_ttt.reset_stat(ctx.guild.id)
            else:
                await ctx.send("You cannot use the command ask server admin, moderator or one of the players to end the game")
             



async def setup(client:commands.Bot):
    await client.add_cog(uttt(client))


