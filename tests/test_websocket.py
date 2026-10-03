import asyncio
import json
import websockets


async def test_websocket():

    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:

        print("Connected to CyberShield WebSocket")

        print("Waiting for alert...")

        while True:

            message = await websocket.recv()

            data = json.loads(message)

            print("\n🚨 REAL-TIME ALERT RECEIVED")

            print(json.dumps(
                data,
                indent=4
            ))


asyncio.run(test_websocket())