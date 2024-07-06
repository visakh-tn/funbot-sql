import json
import sqlite3
f=open('hangman.json','r')
game=json.load(f)
game_stat=game

class hangmanc:
    
    
    global game_stat
    def get_word(g_id):
        f=open('hangman.json','r')
        game=json.load(f)
        game_stat=game
        return game_stat.get(str(g_id)).get("word")
    def get_lisguess(g_id):
        f=open('hangman.json','r')
        game=json.load(f)
        game_stat=game
        return game_stat.get(str(g_id)).get("lisguess")
    def get_wrong(g_id):
        f=open('hangman.json','r')
        game=json.load(f)
        game_stat=game
        return game_stat.get(str(g_id)).get("wrong")
    def check_gid(g_id):
        f=open('hangman.json','r')
        game=json.load(f)
        game_stat=game
        # print(game_stat.keys)
        if str(g_id) in list(game_stat.keys()):
            print(g_id,"in hang append...")
            return True
        else:
            print("gid not in the dictionary...")
            return False

    def reset_stat(g_id):
        print("resetting")
        d={"word":"","lisguess":[],"wrong":0}
        game_stat.update({str(g_id):d})
        file=open('hangman.json','w')
        json.dump(game_stat,file,indent=2)
        file.close()
    def add_wrong(g_id):
        f=open('hangman.json','r')
        game=json.load(f)
        game_stat=game
        words=game_stat.get(str(g_id)).get("word")
        lis=game_stat.get(str(g_id)).get("lisguess")
        w=game_stat.get(str(g_id)).get("wrong")
        w=w+1
        f.close()
        game_stat.update({str(g_id):{"word":words,"lisguess":lis,"wrong":w}})
        file=open('hangman.json','w')
        json.dump(game_stat,file,indent=2)
        file.close()
    def update_lisguess(g_id,li):
        print("updating lisguess")
        f=open('hangman.json','r')
        game=json.load(f)
        game_stat=game
        words=(game_stat.get(str(g_id))).get("word")
        w=(game_stat.get(str(g_id))).get("wrong")
        f.close()
        game_stat.update({str(g_id):{"word":words,"lisguess":li,"wrong":w}})
        file=open('hangman.json','w')
        json.dump(game_stat,file,indent=2)
        file.close()
        print("updated lisguess")

    def update_word(g_id,word):
        
        d={"word":word,"lisguess":[],"wrong":0}
        game_stat.update({str(g_id):d})
        file=open('hangman.json','w')
        json.dump(game_stat,file,indent=2)
        file.close()
        # print(word)
    
    def append_guild(g_id):
        d={"word":" ","lisguess":[],"wrong":0}
        game_stat[str(g_id)]=d
        file=open('hangman.json','w')
        json.dump(game_stat,file,indent=2)
        file.close()
        
class points:
    def update_pt(p_id,pt):
        with open('h_points.json','r') as f:
            pts=json.load(f)
        p=pts.get(str(p_id))
        p=p+pt
        pts.update({str(p_id):p})
        with open('h_points.json','w') as file:
            json.dump(pts,file,indent=2)
    
    def check_pid(p_id):
        with open('h_points.json','r') as f:
            pts=json.load(f)
        if str(p_id) in list(pts.keys()):
            return True
        else:
            return False
        

    def append_pid(p_id):
        with open('h_points.json','r') as f:
            pts=json.load(f)
            pts[str(p_id)]=0
        with open('h_points.json','w') as file:
            json.dump(pts,file)
    
    def show_pt(p_id):
        with open('h_points.json','r') as f:
            pts=json.load(f)
        return pts.get(str(p_id))

#----------------- SQLITE3 --------------------------

class hangmansql:
    def __init__(self):
        pass
    def make_table(self):
        con = sqlite3.connect("funbot.db")
        cr=con.cursor()
        cr.execute("CREATE TABLE hangman (g_id,ch_id,word,lisguess,wrongs)")
        con.commit()
    def create_game(self,gid,wrd="",lisguess=[],wrong=0):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("SELECT g_id FROM hangman WHERE g_id=?",(gid,))
        result = cr.fetchall()
        if result:
            cr.execute("UPDATE hangman SET word=?,lisguess=?,wrongs=? WHERE g_id=?", (wrd, json.dumps(lisguess), wrong,result[0][0]))
        else:
            guessed = json.dumps(lisguess)
            cr.execute("INSERT INTO hangman (g_id,word,lisguess,wrongs)VALUES(?,?,?,?)", (gid, wrd, guessed, wrong))
        con.commit()

    def reset_game(self,gid):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("UPDATE hangman SET word=NULL,lisguess=?,wrongs=? WHERE g_id=?",(json.dumps([]),0,gid))
        con.commit()

    def update_hangman(self,gid,col_name,value):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        sql = f"UPDATE hangman SET {col_name} = ? WHERE g_id = {gid}"
        cr.execute(sql,(value,))
        con.commit()

    def get_hangman(self,gid):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("SELECT * FROM hangman WHERE g_id=?",(gid,))
        result = cr.fetchone()
        if result:
            hangman_stat = {"word":result[2],"lisguess":json.loads(result[3]),"wrongs":result[4]}
        else:
            hangman_stat = None
        return hangman_stat
