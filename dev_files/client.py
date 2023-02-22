# Importing the relevant libraries
import websockets
import asyncio
import dev_files.results_display as results_display
import json
from gpiozero import Button

# Set up the GPIO button
button = Button(23)


# The main function that will handle connection and communication
# with the server
async def listen():
    url = "ws://atom-radpi-01.local:7890"
    # Connect to the server
    async with websockets.connect(url) as ws:

        # # Stay alive forever, waiting for button trigger to send a new request to server
        while True:
            button.wait_for_press()
            # Send request for data
            await ws.send('{"request": "distance"}')
            # while True:
            msg = await ws.recv()
            print(msg)
            data = json.loads(msg)
            data["label"] = "Distance"
            results_display.draw_display(json.dumps(data))

# Start the connection
asyncio.get_event_loop().run_until_complete(listen())
