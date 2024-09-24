import rclpy
from rclpy.node import Node
from tf2_msgs.msg import TFMessage
from std_msgs.msg import String
from .land import land_command
import time

class MissionPlanner(Node):


    def create_callback(self, drone : str, drones : list[str], channel : int):
        # channel = 100
        def listener_callback(msg):
            if msg.transforms:
                detected_tag = msg.transforms[0].child_frame_id
                if drones[drone] == False:
                    #self.get_logger().info( f'IGNORING {drone}')
                    return
                self.get_logger().info( f'{drone} saw: "%s"' % detected_tag)
                if detected_tag in self.undetected_tags: # Single rescue
                    self.get_logger().info('Target "%s" has been detected' % detected_tag)    
                    self.get_logger().info(f'Landing {drone} on "%s"' % detected_tag)
                    self.undetected_tags.remove(detected_tag)
                    drones[drone] = False
                    land_command(channel, int(drone[2:], 16))
                elif detected_tag in self.doublerescue and self.doublerescue[detected_tag] > 0: #double rescue
                    self.doublerescue[detected_tag] -= 1
                    self.get_logger().info('Target "%s" has been detected' % detected_tag)    
                    self.get_logger().info(f'Landing {drone} on "%s"' % detected_tag)
                    drones[drone] = False
                    if self.doublerescue[detected_tag] == 0:
                        self.doublerescue.remove(detected_tag)
                    land_command(channel,int(drone[2:], 16))
                self.get_logger().info(f'TARGETS REMAINING {len(self.undetected_tags) + len(self.doublerescue)}')
            return
        return listener_callback
    

    def __init__(self):
        
        super().__init__('mission_planner')

        #self.declare_parameter("undetectedTags", {"tag36h11:200","tag36h11:204"}) 
        self.undetected_tags : set[str] = {"tag36h11:0","tag36h11:1","tag36h11:2","tag36h11:3","tag36h11:4","tag36h11:5"}
        
        self.doublerescue : dict[str, int] = {"tag36h11:6":2,"tag36h11:7":2,"tag36h11:8":2,"tag36h11:9":2,"tag36h11:10":2}
        
        #drone_ids = ["cf01","cf02","cf03","cf04","cf05","cf06","cf12","cf13"]
        drone_ids : list[str] = ["cf01","cf02","cf03","cf04","cf05","cf06","cf07","cf08","cf09","cf10","cf11","cf12","cf13","cf14","cf15"]
        #drone_ids = ["cf06","cf07","cf08","cf09","cf10","cf11"]
        #drone_ids = ["cf01","cf02","cf03","cf04","cf05","cf09"]
        drones : dict[str, bool] = {drone_id: True for drone_id in drone_ids}
        drone_channel : dict[str, int] = {"cf01":80,"cf02":80,"cf03":80,"cf04":80,"cf05":80,
        "cf06":120,"cf07":120,"cf08":120,"cf09":100,"cf10":100,
        "cf11":120,"cf12":120,"cf13":120,"cf14":120,"cf15":120}
        self.callbacks = {}
   
            
        # Create a dictionary of callback functions wrt drones
        for drone in drones:
            # Extract the number from the drone's name and use it to construct the function name
            callback_name : str = 'listener_callback' + drone[2:]
            current_callback : function = self.create_callback(drone, drones, drone_channel[drone])
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
