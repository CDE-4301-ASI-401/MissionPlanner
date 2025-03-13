from cflib.drivers.crazyradio import Crazyradio
import time
import sys
from cflib.utils import power_switch
#python kill_all.py
if __name__ == '__main__':
    # try:
    #     channel = sys.argv[1]
    # except IndexError:
    #     print("Enter channel number")
 
    drone_channel = {"cf01":60,"cf02":60,"cf33":60,"cf04":60,
        "cf05":80,"cf06":60,"cf07":80,"cf08":60,"cf09":80,
        "cf11":60,"cf12":60,"cf13":60,"cf14":60,
        "cf15":80,"cf16":80,"cf17":80,"cf18":80,"cf19":80,
        "cf20":60,"cf35":80,"cf37":80}
        
    for i in range(3):
        for i in drone_channel:
            id = i[2:]
            channel = drone_channel.get(i)
            uri = f'radio://0/{channel}/2M/E7E7E7E7{id}'
            # print(f'url: {uri}')
            try:
                cf = power_switch.PowerSwitch(uri)
                cf.platform_power_down()
                print(f"Successfully powered down Drone {id} on channel {channel}")
            except Exception as e:
                print(f"ignored drone {id} on channel {channel}")
                
