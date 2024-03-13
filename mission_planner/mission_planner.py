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
                self.get_logger().info( f'{drone} saw: "%s"' % detectedTag)
                if drones[drone] == False:
                    self.get_logger().info( f'IGNORING {drone}')
                    return
                if detectedTag in self.undetectedTags: # Single rescue
                    self.get_logger().info('Target "%s" has been detected' % detectedTag)    
                    self.get_logger().info(f'Landing {drone} on "%s"' % detectedTag)
                    self.undetectedTags.remove(detectedTag)
                    drones[drone] = False
                    land_command(channel, int(drone[2:], 16))
                elif detectedTag in self.doublerescue and self.doublerescue[detectedTag]>0: #double rescue
                    self.doublerescue[detectedTag] -= 1
                    self.get_logger().info('Target "%s" has been detected' % detectedTag)    
                    self.get_logger().info(f'Landing {drone} on "%s"' % detectedTag)
                    drones[drone] = False
                    land_command(channel,int(drone[2:], 16))
            return
        return listener_callback
    

    def __init__(self):
        
        super().__init__('mission_planner')

        #self.declare_parameter("undetectedTags", {"tag36h11:200","tag36h11:204"}) 
        self.undetectedTags = {"tag36h11:200","tag36h11:204","tag36h11:205","tag36h11:208"}
        self.doublerescue = {"tag36h11:206":2}
        
        #drones_ids = ["cf01","cf02","cf03","cf04","cf05","cf09"]
        drone_ids = ["cf06","cf07","cf08","cf09","cf10","cf11"]
        #drone_ids = ["cf01","cf02","cf03","cf04","cf05","cf09"]
        drones = {drone_id: True for drone_id in drone_ids}
        drone_channel = {"cf01":80,"cf02":80,"cf03":80,"cf04":80,"cf05":80,"cf06":120,"cf07":120,"cf08":120,"cf09":100,"cf10":100,"cf11":120,"cf13":120,"cf12":120}
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
