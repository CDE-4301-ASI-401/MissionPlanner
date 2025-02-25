import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage
from std_msgs.msg import String
from .land import land_command
from .reverse import reverse_command    
import time
from threading import Event
from cflib.positioning.motion_commander import MotionCommander
import numpy as np
import time

#drone id is in terms of hexadecimal
class MissionPlanner(Node):

    def create_callback(self, drone, drones, channel):
        # channel = 100
        
        def listener_callback(msg):
 
            if msg.transforms:
                # self.get_logger().info(f'msg.transforms: {msg.transforms}')
                detectedTag = msg.transforms[0].child_frame_id
                x = msg.transforms[0].transform.translation.x
                # y = msg.transforms[0].transform.translation.y
                z = msg.transforms[0].transform.translation.z

                self.get_logger().info(f'x: {x}, z: {z}')
                distance = np.sqrt(x**2 + z**2)
                self.get_logger().info(f'distance: {distance}')
                current_time = time.time()
                delta = current_time - self.reverse_command_timestamp
                # self.get_logger().info(f'delta: {delta}')
                
                if not self.undetectedTags:
                    self.get_logger().info('All targets have been detected')
                    for drone in drones:
                        land_command(channel, int(drone[2:], 16))
                        self.get_logger().info('Final land command issued')
                    return
                for drone in drones:
                    if drones[drone] == False:
                #         #self.get_logger().info( f'IGNORING {drone}')
                        return
                
                self.get_logger().info( f'{drone} detectedTag: "%s"' % detectedTag)
 
                if detectedTag in self.dangerZones:
                    OneDangerZone = detectedTag
                    self.get_logger().info(f'{OneDangerZone} is a danger zone')

                    if detectedTag in self.undetectedTags:
                        OneVictimTag = detectedTag
                        self.get_logger().info(f'starting delay')
                        time.sleep(10)
                        self.get_logger().info(f'line 33 Landing {drone} on "%s"' % OneVictimTag)
                        self.undetectedTags.remove(OneVictimTag)
                        drones[drone] = False
                        land_command(channel, int(drone[2:], 16))

                elif detectedTag not in self.dangerZones:

                    if detectedTag in self.reverseNavigationAids:
                        OneNavigationAid = detectedTag
                        # self.get_logger().info(f'new navAidDetection {self.navAidDetection}')
                        self.get_logger().info(f'line 41 {drone} saw navigation aid {OneNavigationAid}')
                        
                        # if drone not in ["cf01", "cf02", "cf03", "cf04", "cf05", "cf06", "cf07", "cf08", "cf09"]:
                        if drone not in ["cf33", "cf02", "cf35", "cf04", "cf05", "cf06", "cf07", "cf09"]:
                            if self.navAidDetection == True or delta > 5:
                                reverse_command(channel, int(drone[2:], 16))
                                # self.get_logger().info(f'line 45 reverse command sent {drone} channel {channel} [{int(drone[2:], 16)}]')
                                self.get_logger().info(f'line 45 reverse command sent {drone}')
                                self.reverse_command_timestamp = current_time
                                self.navAidDetection = False
                            else:
                                self.get_logger().info(f'line 48 reverse command ignored {drone}')
                                self.navAidDetection = False

                    if detectedTag in self.undetectedTags:
                        OneVictimTag = detectedTag
                        # if distance < 3: #for a height of 0.5m
                        self.get_logger().info(f'starting delay')
                        time.sleep(10)
                        self.get_logger().info(f'line 53 Landing {drone} on "%s"' % OneVictimTag)
                        self.undetectedTags.remove(OneVictimTag)
                        drones[drone] = False
                        land_command(channel, int(drone[2:], 16))

                self.get_logger().info(f'TARGETS REMAINING {len(self.undetectedTags)}')

            return
    
        return listener_callback
    

    def __init__(self):
        
        super().__init__('mission_planner')

        self.reverse_command_timestamp = time.time()

        self.navAidDetection = True
        # self.get_logger().info(f'current navAidDetection {self.navAidDetection}')
        #self.declare_parameter("undetectedTags", {"tag36h11:200","tag36h11:204"}) 
        
        #undetected tags does not contain danger zones and navigation aids
        self.undetectedTags = {"tag36h11:26","tag36h11:27","tag36h11:24"}
        
        # self.undetectedTags = {}
        # self.undetectedTags={"tag36h11:30"}

        # self.dangerZones={"tag36h11:32"}

        self.reverseNavigationAids={"tag36h11:52","tag36h11:48","tag36h11:47","tag36h11:36"}

#reverse navigation aid is aid 30 31 36 37

        self.dangerZones={"tag36h11:10","tag36h11:11","tag36h11:12",
                          "tag36h11:13","tag36h11:14","tag36h11:15",
                          "tag36h11:16","tag36h11:17"}
        # self.dangerZones={}
    
        # drone_ids = ["cf01","cf02","cf03","cf04",
        # "cf05","cf06","cf07","cf08","cf09","cf10",
        # "cf11","cf12","cf13","cf14","cf15","cf16",
        # "cf37","cf18","cf19","cf20","cf35","cf37"]


        # drone_ids = ["cf10","cf11","cf12","cf13","cf14"]
        # drone_ids = ["cf37","cf20"]
        drone_ids = ["cf01"]

        # drone_ids = ["cf20"]
        drones = {drone_id: True for drone_id in drone_ids}
        # drone_channel = {"cf01":60,"cf02":60,"cf03":60,"cf04":60,
        #     "cf05":80,"cf06":60,"cf07":80,"cf08":60,"cf09":80,
        #     "cf10":60,"cf11":60,"cf12":60,"cf13":60,"cf14":60,
        #     "cf15":80,"cf16":80,"cf17":80,"cf18":80,"cf19":80,
        #     "cf20":60,"cf35":80,"cf37":80}
        # drone_channel = {"cf37":80,"cf20":80}
        drone_channel = {"cf01":70}
        self.callbacks = {}
   
        # Create a dictionary of callback functions wrt drones
        for drone in drones:
            # Extract the number from the drone's name and use it to construct the function name
            callback_name = 'listener_callback' + drone[2:]
            current_callback = self.create_callback(drone,drones,drone_channel[drone])
            current_callback.__name__ = callback_name   # give the callback function a specific name.
            setattr(self, callback_name, current_callback)
            self.callbacks[drone] = current_callback


        # Create a subscription for each drone
        for drone in drones:
            print(f'mission_planner:{TFMessage}')
            current_subscription = self.create_subscription(
                TFMessage,
                drone + '/tf',
                self.callbacks[drone],
                10)
            current_subscription
 


def main(args=None):
    rclpy.init(args=args)

    mission_planner = MissionPlanner()

    rclpy.spin(mission_planner)

if __name__ == '__main__':
    main()
