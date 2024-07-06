import json
import sqlite3


class IdClass:
    def __init__(self) -> None:
        pass


#------- CHECK GUILD ID ----------------------------------------------------
    def check_gid(self,g_id):
        with open('channel_ids.json','r') as f:
            id_read = json.load(f)
        if str(g_id) in id_read:
            return True
        else:
            return False

#----------- GET ID  ----------------------------------------------------
    def get_hangman(self, g_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        if str(g_id) in id_read:
            return id_read[str(g_id)]["hangman"]
    def get_counting(self, g_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        if str(g_id) in id_read:
            return id_read[str(g_id)]["counting"]
    def get_ttt(self, g_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        if str(g_id) in id_read:
            return id_read[str(g_id)]["ttt"]
    def get_disabled(self,g_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        if str(g_id) in id_read:
            return id_read[str(g_id)]["dis_command"]
    def get_lastnum(self,g_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        if str(g_id) in id_read:
            return id_read[str(g_id)]["last_count"]

    def get_lastcounter(self,g_id):
        with open('channel_ids.json','r') as f:
            id_read = json.load(f)
            if str(g_id) in id_read:
                return id_read[str(g_id)]["last_counter"]






#----- ADD GUILD ---------------------------------------------------------------

    def add_guild(self, g_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        id_read[str(g_id)]={"counting": None,
                            "hangman": None,
                            "ttt": None,
                            "dis_command": ["1"],
                            "last_count": 0,
                            "last_counter":None}
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)

#-------- UPDATE CHANNEL ID -------------------------------------------------------------

    def update_counting(self,g_id,c_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        id_read[str(g_id)]["counting"]=str(c_id)
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)
    def update_hangman(self,g_id,c_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        id_read[str(g_id)]["hangman"]=str(c_id)
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)
    def update_ttt(self,g_id,c_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        id_read[str(g_id)]["ttt"]=str(c_id)
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)

    def update_disabled(self,g_id,com):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        command_list = id_read[str(g_id)]["dis_command"]
        command_list.append(str(com))
        id_read[str(g_id)]["dis_command"]=command_list
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)
    def update_enabled(self,g_id,com):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        command_list = id_read[str(g_id)]["dis_command"]
        command_list.remove(str(com))
        id_read[str(g_id)]["dis_command"]=command_list
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)

    def update_lastnum(self,g_id,num):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        id_read[str(g_id)]["last_count"]=num
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)

    def update_lastnum0(self,g_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        id_read[str(g_id)]["last_count"]=0
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)

    def update_lastcounter(self,g_id,a_id):
        with open('channel_ids.json', 'r') as f:
            id_read = json.load(f)
        id_read[str(g_id)]["last_counter"]=a_id
        with open('channel_ids.json','w') as f:
            json.dump(id_read,f,indent=4)

class IdClass_new:
    def __init__(self):
        pass
    def make_guilds(self,gid,count,hang,ttt,last_n,last_c,dis):
        con=sqlite3.connect("funbot.db")
        cr=con.cursor()
        cr.execute("CREATE TABLE guilds (g_id,count_ch,hangman_ch,ttt_ch,last_number,last_counter,disabled_comm)")
        cr.commit()
        # cr.execute("")

    def add_guilds(self, gid,count=None,hang=None,ttt=None,last_n=0,last_c=None,dis=None):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        if dis == None:
            dis=json.dumps([])
        cr.execute("INSERT INTO guilds (g_id,count_ch,hangman_ch,ttt_ch,last_number,last_counter,disabled_comm) VALUES (?,?,?,?,?,?,?)", (gid,count,hang,ttt,last_n,last_c,dis))
        con.commit()

    def get_channel_id(self,gid):
        con=sqlite3.connect("funbot.db")
        cr=con.cursor()
        cr.execute("SELECT * FROM guilds WHERE g_id=?",(gid,))
        con.commit()
        return cr.fetchall()
    def del_guilds(self,gid):
        con=sqlite3.connect("funbot.db")
        cr=con.cursor()
        cr.execute("DELETE FROM guilds WHERE CAST(g_id AS INTEGER) = ?",(gid,))
        con.commit()
    def update_guilds(self,gid,col_name,new_value):
        con=sqlite3.connect("funbot.db")
        cr=con.cursor()
        sql=f"UPDATE guilds SET {col_name}=? WHERE g_id=?"
        cr.execute(sql,(new_value,gid))
        con.commit()
    def get_table(self):
        con=sqlite3.connect("funbot.db")
        cr=con.cursor()
        cr.execute("SELECT * FROM guilds")
        guild_detail=cr.fetchall()
        return guild_detail

    def chek_gid(self,gid):
        con = sqlite3.connect("funbot.db")
        cr = con.cursor()
        cr.execute("SELECT g_id FROM guilds WHERE last_number = 0")
        return cr.fetchall()


