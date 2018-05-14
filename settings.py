# This settings.py need to reflect the exact config of you deplyed network 
# Global settings :

# If you want to run with or without IPv6 support [False or True]
IPv6_active = False

# Uncomment the approriate section and fullfil the right information. 


# One switch 

vlan_name = 'IXP_VLAN'
dp_id_sw1 = 0x1
sw1_type = 'Lagopus'


# One switch plus legacy non SDN switch 
# +-------------------+            +----------+
# |                   |            |          |
# |  none SDN switch  --------------   SW1    |
# |                   |            |          |
# +-------------------+            +----------+
# Uncomment this section below when topo arguments is equal to one_legacy

# vlan_name = 'PIXIE'
# vlan_number = 3
# dp_id_sw1 = 0x1aeba5a6f8
# sw1_port_to_legacy = 27
# sw1_type = 'Allied-Telesis'
# vlan_local = 3
# vlan_interco = 3000

# # two switch plus two legacy:
# +-----------------------+                  +--------------------------+
# |                       |                  |                          |
# |Primary non SDN switch -------------------- Secondary non SDN switch |
# |                       |                  |                          |
# +-----|-------\---------+                  +----/--------|------------+
#       |        ----\                       /----         |             
#       |             ----\             /----              |             
#       |                  ----\   /----                   |             
#       |                    /-----\                       |             
#       |               /----       ----\                  |             
#       |          /----                 ----\             |             
#       |     /----                           ----\        |             
# +-----|-----+                                    --------|-----+       
# |           |                                     |            |       
# |   SW!     |                                     |    SW2     |       
# |           |                                     |            |       
# +-----------+                                     +------------+       
# Uncomment this section below when topo  arguments is equal to two_legacy

# vlan_name = 'PIXIE'
# vlan_number = 2 
# dp_id_sw1 = 0x1
# dp_id_sw2 = 0x2
# sw1_primary_port = '3'
# sw1_backup_port = '4'
# sw2_primary_port = '3'
# sw2_backup_port = '4'
# sw1_type = 'Open vSwitch'
# sw2_type = 'Open vSwitch'


# # Triangle :
# +---------+                       +---------+
# |         |                       |         |
# |  SW1    -------------------------   SW2   |
# |         |                       |         |
# +--\------+                       +---------+
#     -\                               -/      
#       -\                           -/        
#         -\                       -/          
#           -\                   -/            
#             -\               -/              
#               -\+--------+ -/                
#                 -        -/                  
#                 |  SW3   |                   
#                 |        |                   
#                 +--------+                   
# Uncomment this section below when topo  arguments is equal to triangle


# vlan_name = 'IXP_VLAN'
# dp_id_Edge1 = 0x1
# dp_id_Edge2 = 0x2
# dp_id_Edge3 = 0x3
# sw1_type = 'Open vSwitch'
# sw2_type = 'Open vSwitch'
# sw3_type = 'Open vSwitch'
# sw1_portnum_to_sw2 = '47'
# sw1_portnum_to_sw3 = '48'
# sw2_portnum_to_sw1 = '1'
# sw2_portnum_to_sw3 = '2'
# sw3_portnum_to_sw1 = '2'
# sw3_portnum_to_sw2 = '1'