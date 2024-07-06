import json
import requests
import sqlite3
from bs4 import BeautifulSoup

class scores:
    def add_score(name):
        f=open('score.json','r')
        read=json.load(f)
        score_dict=read[0]
        name_list=list(score_dict.keys())
        f.close()
        
        if name in name_list:
            points=score_dict.get(name)+1
        else: 
            points=1
        d={name:points}
        score_dict.update(d)
        file=open('score.json','w')
        li=[]
        li.append(score_dict)
        json.dump(li,file)
        file.close()
    def dumb_count(name):
        f=open('score.json','r',encoding='utf-8')
        read=json.load(f)
        score_dict=read[0]
        point=score_dict.get(name)
        f.close()
        return point
    
    def jklm(lang='ENG',g='BP'):
        url='https://jklm.fun/api/rooms'
        response = requests.get(url)
        li=[]
        
        if response.status_code == 200:
            data = response.json()
            f=open('jklm.json','w')
            json.dump(data,f,indent=2)
            def roomer(room):
                d_room['Name']=room.get('name')
                d_room['Code']=room.get('roomCode')
                d_room['Players']=room.get('playerCount')
                return d_room
            def room_disp(room_list):
                s=[]
                for i in room_list:
                    string='Name: '+i.get('Name')+' Code: '+i.get('Code')+' Players: '+str(i.get('Players'))
                    s.append(string)
                room='\n'.join(s)
                return room
            with open('jklm.json', 'r') as f:
                rooms = []
                read = json.load(f)
                public_rooms = read.get('publicRooms')

                for room in public_rooms:
                    if room.get('playerCount') > 1:
                        rooms.append(room)

                english_bp = []
                french_bp = []
                spanish_bp = []
                english_ps = []
                french_ps = []
                spanish_ps = []

                for room in rooms:
                    d_room={}
                    if room.get('gameId') == 'bombparty':
                        if room.get('details') == 'English':
                            d_room=roomer(room)
                            english_bp.append(d_room)
                        elif room.get('details') == 'French':
                            d_room=roomer(room)
                            french_bp.append(d_room)
                        elif room.get('details') == 'Spanish':
                            d_room=roomer(room)
                            spanish_bp.append(d_room)
                    elif room.get('gameId') == 'popsauce':
                        if room.get('details') == 'English':
                            d_room=roomer(room)
                            english_ps.append(d_room)
                        elif room.get('details') == 'French':
                            d_room=roomer(room)
                            french_ps.append(d_room)
                        elif room.get('details') == 'Spanish':
                            d_room=roomer(room)
                            spanish_ps.append(d_room)
            if(lang=='ENG'and g=='BP'):
                return room_disp(english_bp)
            if(lang=='FR'and g=='BP'):
                return room_disp(french_bp)
            if(lang=='ESP'and g=='BP'):
                return room_disp(spanish_bp)
            if(lang=='ENG'and g=='PS'):
                return room_disp(english_ps)
            if(lang=='FR'and g=='PS'):
                return room_disp(french_ps)
            if(lang=='ESP'and g=='PS'):
                return room_disp(spanish_ps)
       
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return 'empty'
# -----------------------------------------------------------------
class words:

    def meaning(word):
        url=f'https://www.merriam-webster.com/dictionary/{word}'
        r=requests.get(url)
        html=r.text
        soup=BeautifulSoup(html,'html.parser')
        entries = soup.find_all('div', class_='vg-sseq-entry-item')
        d=[]
        website=1
        f=["no idea"]
        def meaning_disp(d):
            s=[]
            no=1
            for i in d:
                string=f"{no}. {i}"
                s.append(string)
                no+=1
            meanings='\n'.join(s)
            return meanings
        if entries:
            for entry in entries:
                dt_text = entry.find('span', class_='dtText').text.strip().strip(':')
                d.append(dt_text)
            return meaning_disp(d),website
        else:
            url=f'https://www.urbandictionary.com/{word}'
            r=requests.get(url)
            html=r.text
            soup=BeautifulSoup(html,'html.parser')
            entries_ud = soup.find_all('div', class_='p-5 md:p-8')
            d_ud=[]
            website=2
            na=["no idea"]
            
            if entries_ud:
                for entry in entries_ud:
                    dt_text = entry.find('div', class_='break-words meaning mb-4').text.strip().strip(':')
                    d_ud.append(dt_text)
                return meaning_disp(d_ud),website
            else:
                 website=0
                 return f,website


class points:
    def update_pt(p_id, pt):
        with open('h_points.json', 'r') as f:
            pts = json.load(f)
        p = pts.get(str(p_id))
        p = p + pt
        pts.update({str(p_id): p})
        with open('h_points.json', 'w') as file:
            json.dump(pts, file, indent=2)

    def check_pid(p_id):
        with open('h_points.json', 'r') as f:
            pts = json.load(f)
        if str(p_id) in list(pts.keys()):
            return True
        else:
            return False

    def append_pid(p_id):
        with open('h_points.json', 'r') as f:
            pts = json.load(f)
            pts[str(p_id)] = 0
        with open('h_points.json', 'w') as file:
            json.dump(pts, file)

    def show_pt(p_id):
        with open('h_points.json', 'r') as f:
            pts = json.load(f)
        return pts.get(str(p_id))

