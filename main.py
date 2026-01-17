import heapq
import random
import time
from orderbook import OrderBook
from visualizer import Visualizer

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
        visualizer.update(orderbook)
        
        time.sleep(0.5)  # Wait 0.5 seconds between orders

if __name__ == "__main__":
    # Initialize order book and visualizer
    orderbook = OrderBook()
    visualizer = Visualizer(orderbook)
    
    # Start market maker bot
    market_maker_bot(orderbook, visualizer)
