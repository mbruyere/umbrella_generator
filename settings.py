# This settings.py need to reflect the exact config of you deplyed network 

# Uncomment the approriate section and fullfil the right information. 


# One switch 

# vlan_name = 'IXP_VLAN'
# dp_id_sw1 = 0x1
# sw1_type = 'Allied-Telesis'


# One switch plus legacy non SDN switch 
# +-------------------+            +----------+
# |                   |            |          |
# |  none SDN switch  --------------   SW1    |
# |                   |            |          |
# +-------------------+            +----------+
# Uncomment this section below when topo arguments is equal to one_legacy

# vlan_name = 'IXP_VLAN'
# dp_id_sw1 = 0x1
# sw1_type = 'Allied-Telesis'



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
# dp_id_sw1 = 0x1
# dp_id_sw2 = 0x2
# sw1_primary_port = '27'
# sw1_backup_port = '28'
# sw2_primary_port = '27'
# sw2_backup_port = '28'
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