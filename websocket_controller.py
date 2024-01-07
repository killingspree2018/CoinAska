import asyncio
import json
import websockets

from api.services.main_bot_service import MarketMakingBotService

async def connect_to_websocket_server():
    uri = "wss://ws.coinstore.com/s/ws"
    
    async with websockets.connect(uri) as websocket:
        # Send a message to the server
        sub_req = {
                        "op": "SUB",
                        "channel": [
                            # "askausdt@ticker",
                            "askausdt@depth",
                            # "739@trade"
                        ],
                        "id": 1
                    }
        sub_message = json.dumps(sub_req)
        await websocket.send(sub_message)
        # print(f"Sent message: {sub_message}")
        x = 5
        while x:
            # Receive a response from the server
            response = await websocket.recv()
            response_obj = json.loads(response)
            # if response_obj.get('T') == 'ticker':
            #     print(f"Received ticker Data: {response}")
            #     current_price = float(response_obj.get('close'))
            #     bot_service = MarketMakingBotService(current_price)
            #     bot_service.initiate_orders()
            #     x=1
            # if response_obj.get('T') == 'trade':
            #     print(f"Received trade Data: {response}")
            if response_obj.get('T') == 'depth':
                # print(f"Received depth Data: {response}")
                print(f"Length of sell orders depth Data: {len(response_obj.get('a'))}")
                print(f"Length of buy orders depth Data: {len(response_obj.get('b'))}")
            x -= 1
        # bot_service.price_movement(100)
        unsub_req = {
                "op": "UNSUB",
                "channel": [
                    # "askausdt@ticker",
                    "askausdt@depth",
                    # "739@trade"
                ],
                "id": 2
            }
        unsub_message = json.dumps(unsub_req)
        await websocket.send(unsub_message)
        # print(f"Sent message: {unsub_message}")

# Run the WebSocket client
asyncio.get_event_loop().run_until_complete(connect_to_websocket_server())
