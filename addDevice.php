<?php
   class MyDB extends SQLite3 {
      function __construct() {
         $this->open('mac');
      }
   }
   
   $db = new MyDB();
   $sql =<<<EOF
      CREATE TABLE IF NOT EXISTS devices
      (ip           CHAR(50)    NOT NULL,
       port         CHAR(50)    NOT NULL,
       community    CHAR(50)    NOT NULL,
       version      CHAR(10)    NOT NULL);
EOF;
   $ret = $db->exec($sql);
   $sql =<<<EOF
      CREATE TABLE IF NOT EXISTS track
      (device_ip    CHAR(50)    NOT NULL,
       vlan         CHAR(50)    NOT NULL,
       port         CHAR(50)    NOT NULL,
       mac_address  CHAR(50)    NOT NULL);
EOF;
   $ret = $db->exec($sql);
   $ip = $_GET['ip'];
   $port = $_GET['port'];
   $community = $_GET['community'];
   $version = $_GET['version'];
   $sql ="insert into devices(ip, port, community, version) values('$ip','$port','$community','$version')";
   $ret = $db->exec($sql);
   if(!$ret) {
      echo "FALSE";
   } else {
      echo "OK";
   }
   $db->close();
?>
