Umbrella.py is a v0.1 script to generate FAUCET YAML config file  

To know more about the Umbrella IXP architecture: [Umbrella ACM SOSR 18][https://conferences.sigcomm.org/sosr/2018/sosr18-finals/sosr18-poster-final14.pdf]

It runs with Python 3.6 

Dependencies :

```
pip3 install pathlib2==2.3.0 docopt==0.6.2 ruamel.yaml==0.15.35 ipaddress==1.0.19
```


## How to use it :
```
./umbrella.py
Usage:
  umbrella.py topo <topo_name> <csv_file_name> <faucet_config_file_name>
  umbrella.py --check_output_config | -c <faucet_config_to_check>
  umbrella.py -h | --help | --version
```
It is required to have a CSV file with this header column and filled with rigth information. 

You can find sample CSV files in the repository

```
idrtr,hostname,addr_ipv4,addr_ipv6,macaddr,.membre,pop,switch,port,status
0,h1,10.0.0.1,2001:7f8:68::1,00:00:00:00:00:01,h1,TLS00,sw1,1,Production
1,h2,10.0.0.2,2001:7f8:68::2,00:00:00:00:00:02,h2,TLS00,sw1,2,Production
2,h3,10.0.0.3,2001:7f8:68::3,00:00:00:00:00:03,h3,TLS00,sw1,3,Production
3,h4,10.0.0.4,2001:7f8:68::4,00:00:00:00:00:04,h4,TLS01,sw1,4,Production
```

## The settings.py need to edited to reflect the configuration of your network 

Uncomment the approriate section and fullfil the right information. 

If you want to run with or without IPv6 support
**IPv6_active = [ False - True ]**

### One single OpenFlow Switch 

Uncomment this section below when topo arguments is equal to **one_switch**

```
vlan_name = 'IXP_VLAN'
dp_id_sw1 = 0x1
sw1_type = 'Allied-Telesis'
```

### One OpenFlow switch connected to a legacy non SDN switch

```
+-------------------+            +----------+
|                   |            |          |
|  none SDN switch  --------------   SW1    |
|                   |            |          |
+-------------------+            +----------+
```

Uncomment this section below when topo arguments is equal to one_legacy

```
vlan_name = 'PIXIE'
vlan_number = 3
dp_id_sw1 = 0x1
sw1_port_to_legacy = 27
sw1_type = 'Open vSwitch'
```

### Two switch plus two legacies:

```
+-----------------------+                  +--------------------------+
|                       |                  |                          |
|Primary non SDN switch -------------------- Secondary non SDN switch |
|                       |                  |                          |
+-----|-------\---------+                  +----/--------|------------+
      |        ----\                       /----         |             
      |             ----\             /----              |             
      |                  ----\   /----                   |             
      |                    /-----\                       |             
      |               /----       ----\                  |             
      |          /----                 ----\             |             
      |     /----                           ----\        |             
+-----|-----+                                    --------|-----+       
|           |                                     |            |       
|   SW!     |                                     |    SW2     |       
|           |                                     |            |       
+-----------+                                     +------------+       
```

Uncomment this section below when topo  arguments is equal to **two_legacy**
```
vlan_name = 'PIXIE'
dp_id_sw1 = 0x1
dp_id_sw2 = 0x2
sw1_primary_port = '27'
sw1_backup_port = '28'
sw2_primary_port = '27'
sw2_backup_port = '28'
sw1_type = 'Open vSwitch'
sw2_type = 'Open vSwitch'
```

### Triangle :
```
+---------+                       +---------+
|         |                       |         |
|  SW1    -------------------------   SW2   |
|         |                       |         |
+--\------+                       +---------+
    -\                               -/      
      -\                           -/        
        -\                       -/          
          -\                   -/            
            -\               -/              
              -\+--------+ -/                
                -        -/                  
                |  SW3   |                   
                |        |                   
                +--------+                   
```

Uncomment this section below when topo  arguments is equal to **triangle**

```
vlan_name = 'IXP_VLAN'
dp_id_Edge1 = 0x1
dp_id_Edge2 = 0x2
dp_id_Edge3 = 0x3
sw1_type = 'Allied-Telesis'
sw2_type = 'Allied-Telesis'
sw3_type = 'Allied-Telesis'
sw1_portnum_to_sw2 = '25'
sw1_portnum_to_sw3 = '28'
sw2_portnum_to_sw1 = '25'
sw2_portnum_to_sw3 = '26'
sw3_portnum_to_sw1 = '28'
sw3_portnum_to_sw2 = '25'
```
