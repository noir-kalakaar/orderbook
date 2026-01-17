import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np
from orderbook import OrderBook

class Visualizer:
    def __init__(self, orderbook: OrderBook):
        self.orderbook = orderbook
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 6))
        self.fig.suptitle('Limit Order Book Simulation')
        
        # Set up the bid side (left)
        self.ax1.set_title('Bids (Buy Orders)')
        self.ax1.set_xlabel('Price')
        self.ax1.set_ylabel('Volume')
        self.ax1.set_facecolor('lightgray')
        
        # Set up the ask side (right)
        self.ax2.set_title('Asks (Sell Orders)')
        self.ax2.set_xlabel('Price')
        self.ax2.set_ylabel('Volume')
        self.ax2.set_facecolor('lightgray')
        
        # Initialize empty plots
        self.bids_bar = None
        self.asks_bar = None
        
        # Set up the animation
        self.ani = animation.FuncAnimation(
            self.fig, self.update, interval=100, blit=False
        )
        
        plt.tight_layout()
        
    def update(self, frame):
        """Update the visualization with current order book state"""
        # Get depth data
        bids, asks = self.orderbook.get_depth()
        
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        
        # Plot bids (green bars)
        if bids:
            bid_prices = [price for price, qty in bids]
            bid_volumes = [qty for price, qty in bids]
            self.ax1.barh(bid_prices, bid_volumes, color='green', alpha=0.7)
            self.ax1.set_title('Bids (Buy Orders)')
            self.ax1.set_xlabel('Volume')
            self.ax1.set_ylabel('Price')
            self.ax1.set_facecolor('lightgray')
            self.ax1.invert_xaxis()  # Higher prices on top
            
        # Plot asks (red bars)
        if asks:
            ask_prices = [price for price, qty in asks]
            ask_volumes = [qty for price, qty in asks]
            self.ax2.barh(ask_prices, ask_volumes, color='red', alpha=0.7)
            self.ax2.set_title('Asks (Sell Orders)')
            self.ax2.set_xlabel('Volume')
            self.ax2.set_ylabel('Price')
            self.ax2.set_facecolor('lightgray')
            
        # Add grid for better readability
        self.ax1.grid(True, linestyle='--', alpha=0.7)
        self.ax2.grid(True, linestyle='--', alpha=0.7)
        
        # Set title with current mid price
        if bids and asks:
            best_bid = bids[0][0]
            best_ask = asks[0][0]
            mid_price = (best_bid + best_ask) / 2
            self.fig.suptitle(f'Limit Order Book Simulation - Mid Price: ${mid_price:.2f}')
        else:
            self.fig.suptitle('Limit Order Book Simulation')
            
        plt.tight_layout()
        
    def show(self):
        """Display the visualization"""
        plt.show()
