import cv2
import base64
import numpy as np
from PIL import Image
from src.templates.threadwithstop import ThreadWithStop
from src.utils.messages.allMessages import mainCamera, serialCamera, SteerMotor, SpeedMotor, Klem
from src.utils.messages.messageHandlerSubscriber import messageHandlerSubscriber
from src.utils.messages.messageHandlerSender import messageHandlerSender

class threadLaneKeeping(ThreadWithStop):
    """
    Thread that runs your lane detection logic on each incoming frame
    and sends out speed/steer commands.
    """
    def __init__(self, queueList, logger, debugger=False):
        super(threadLaneKeeping, self).__init__()
        self.queuesList = queueList
        self.logger = logger
        self.debugger = debugger

        
        self.cameraSubscriber = messageHandlerSubscriber(self.queuesList, mainCamera, "lastOnly", False)
        self.kl = messageHandlerSender(self.queuesList, Klem)
        kl.send(30)
        # self.cameraSubscriber = messageHandlerSubscriber(self.queuesList, serialCamera, mode="all", block=False)

        self.steerSender = messageHandlerSender(self.queuesList, SteerMotor)
        self.speedSender = messageHandlerSender(self.queuesList, SpeedMotor)

    def run(self):
        """
        Loop forever, reading camera frames and computing new steer/speed.
        """
        while self._running:

            frame_b64 = self.cameraSubscriber.receive()
            if frame_b64 is None:
                continue  

            frame_data = base64.b64decode(frame_b64)
            
            
            im = Image.fromarray(arr)
            im.save("your_file.jpeg")
            np_arr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is None:
                continue

            steer_value, speed_value = self.do_lane_detection(frame)

            self.steerSender.send(int(steer_value))
            self.speedSender.send(int(speed_value))

    def do_lane_detection(self, frame):
        """
        To be implemented
        Return (steer, speed).
        """
        logger.info("attempting lane detection")
        return 0, 30
