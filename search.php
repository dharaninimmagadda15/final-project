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

   $mac = $_GET['mac'];
   $sql ="SELECT * from track where mac_address LIKE '$mac'";

   $ret = $db->query($sql);
   while($row = $ret->fetchArray(SQLITE3_ASSOC) ) {
    $string=implode("|",$row);
    echo $string; 
    echo "<br>";
   }
   $db->close();
?>
