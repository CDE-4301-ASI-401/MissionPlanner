from cflib.drivers.crazyradio import Crazyradio
import time
import sys

def reverse_command(channel, drone_address=0xff):   

    # for devid in range(3):
    #     try:
    #         cr = Crazyradio(devid=devid)
    #         return cr
    #     except Exception as e:
    #         print(f"Error with dongle {devid}: {e}")
    #         continue
    id = 0
    done = False

    while (not done):
        try:
            cr = Crazyradio(devid=id)
                
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
            done = True
        except:
            print(f"Error with dongle {id}")
            id = id + 1 % 7
            print(f"Trying dongle {id}")



if __name__ == '__main__':
    try:
        reverse_command(channel=int(sys.argv[1]), drone_address=(int(sys.argv[2],16)))
    except IndexError:
        print("No channel specified!")
