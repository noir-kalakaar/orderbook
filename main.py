import heapq
import random
import time
from orderbook import OrderBook
from visualizer import Visualizer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import defaultdict
import asyncio
import threading

def market_maker_bot(orderbook, visualizer):
    """Market maker bot that places orders around mid-price"""
    mid_price = 100.0
    spread = 2.0  # 2 dollar spread
    
    while True:
        # Place buy order
        buy_price = mid_price - spread/2 + random.uniform(-1, 1)
        buy_qty = random.randint(1, 10)
        orderbook.add_order("buy", buy_price, buy_qty)
        
        # Place sell order
        sell_price = mid_price + spread/2 + random.uniform(-1, 1)
        sell_qty = random.randint(1, 10)
        orderbook.add_order("sell", sell_price, sell_qty)
        
        # Update visualization
        # visualizer.update(orderbook)
        
        time.sleep(0.1)  # Wait 0.1 seconds between orders

async def live_mode(orderbook, visualizer):
    """Live mode using Binance WebSocket feed"""
    # Import here to avoid issues with async
    from binance_feed import start_binance_feed
    
    # Start the Binance feed in a separate thread to avoid blocking
    def run_async():
        asyncio.run(start_binance_feed(orderbook))
    
    # Run the async function in a separate thread
    thread = threading.Thread(target=run_async)
    thread.daemon = True
    thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Live mode stopped")

if __name__ == "__main__":
    # Initialize order book and visualizer
    orderbook = OrderBook()
    visualizer = Visualizer(orderbook)
    
    # Ask user for mode
    print("Choose mode:")
    print("1. Simulation Mode")
    print("2. Live Mode (Binance)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Start market maker bot in a thread
        import threading
        bot_thread = threading.Thread(target=market_maker_bot, args=(orderbook, visualizer))
        bot_thread.daemon = True
        bot_thread.start()
        
        # Show the visualization
        visualizer.show()
    elif choice == "2":
        # Start live mode
        print("Starting live mode with Binance WebSocket...")
        live_mode(orderbook, visualizer)
    else:
        print("Invalid choice. Starting simulation mode by default.")
        # Start market maker bot in a thread
        import threading
        bot_thread = threading.Thread(target=market_maker_bot, args=(orderbook, visualizer))
        bot_thread.daemon = True
        bot_thread.start()
        
        # Show the visualization
        visualizer.show()
