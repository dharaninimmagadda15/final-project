import shlex, subprocess
import sqlite3
from db_structure import DB_table, DB_NAME
from time import sleep
device_ip = "192.168.184.21"
community = "public"
OID_VLAN_PORT_INDEXS = ".1.3.6.1.2.1.17.7.1.2"
def get_required_info(community, device_ip, oid):
    command = "snmpwalk -v 2c -c %s %s %s"%(community, device_ip, oid)
    res = subprocess.Popen(shlex.split(command+" %s"%oid), stdout=subprocess.PIPE)
    out, err = res.communicate()
    req_info = []
    for i in out.splitlines():
        i_str = str(i)
        if "INTEGER" in i_str:
           
            vlan_mac,_,_,port = i_str.strip("'").split()
            vlan_mac_list = vlan_mac.split('.')
            mac_address = " ".join(vlan_mac_list[-6:])
            vlan = vlan_mac_list[-7]
            row = {"device_ip": device_ip, "vlan": vlan, "port": port,"mac_address": mac_address}
            req_info.append(row)
    return req_info

def insert_db(row):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("insert into "+DB_table+" values('%(device_ip)s','%(vlan)s','%(port)s','%(mac_address)s')" % ( row))
    con.commit()
    con.close()

def browse_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("select * from %s" % DB_table)
    data = cur.fetchall()
    con.close()
    return data


while True:
    print ("*"*100)
    print ("probing switch for mac address")
    print ("*"*100)
    data = get_required_info(community, device_ip,  OID_VLAN_PORT_INDEXS)
    print (data)
    print ("*"*100)
    print ("mac addresses got from switch")
    print ("*"*100)
    print (data)
    print ("*"*100)
    print ("inserting mac addresses in to DB")
    print ("*"*100)
    for row in data:
        insert_db(row)
    print ("*"*100)
    print ("insertion completed")
    print ("*"*100)
    print ("*"*100)
    print ("Browsing mac address from DB")
    print ("*"*100)
    print(browse_db())
    print ("*"*100)
    print ("WAITING FOR 5 SECONDS")
    print ("*"*100)
    sleep(5)
   
