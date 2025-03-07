
from cflib.drivers.crazyradio import Crazyradio
import time
import sys


def command_tag_3(channel,drone_address=0xff):   
    id = 3
    done = False

    while (not done):
        try:
            cr = Crazyradio(devid=id) #devid = radio dongle id (0 being the first dongle)

            cr.set_channel(channel)
            cr.set_data_rate(cr.DR_2MPS)

            for i in range(3):
                # Send multicast packet to P2P port 7
                cr.set_address((0xff,0xe7,0xe7,0xe7,0xe7)) # sets destination address for outgoing packets
                cr.set_ack_enable(False) # disable acknowledgement for outgoing packets
                cr.send_packet( (0xff, 0x80, 0x72, 0x01, drone_address) ) # sends packet to destination address via radio link 
                print('Tag C ' + str(drone_address))
            

                time.sleep(0.01)
            cr.close()
            done = True
            return 0
         
        except:
            print(f"command_tag_3: Error with dongle {id}")
            id = (id + 1) % 7
            print(f"command_tag_3: Trying dongle {id}")

if __name__ == '__main__':
    try:
            #print(hex(int(sys.argv[2])))
            command_tag_3(channel=int(sys.argv[1]), drone_address=(int(sys.argv[2],16)))
            #land_command(channel=int(sys.argv[1]), drone_address=(int(sys.argv[2])))
    except IndexError:
        print("Please specify channel and drone ID")
         
'''
0xff = broadcast address
0xe7 = multicast address (vendor specific address)
0x80 = 
0x63 = command to control whether crazyflies should keep flying
0x00 = 
'''

'''
safmc 2025 use 7 dongles (0 to 6)
take off: dongle 0
land: dongle 0
command_tag_1: dongle 1
command_tag_2: dongle 2
command_tag_3: dongle 3
reverse: dongle 4
'''