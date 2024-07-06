import json
# required variables for the game=
        # game_dict
        # nxtbox
        # nxtplayer
        #player_1 and player_2 ID
        # is the game_on
class game_stat_ttt:
        def __init__(self) -> None:
                pass
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #GET STATS---------------------------------------------------

        def get_game_dict(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("game_dict")
        
        def get_x_win(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("x_win")


        def get_o_win(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("o_win")
        

        def get_d_game(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("d_game")
        
        def get_p_game(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("p_game")

        def get_nxtbox(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("nextbox")
        def get_nxtplayer(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("nextplayer")
        def get_p1(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("player_1")
        def get_p2(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("player_2")
        def isgameon(g_id):
                with open('tictactoe.json','r') as file:
                        game_stat=json.load(file)
                        game=game_stat.get(str(g_id))
                return game.get("game_on")

        #UPDATE GAME STATS------------------------------------------------


        def update_game_dict(g_id, game):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["game_dict"] = game

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)

        

        def update_x_win(g_id, xwin):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["x_win"] = xwin

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
        
        def update_o_win(g_id, owin):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["o_win"] = owin

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)



        def update_d_game(g_id, dgame):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["d_game"] = dgame

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
        
        def update_p_game(g_id, pgame):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["p_game"] = pgame

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
        


        def update_nxtbox(g_id, nxtbox):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["nextbox"] = nxtbox

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
        
        def update_nxtplayer(g_id, nxtplayer):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["nextplayer"] = nxtplayer

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
        
        def update_players(g_id, p1,p2):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["player_1"] = p1
                data[str(g_id)]["player_2"] = p2

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
        
        def update_gameon(g_id,game_status):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                data[str(g_id)]["game_on"] = game_status

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
#-----------------------------------------------------------------------
#RESET FOR NEW GAME-----------------------------------------------------
        def reset_stat(g_id):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)
                game={"game_dict":None,"x_win":[],"o_win":[],"d_game":[],"p_game":[],"nextbox":9,"nextplayer":None,"player_1":None,"player_2":None,"game_on":0}
                data[str(g_id)] = game

                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
        def is_new(g_id):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)
                gid=list(data.keys())
                if str(g_id) in gid:
                        return False
                else:
                        return True
        def add_new(gid,p1,p2):
                with open('tictactoe.json', 'r') as file:
                        data = json.load(file)

                game={"game_dict":None,"x_win":[],"o_win":[],"d_game":[],"p_game":[],"nextbox":9,"nextplayer":None,"player_1":p1,"player_2":p2,"game_on":1}

                
                data[str(gid)]=game
                with open('tictactoe.json', 'w') as file:
                        json.dump(data, file, indent=2)
#---------------------------------------------------------------------------
#