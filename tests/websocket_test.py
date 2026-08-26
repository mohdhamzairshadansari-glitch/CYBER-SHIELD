import asyncio
import websockets


async def main():

    uri = "ws://127.0.0.1:8000/ws"

    async with websockets.connect(uri) as websocket:

        print("Connected to CyberShield WebSocket")
        print("Waiting for security alerts...\n")

        while True:

            message = await websocket.recv()

            print("🚨 LIVE ALERT:")
            print(message)
            print()


if __name__ == "__main__":

    asyncio.run(main())