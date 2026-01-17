import asyncio
import websockets
import json
from orderbook import OrderBook

async def start_binance_feed(orderbook: OrderBook):
    """Connect to Binance WebSocket and update order book with real-time data"""
    uri = "wss://stream.binance.com:9443/ws/btcusdt@depth20@100ms"
    
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            # Parse the JSON message
            data = json.loads(message)
            
            # Clear current bids and asks
            orderbook.bids.clear()
            orderbook.asks.clear()
            
            # Process bids
            for bid in data.get('bids', []):
                price, qty = float(bid[0]), float(bid[1])
                orderbook.add_order("buy", price, qty)
            
            # Process asks
            for ask in data.get('asks', []):
                price, qty = float(ask[0]), float(ask[1])
                orderbook.add_order("sell", price, qty)
