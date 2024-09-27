import json
from channels.generic.websocket import AsyncWebsocketConsumer
import cv2
import asyncio
import base64
from .TigerDetector import TigerDetector


class WebcamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.tiger_detector = TigerDetector()
        url='http://192.168.100.102:8080/video'
        self.camera = cv2.VideoCapture(0)
        asyncio.create_task(self.process_frames())

    async def disconnect(self, close_code):
        self.camera.release()

    async def process_frames(self):
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break

            processed_frame = self.tiger_detector.process_frame(frame)

            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')

            await self.send(json.dumps({
                'frame': frame_base64,
            }))

            await asyncio.sleep(0.033)  # ~30 fps