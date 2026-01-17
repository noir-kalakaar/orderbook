import heapq
import time
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Order:
    id: int
    side: str  # 'buy' or 'sell'
    price: float
    qty: int
    timestamp: float

class OrderBook:
    def __init__(self):
        # Min-heap for asks (sell orders)
        self.asks = []
        # Max-heap for bids (buy orders) - using negative prices
        self.bids = []
        self.order_id_counter = 0
        
    def add_order(self, side: str, price: float, qty: int):
        """Add an order to the order book"""
        self.order_id_counter += 1
        order = Order(self.order_id_counter, side, price, qty, time.time())
        
        if side == "buy":
            # For bids, store negative price to simulate max-heap
            heapq.heappush(self.bids, (-order.price, order))
        else:  # sell
            heapq.heappush(self.asks, (order.price, order))
            
        # Try to match orders
        self.match_order()
    
    def match_order(self):
        """Match buy and sell orders"""
        # While we have matching orders
        while self.asks and self.bids:
            # Get the best ask (lowest price)
            ask_price, ask_order = heapq.heappop(self.asks)
            # Get the best bid (highest price)
            bid_price, bid_order = heapq.heappop(self.bids)
            
            # If bid price >= ask price, match them
            if bid_order.price >= ask_order.price:
                # Calculate matched quantity
                matched_qty = min(bid_order.qty, ask_order.qty)
                
                # Update quantities
                bid_order.qty -= matched_qty
                ask_order.qty -= matched_qty
                
                # If there's remaining quantity, put back in heap
                if bid_order.qty > 0:
                    heapq.heappush(self.bids, (-bid_order.price, bid_order))
                else:
                    # If bid is fully matched, we can add it to execution log
                    pass
                    
                if ask_order.qty > 0:
                    heapq.heappush(self.asks, (ask_price, ask_order))
                else:
                    # If ask is fully matched, we can add it to execution log
                    pass
            else:
                # No match, put back the orders
                heapq.heappush(self.bids, (bid_price, bid_order))
                heapq.heappush(self.asks, (ask_price, ask_order))
                break
    
    def get_depth(self) -> Tuple[List[Tuple[float, int]], List[Tuple[float, int]]]:
        """Get cumulative depth for bids and asks"""
        # Process bids (max-heap)
        bids = []
        bid_heap_copy = self.bids.copy()
        cumulative_qty = 0
        
        # Sort bids by price descending (highest first)
        sorted_bids = sorted(bid_heap_copy, key=lambda x: -x[0])
        
        for price, order in sorted_bids:
            cumulative_qty += order.qty
            bids.append((price, cumulative_qty))
        
        # Process asks (min-heap)
        asks = []
        ask_heap_copy = self.asks.copy()
        cumulative_qty = 0
        
        # Sort asks by price ascending (lowest first)
        sorted_asks = sorted(ask_heap_copy, key=lambda x: x[0])
        
        for price, order in sorted_asks:
            cumulative_qty += order.qty
            asks.append((price, cumulative_qty))
            
        return bids, asks
