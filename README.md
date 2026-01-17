# High-Frequency Limit Order Book Simulation

A high-performance Python implementation of a Limit Order Book (LOB) simulation with real-time data visualization and market-making capabilities.

## Core Concepts

### Price-Time Priority Matching Engine
This implementation follows the standard exchange matching algorithm where orders are executed based on:
- **Price Priority**: Higher bids and lower asks execute first
- **Time Priority**: Earlier orders at the same price level execute first

### Data Structures
- **Min-Heap for Asks**: Ensures lowest price orders are matched first (O(log n) complexity)
- **Max-Heap for Bids**: Simulated using negative prices to ensure highest price orders are matched first (O(log n) complexity)

## Features

### Real-Time Crypto Feed
**Live Mode** consumes the Binance WebSocket stream (`btcusdt@depth20@100ms`) to receive real-time order book updates:
- Uses `asyncio` and `websockets` for efficient asynchronous I/O
- Processes full snapshots every 100ms
- Updates the order book with current market data

### Simulation Mode
**Simulation Mode** features a threaded Market Maker bot that generates synthetic orders:
- Places Gaussian-distributed buy/sell orders around a mid-price
- Creates realistic market spread dynamics
- Demonstrates order book behavior in a controlled environment

### Visualization
Real-time rendering using Matplotlib's `FuncAnimation`:
- Side-by-side bar charts for bids (green) and asks (red)
- X-axis represents price, Y-axis represents cumulative volume
- Live mid-price calculation and display

## Tech Stack

- **Python 3.11**
- **Matplotlib** for real-time visualization
- **Asyncio** and **Websockets** for asynchronous network operations
- **Heapq** for efficient heap-based data structures

## Usage

### Dependencies
