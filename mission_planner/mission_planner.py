import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage
from std_msgs.msg import String
from .land import land_command
import time

class MissionPlanner(Node):

    def create_callback(self, drone,drones, channel):
        # channel = 100
        def listener_callback(msg):
            if msg.transforms:
                detectedTag = msg.transforms[0].child_frame_id
                if drones[drone] == False:
                    #self.get_logger().info( f'IGNORING {drone}')
                    return
                self.get_logger().info( f'{drone} saw: "%s"' % detectedTag)
                if detectedTag in self.dangerZones:
                    self.get_logger().info(f' {detectedTag} is a danger zone')
                elif detectedTag not in self.dangerZones:
                    if detectedTag in self.undetectedTags: # Single rescue
                        self.get_logger().info('Target "%s" has been detected' % detectedTag)    
                        self.get_logger().info(f'Landing {drone} on "%s"' % detectedTag)
                        self.undetectedTags.remove(detectedTag)
                        drones[drone] = False
                        land_command(channel, int(drone[2:], 16))
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
        # self.undetectedTags = {"tag36h11:0","tag36h11:1","tag36h11:2","tag36h11:3","tag36h11:4","tag36h11:5"}
        #undetected tags does not contain danger zones 
        # self.undetectedTags ={"tag36h11:30","tag36h11:31","tag36h11:40","tag36h11:41","tag36h11:42","tag36h11:43"}
        # self.undetectedTags = {"tag36h11:30","tag36h11:31"}
        self.undetectedTags = {"tag36h11:30"}
        # self.undetectedTags = {"tag36h11:24","tag36h11:25"}
        # self.dangerZones={"tag36h11:35","tag36h11:34","tag36h11:22","tag36h11:23" }
        self.dangerZones={}
        # self.dangerZones={"tag36h11:42","tag36h11:43"}
        # self.doublerescue = {"tag36h11:6":2,"tag36h11:7":2,"tag36h11:8":2,"tag36h11:9":2,"tag36h11:10":2}
    
        #drone_ids = ["cf01","cf02","cf03","cf04","cf05","cf06","cf12","cf13"]
        # drone_ids = ["cf01","cf02","cf03","cf04","cf05","cf06","cf07","cf08","cf09","cf10","cf11","cf12","cf13","cf14","cf15"]
        # drone_ids = ["cz07","cf10","cf11"]
        drone_ids = ["cz07"]
        #drone_ids = ["cf06","cf07","cf08","cf09","cf10","cf11"]
        #drone_ids = ["cf01","cf02","cf03","cf04","cf05","cf09"]
        drones = {drone_id: True for drone_id in drone_ids}
        # drone_channel = {"cf01":80,"cf02":80,"cf03":80,"cf04":80,"cf05":80,
        # "cf06":120,"cf07":120,"cf08":120,"cf09":100,"cf10":100,
        # "cf11":120,"cf12":120,"cf13":120,"cf14":120,"cf15":120}
        drone_channel = {"cz07":80}
        # drone_channel = {"cz07":80,"cf10":80,"cf11":60}
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