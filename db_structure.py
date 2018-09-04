import sqlite3
con = sqlite3.connect("")
DB_NAME = "mac"
DB_table = "mac_info"

if __name__ == "__main__":
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("create table %s(device_ip varchar(250), vlan varchar(250), port varchar(250), mac_address varchar(250))" % DB_table)
    con.close()
