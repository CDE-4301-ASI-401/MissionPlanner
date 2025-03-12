from cflib.drivers.crazyradio import Crazyradio
import time
import sys
from cflib.utils import power_switch
#to kill one specific drone. i.e. python3 kill.py 15 for cf15
if __name__ == '__main__':

    drone_channel = {"cf01":60,"cf02":60,"cf33":60,"cf04":60,
        "cf05":80,"cf06":60,"cf07":80,"cf08":60,"cf09":80,
        "cf11":60,"cf12":60,"cf13":60,"cf14":60,
        "cf15":80,"cf16":80,"cf17":80,"cf10":80,"cf19":80,
        "cf20":60,"cf35":80,"cf37":80}
    
    for i in drone_channel:
        id = i[2:]
        # print(f'id: {id}')
        # print(f'sys.argv[1]: {sys.argv[1]}')
        if id == sys.argv[1]:

            channel = drone_channel.get(i)

            cf = power_switch.PowerSwitch(f'radio://0/{channel}/2M/E7E7E7E7{id}')
            # print(f'radio://0/{channel}/2M/E7E7E7E7{id}')
            cf.platform_power_down()
            print(f"line 26 Successfully powered down Drone {id} on channel {channel}")

            