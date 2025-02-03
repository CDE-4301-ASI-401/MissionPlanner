import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage
from std_msgs.msg import String
from .land import land_command
from .reverse import reverse_command    
import time
from threading import Event
from cflib.positioning.motion_commander import MotionCommander

class MissionPlanner(Node):

    def create_callback(self, drone,drones, channel):
        # channel = 100
        def listener_callback(msg):

            if msg.transforms:
                detectedTag = msg.transforms[0].child_frame_id
                OneDangerZone = None
                OneVictimTag = None
                OneNavigationAid = None
                if drones[drone] == False:
                    #self.get_logger().info( f'IGNORING {drone}')
                    return
                self.get_logger().info( f'{drone} saw: "%s"' % detectedTag)
                
                if detectedTag in self.dangerZones:
                    self.get_logger().info(f' {detectedTag} is a danger zone')
                    OneDangerZone = detectedTag

                elif detectedTag not in self.dangerZones:
                    if detectedTag in self.undetectedTags: # Single rescue
                        OneVictimTag = detectedTag
                        self.get_logger().info('Target "%s" has been detected' % detectedTag)    
                        
                        if OneDangerZone == None and OneVictimTag != None:
                            self.get_logger().info(f'Landing {drone} on "%s"' % OneVictimTag)
                                
                            self.undetectedTags.remove(OneVictimTag)
                            drones[drone] = False
                            land_command(channel, int(drone[2:], 16))
                            OneDangerZone = None

                        elif OneDangerZone != None and OneVictimTag != None:
                            self.get_logger().info(f'Land {drone} on victim "{OneVictimTag}" away from "{OneDangerZone}" with delay')
                            self.undetectedTags.remove(OneVictimTag)
                            
                            drones[drone] = False
                            time.sleep(5) #delay
                            land_command(channel, int(drone[2:], 16))
                            OneDangerZone = None
                            OneVictimTag = None

                if detectedTag in self.reverseNavigationAids:
                    OneNavigationAid = detectedTag
                    self.get_logger().info(f'{drone} saw navigation aid {OneNavigationAid}')
                    if drone not in ["cf06", "cf07", "cf08", "cf09"]:
                        reverse_command(channel, int(drone[2:], 16))
                        OneNavigationAid = None
                 
                    
                
#alll drones except for red drones


 
                # if not self.undetectedTags:
                #     self.get_logger().info('All targets have been detected')
                #     for drone in drones:
                #         drones[drone] = False
                #     land_command(channel, int(drone[2:], 16))   
                #     return
                # self.get.logger().info(f'TARGETS REMAINING {len(self.undetectedTags)}')
            return
    
        return listener_callback
    

    def __init__(self):
        
        super().__init__('mission_planner')

        #self.declare_parameter("undetectedTags", {"tag36h11:200","tag36h11:204"}) 
        
        #undetected tags does not contain danger zones and navigation aids
        # self.undetectedTags = {"tag36h11:21","tag36h11:22","tag36h11:23",
        #                        "tag36h11:24","tag36h11:25","tag36h11:26",
        #                        "tag36h11:27"}
        self.undetectedTags={"tag36h11:30"}

        self.dangerZones={"tag36h11:32"}

        self.reverseNavigationAids={"tag36h11:30","tag36h11:31","tag36h11:36","tag36h11:37"}

#reverse navigation aid is aid 30 31 36 37

        # self.dangerZones={"tag36h11:10","tag36h11:11","tag36h11:12",
        #                   "tag36h11:13","tag36h11:14","tag36h11:15",
        #                   "tag36h11:16","tag36h11:17"}
        # self.dangerZones={}
    
        # drone_ids = ["cf01","cf02","cf03","cf04","cf05",
        # "cf06","cf07","cf08","cf09","cf10",
        # "cf11","cf12","cf13","cf14","cf15",
        # "cf16","cf17","cf18","cf19","cf34"]
        drone_ids = ["cf18"]
        drones = {drone_id: True for drone_id in drone_ids}
        # drone_channel = {"cf01":60,"cf02":60,"cf03":60,"cf04":60,"cf05":80,
        # "cf06":60,"cf07":80,"cf08":60,"cf09":80,"cf10":60,
        # "cf11":60,"cf12":60,"cf13":60,"cf14":60,"cf15":80,
        # "cf16":80,"cf17":80,"cf18":80,"cf19":80,"cf34":60}
        drone_channel = {"cf18":80}

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
