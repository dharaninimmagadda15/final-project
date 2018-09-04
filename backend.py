import shlex, subprocess
import sqlite3
from db_structure import DB_table, DB_NAME
from time import sleep
hostIP = "192.168.184.21"
hostCommunity = "public"
OID_VLAN_PORT_INDEXS = ".1.3.6.1.2.1.17.7.1.2"
command = "snmpwalk -v 2c -c %s %s"%(hostCommunity, hostIP)
def get_output(oid):
    res = subprocess.Popen(shlex.split(command+" %s"%oid), stdout=subprocess.PIPE)
    out, err = res.communicate()
    return out
def get_mac_addresses():
    port_indexes = get_output(OID_VLAN_PORT_INDEXS)
    mac_addresses = []
    for i in port_indexes.splitlines():
        i_str = str(i)
        if "INTEGER" in i_str:
            oid_macaddress = i_str.split()[0]
            mac_address_list = oid_macaddress.rsplit('.',6)[1:]
            mac_addresses.append(" ".join(mac_address_list))
    return mac_addresses

def insert_db(mac_address):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute("insert into %s values('%s')" % (DB_table, mac_address))
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
    mac_addresses = get_mac_addresses()
    print ("*"*100)
    print ("mac addresses got from switch")
    print ("*"*100)
    print (mac_addresses)
    print ("*"*100)
    print ("inserting mac addresses in to DB")
    print ("*"*100)
    for mac_address in mac_addresses:
        insert_db(mac_address)
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
    
    
   
        
    
