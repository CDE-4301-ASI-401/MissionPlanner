from cflib.drivers.crazyradio import Crazyradio
import time
import sys

def reverse_command(channel, drone_address=0xff):   

    id = 4
    done = False

    while (not done):
        try:
            cr = Crazyradio(devid=id)
                
            cr.set_channel(channel)
            cr.set_data_rate(cr.DR_2MPS)

            # # Send multicast packet to P2P port 7
            # cr.set_address((0xff, 0xe7, 0xe7, 0xe7, 0xe7))
            # cr.set_ack_enable(False)

            for i in range(3):
                # Send multicast packet to P2P port 7
                cr.set_address((0xff, 0xe7, 0xe7, 0xe7, 0xe7))
                cr.set_ack_enable(False)
                cr.send_packet((0xff, 0x80, 0x70, 0x01, drone_address))  # Send the packet
                print('send reverse to ' + str(drone_address))

                time.sleep(0.01)
            cr.close()
            done = True
        except:
            print(f"reverse: Error with dongle {id}")
            id = (id + 1) % 7
            print(f"reverse:Trying dongle {id}")



if __name__ == '__main__':
    try:
        reverse_command(channel=int(sys.argv[1]), drone_address=(int(sys.argv[2],16)))
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