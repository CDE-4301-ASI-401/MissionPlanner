from cflib.drivers.crazyradio import Crazyradio
import time
import sys

def reverse_command(channel, drone_address=0xff):   

    cr = Crazyradio(devid=1)
    cr.set_channel(channel)
    cr.set_data_rate(cr.DR_2MPS)

    # Send multicast packet to P2P port 7
    cr.set_address((0xff, 0xe7, 0xe7, 0xe7, 0xe7))
    cr.set_ack_enable(False)

    for i in range(3):
        # Send multicast packet to P2P port 7
        cr.set_address((0xff, 0xe7, 0xe7, 0xe7, 0xe7))
        cr.set_ack_enable(False)
        cr.send_packet((0xff, 0x80, 0x70, 0x01, 0xff))  # Send the packet
        print('send reverse to ' + str(drone_address))

        time.sleep(0.01)
    cr.close()



if __name__ == '__main__':
    try:
        reverse_command(channel=int(sys.argv[1]), drone_address=(int(sys.argv[2],16)))
    except IndexError:
        print("No channel specified!")
