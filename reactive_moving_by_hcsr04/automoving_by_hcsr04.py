import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
from std_msgs.msg import Int32MultiArray, String
import serial
import time

bottom = 50
R = 12
L = 13
ENABLE_r = 17
ENABLE_l = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(R, GPIO.OUT)
GPIO.setup(L, GPIO.OUT)
GPIO.setup(ENABLE_r, GPIO.OUT)
GPIO.setup(ENABLE_l, GPIO.OUT)
GPIO.output(ENABLE_r, GPIO.LOW)
GPIO.output(ENABLE_l, GPIO.LOW)

p_r = GPIO.PWM(R, bottom)
p_l = GPIO.PWM(L, bottom)

p_r.start(0)
p_l.start(0)

class PublisherNode(Node):
    def __init__(self):
        super().__init__("automoving_by_hcsr04")
        self.joy_r = 0
        self.joy_l = 0

        self.verocity = None
        self.pub = self.create_publisher(Int32MultiArray, "verocity", 10)
        timer_period = 1.0
        self.tmr = self.create_timer(timer_period, self.hcsrToGpio)

    def reading(self, sensor):
        TRIG = 22
        ECHO = 23
        
        if sensor == 0:
            GPIO.setup(TRIG,GPIO.OUT)
            GPIO.setup(ECHO,GPIO.IN)
            GPIO.output(TRIG, GPIO.LOW)
            time.sleep(0.3)

            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
              signaloff = time.time()

            while GPIO.input(ECHO) == 1:
              signalon = time.time()

            timepassed = signalon - signaloff
            distance = timepassed * 17000
            return distance
            GPIO.cleanup()
        else:
            print ("Incorrect usonic() function varible.")    

    def hcsrToGpio(self):
        msg = String()
        msg.data = 'distance: "{0}"'.format(self.reading(0))
        self.get_logger().info('Publishing: "{0}"'.format(msg.data))

        self.dist = self.reading(0)
        motor_r = 0
        motor_l = 0

        if 20 < self.dist < 30:
            GPIO.output(ENABLE_r, GPIO.LOW)
            GPIO.output(ENABLE_l, GPIO.LOW)
            p_r.ChangeDutyCycle(100)
            p_l.ChangeDutyCycle(100)
            print("go:")
            
        else :
            print("stop:")
            p_r.stop()
            p_l.stop()
            p_r.start(0)
            p_l.start(0)
       
def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    GPIO.cleanup()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