class scoreboard:
    def __init__(self):
        pass

    def make_table(self):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("CREATE TABLE scores (p_id,p_name,dum,c_right,c_wrong,c_100,c_1k,hangman,t_win,t_loss,t_games)")
        con.commit()

    def add_point(self,pid,col_name,value=1,pname=None):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        sql = f"SELECT p_id FROM scores WHERE p_id = ?"
        cr.execute(sql,(pid,))
        res = cr.fetchall()
        if res:

            # ----- check if th table has the player id. if no add player with dummy data
            sql = f"SELECT {col_name} FROM scores WHERE p_id = ?"
            cr.execute(sql,(pid,))
            result = cr.fetchone()
            if result:
                score = result[0]
                sql = f"UPDATE scores SET {col_name} = ? WHERE p_id = ?"
                cr.execute(sql,(score+value,pid))
                con.commit()
            else:
                sql = f"INSERT INTO scores ({col_name}) VALUES(?) WHERE p_id =?"
                cr.execute(sql,(value,pid))
                con.commit()
        else:
            self.add_player(pid,pname)
            self.add_point(pid,col_name,value=value)


    def add_player(self,pid,pname=None):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("INSERT INTO scores (p_id,p_name,dum,c_right,c_wrong,c_100,c_1k,hangman,t_win,t_loss,t_games)VALUES(?,?,0,0,0,0,0,0,0,0,0);",(pid,pname))
        con.commit()

    def update_score(self,pid,col_name,value):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        sql = f"UPDATE scores SET {col_name} = ? WHERE p_id = ?"
        cr.execute(sql,(value,pid))
        con.commit()

    def get_score(self,pid,col_name):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        sql = f"SELECT {col_name} FROM scores WHERE p_id = ?"
        cr.execute(sql,(pid,))
        result = cr.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_board(self):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("SELECT * FROM scores")
        return cr.fetchall()

    def add_dummy(self,pid,pname,dums=0,cright=0,cwrong=0,c100=0,c1k=0,hang=0,twin=0,tloss=0,tgames=0):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("INSERT INTO scores (p_id,p_name,dum,c_right,c_wrong,c_100,c_1k,hangman,t_win,t_loss,t_games)VALUES(?,?,?,?,?,?,?,?,?,?,?)",(pid,pname,dums,cright,cwrong,c100,c1k,hang,twin,tloss,tgames))
        con.commit()

    def get_row(self,pid):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("SELECT * FROM scores WHERE p_id=?",(pid,))
        return cr.fetchone()

    def check_func(self,pid):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        sql = f"SELECT p_id FROM scores WHERE p_id = ?"
        cr.execute(sql, (pid,))
        res = cr.fetchall()
        if res:
            print("data found")
        else:
            print("no data found")

    def highscore(self,game,col=None,order="DESC"):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        sql = f"SELECT CAST(p_id AS INTEGER),{game} FROM scores ORDER BY {game} {order}"
        if game == 'count':
            if col:
                column = col
            else:
                column = "c_right"
            sql = f"SELECT CAST(p_id AS INTEGER),c_right,c_wrong,c_100,c_1k FROM scores ORDER BY {column} {order}"
        elif game == 'ut':
            if col:
                column = col
            else:
                column = "t_win"          
            sql = f"SELECT CAST(p_id AS INTEGER),t_win,t_loss,t_games,ROUND(t_win*100.0/t_games,2) FROM scores ORDER BY {column} {order}"
        cr.execute(sql)
        result = cr.fetchall()
        return result
    
    def my_score(self,user,arg="hang"):
        if arg == "hang":
            con = sqlite3.connect("funbot.db")
            cur = con.cursor()
            sql= "SELECT dum,hangman FROM scores WHERE CAST(p_id as INTEGER)=?"
            cur.execute(sql,(user,))
            result = cur.fetchone()
            con.close()
            return result
        elif arg == "all" :
            con = sqlite3.connect("funbot.db")
            cur = con.cursor()
            sql= "SELECT dum,c_right,c_wrong,c_100,c_1k,hangman,t_win,t_loss,t_games,ROUND(t_win*100.0/t_games,2) FROM scores WHERE CAST(p_id as INTEGER)=?"
            cur.execute(sql,(user,))
            result = cur.fetchone()
            con.close()
            return result
        elif arg == "ut":
            con = sqlite3.connect("funbot.db")
            cur = con.cursor()
            sql= "SELECT t_win,t_loss,t_games,ROUND(t_win*100.0/t_games,2) FROM scores WHERE CAST(p_id as INTEGER)=?"
            cur.execute(sql,(user,))
            result = cur.fetchone()
            con.close()
            return result
        elif arg == "count":
            con = sqlite3.connect("funbot.db")
            cur = con.cursor()
            sql= "SELECT c_right,c_wrong,c_100,c_1k FROM scores WHERE CAST(p_id as INTEGER)=?"
            cur.execute(sql,(user,))
            result = cur.fetchone()
            con.close()
            return result