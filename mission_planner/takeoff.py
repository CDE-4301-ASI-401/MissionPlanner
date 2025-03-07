from cflib.drivers.crazyradio import Crazyradio
import time
import sys

def takeoff(channel):
    cr = Crazyradio(devid=0)
    cr.set_channel(channel)
    cr.set_data_rate(cr.DR_2MPS)

    for i in range(3):
        # Send multicast packet to P2P port 7
        cr.set_address((0xff,0xe7,0xe7,0xe7,0xe7))
        cr.set_ack_enable(False)
        cr.send_packet( (0xff, 0x80, 0x63, 0x01, 0xff) )
        print('send takeoff command')

        time.sleep(0.01)

if __name__ == '__main__':
    try:
        takeoff(channel=int(sys.argv[1]))
    except IndexError:
        print("No channel specified!")

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