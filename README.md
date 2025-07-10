# Real-Time Price Data Generation and Streaming System

A production-ready system for generating and streaming real-time price data for virtual trading instruments using FastAPI, WebSockets, React, and TypeScript.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Quick Start with Docker](#quick-start-with-docker)
  - [Manual Installation](#manual-installation)
- [API Documentation](#api-documentation)
  - [REST API Endpoints](#rest-api-endpoints)
  - [WebSocket API](#websocket-api)
  - [API Test Cases for Postman](#api-test-cases-for-postman)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development Guide](#development-guide)
- [Testing](#testing)
- [Deployment](#deployment)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Real-Time Price Data System simulates a trading environment by generating random price fluctuations for virtual financial instruments (tickers). It provides both REST API endpoints for historical data and WebSocket connections for real-time price streaming.

### Key Capabilities

- **Automatic Price Generation**: Continuously generates realistic price movements
- **Real-time Streaming**: Low-latency WebSocket connections for live updates
- **Historical Data Access**: REST API for retrieving price history
- **Scalable Architecture**: Supports thousands of concurrent connections
- **Visual Analytics**: Interactive charts with real-time updates

## ✨ Features

### Core Features
- ✅ Configurable number of virtual tickers (instruments)
- ✅ Random price generation with configurable parameters
- ✅ Real-time WebSocket streaming per ticker
- ✅ RESTful API for ticker lists and historical data
- ✅ In-memory circular buffer for efficient data storage
- ✅ Automatic reconnection for WebSocket clients
- ✅ Interactive web interface with live charts

### Technical Features
- ✅ Asynchronous request handling with FastAPI
- ✅ Type-safe frontend with TypeScript
- ✅ Docker containerization
- ✅ CORS support for cross-origin requests
- ✅ Comprehensive error handling
- ✅ Structured logging
- ✅ Clean architecture with domain-driven design

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │
│   React Frontend    │◄────┤   FastAPI Backend   │
│                     │     │                     │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
           │ WebSocket                 │
           │ (Real-time)               │
           │                           │
           │ HTTP/REST                 │
           │ (Historical)              │
           │                           │
           └───────────────────────────┘
```

### Backend Architecture

```
backend/
├── API Layer (FastAPI)
│   ├── REST Routes
│   ├── WebSocket Routes
│   └── Dependencies
│
├── Service Layer
│   ├── Price Generator
│   ├── Ticker Service
│   └── WebSocket Manager
│
├── Domain Layer
│   ├── Entities (Ticker, Price)
│   └── Events (PriceUpdateEvent)
│
└── Repository Layer
    └── Price Repository (In-Memory)
```

### Data Flow

1. **Price Generation**:
   ```
   Price Generator → Price Repository → Event Bus → WebSocket Manager → Clients
   ```

2. **Client Request**:
   ```
   Client → API Route → Service → Repository → Response
   ```

## 🛠️ Technology Stack

### Backend
- **FastAPI** (0.109.0) - Modern async web framework
- **Python** (3.11+) - Core programming language
- **Uvicorn** - ASGI server
- **WebSockets** - Real-time communication
- **Pydantic** - Data validation
- **AsyncIO** - Asynchronous programming

### Frontend
- **React** (18.2.0) - UI library
- **TypeScript** (5.3.3) - Type-safe JavaScript
- **Recharts** (2.10.4) - Charting library
- **Axios** - HTTP client
- **CSS3** - Styling

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server & reverse proxy

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose (recommended)
- OR Python 3.11+ and Node.js 18+
- Git

### Quick Start with Docker

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd realtime-price-system
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```
   **NOTE**: Tested only on Intel based Mac.


3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Manual Installation

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Configure environment**:
   ```bash
   # Edit .env file as needed
   ```

5. **Run the backend**:
   ```bash
   python src/main.py
   ```

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   # Edit .env file as needed
   ```

4. **Start development server**:
   ```bash
   npm start
   ```

## 📚 API Documentation

### Base URLs

- **Local Development**: `http://localhost:8000`
- **Docker**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

### REST API Endpoints

#### 1. Health Check

Check if the API is running and healthy.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy"
}
```

#### 2. Get All Tickers

Retrieve a list of all available tickers with current prices.

**Endpoint**: `GET /api/v1/tickers`

**Response**:
```json
[
  {
    "id": "ITEM_00",
    "name": "Item 00",
    "current_price": 156.55,
    "initial_price": 150.00,
    "created_at": "2024-01-15T10:30:00.123456",
    "updated_at": "2024-01-15T10:35:45.789012"
  },
  {
    "id": "ITEM_01",
    "name": "Item 01",
    "current_price": 89.23,
    "initial_price": 85.50,
    "created_at": "2024-01-15T10:30:00.123456",
    "updated_at": "2024-01-15T10:35:45.789012"
  }
]
```

#### 3. Get Ticker History

Retrieve historical price data for a specific ticker.

**Endpoint**: `GET /api/v1/tickers/{ticker_id}/history`

**Path Parameters**:
- `ticker_id` (string, required): The ticker identifier (e.g., "ITEM_00")

**Query Parameters**:
- `limit` (integer, optional): Maximum number of price points to return (1-1000)

**Examples**:
- Get full history: `/api/v1/tickers/ITEM_00/history`
- Get last 50 points: `/api/v1/tickers/ITEM_00/history?limit=50`

**Response**:
```json
{
  "ticker": {
    "id": "ITEM_00",
    "name": "Item 00",
    "current_price": 156.55,
    "initial_price": 150.00,
    "created_at": "2024-01-15T10:30:00.123456",
    "updated_at": "2024-01-15T10:35:45.789012"
  },
  "history": [
    {
      "value": 150.00,
      "timestamp": "2024-01-15T10:30:00.123456"
    },
    {
      "value": 150.45,
      "timestamp": "2024-01-15T10:30:01.123456"
    },
    {
      "value": 151.23,
      "timestamp": "2024-01-15T10:30:02.123456"
    }
  ]
}
```

**Error Response (404)**:
```json
{
  "detail": "Ticker INVALID_ID not found"
}
```

### WebSocket API

#### WebSocket Connection

Connect to receive real-time price updates for a specific ticker.

**Endpoint**: `ws://localhost:8000/ws/{ticker_id}`

**Path Parameters**:
- `ticker_id` (string, required): The ticker identifier (e.g., "ITEM_00")

**Connection Example**:
```
ws://localhost:8000/ws/ITEM_00
```

**Message Format (Server → Client)**:

Price Update:
```json
{
  "type": "price_update",
  "data": {
    "ticker_id": "ITEM_00",
    "price": 156.78,
    "timestamp": "2024-01-15T10:35:50.123456"
  }
}
```

Error Message:
```json
{
  "type": "error",
  "message": "Error description"
}
```

**Connection Errors**:
- Code 4004: Ticker not found
- Code 1006: Abnormal closure



## ⚙️ Configuration

### Backend Configuration

Environment variables in `backend/.env`:

```env
# API Configuration
API_TITLE=Real-Time Price Data System
API_VERSION=1.0.0
API_PREFIX=/api/v1

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=false

# Price Generation Settings
TICKER_COUNT=10                    # Number of tickers to generate
PRICE_UPDATE_INTERVAL=1.0          # Update interval in seconds
PRICE_CHANGE_RANGE=1.0             # Max price change per update (+/-)
INITIAL_PRICE_MIN=50.0             # Minimum initial price
INITIAL_PRICE_MAX=200.0            # Maximum initial price

# Storage Configuration
MAX_HISTORY_SIZE=1000              # Max history points per ticker

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000","http://frontend:3000"]

# Logging
LOG_LEVEL=INFO
```

### Frontend Configuration

Environment variables in `frontend/.env`:

```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000
```

### Docker Configuration

Docker Compose environment overrides:

```yaml
environment:
  - TICKER_COUNT=20              # Increase number of tickers
  - PRICE_UPDATE_INTERVAL=0.5    # Faster updates
  - MAX_HISTORY_SIZE=5000        # More history
```

## 📁 Project Structure

```
realtime-price-system/
│
├── backend/                       # Backend application
│   ├── src/                      # Source code
│   │   ├── api/                  # API layer
│   │   │   ├── routes/          # Route handlers
│   │   │   └── dependencies.py  # Dependency injection
│   │   ├── core/                # Core functionality
│   │   │   ├── config.py        # Configuration
│   │   │   ├── events.py        # Event bus
│   │   │   └── logging.py       # Logging setup
│   │   ├── domain/              # Domain layer
│   │   │   ├── entities/        # Business entities
│   │   │   └── events/          # Domain events
│   │   ├── services/            # Business logic
│   │   │   ├── price_generator.py
│   │   │   ├── ticker_service.py
│   │   │   └── websocket_manager.py
│   │   ├── repositories/        # Data access
│   │   │   └── price_repository.py
│   │   └── main.py              # Application entry
│   ├── tests/                   # Test files
│   ├── requirements.txt         # Dependencies
│   ├── Dockerfile              # Container definition
│   └── .env                    # Environment template
│
├── frontend/                   # Frontend application
│   ├── public/                 # Static assets
│   ├── src/                    # Source code
│   │   ├── components/         # React components
│   │   ├── hooks/              # Custom hooks
│   │   ├── services/           # API services
│   │   ├── types/              # TypeScript types
│   │   ├── utils/              # Utilities
│   │   ├── App.tsx             # Main component
│   │   └── index.tsx           # Entry point
│   ├── package.json            # Dependencies
│   ├── tsconfig.json           # TypeScript config
│   ├── Dockerfile              # Container definition
│   └── .env                    # Environment template
│
├── docker-compose.yml          # Multi-container setup
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 👨‍💻 Development Guide

### Code Style

#### Backend (Python)
- Follow PEP 8 guidelines
- Use type hints
- Format with Black
- Lint with Flake8
- Type check with MyPy

```bash
# Format code
black src/

# Lint
flake8 src/

# Type check
mypy src/
```

#### Frontend (TypeScript/React)
- Follow React best practices
- Use functional components
- Implement proper TypeScript types
- Format with Prettier
- Lint with ESLint

```bash
# Format code
npm run format

# Lint
npm run lint
```

### Adding a New Feature

1. **Backend Feature**:
   ```python
   # 1. Add domain entity if needed
   # src/domain/entities/new_entity.py
   
   # 2. Create service
   # src/services/new_service.py
   
   # 3. Add API route
   # src/api/routes/new_routes.py
   
   # 4. Update dependencies
   # src/api/dependencies.py
   
   # 5. Write tests
   # tests/unit/test_new_service.py
   ```

2. **Frontend Feature**:
   ```typescript
   // 1. Add types
   // src/types/index.ts
   
   // 2. Create component
   // src/components/NewComponent.tsx
   
   // 3. Add hook if needed
   // src/hooks/useNewFeature.ts
   
   // 4. Update services
   // src/services/api.ts
   ```

#

## 🧪 Testing

### Backend Testing

```bash

cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_price_generator.py -v

# Run integration tests
pytest tests/integration/ -v
```

### Frontend Testing

```bash

cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage --watchAll=false

# Run in watch mode
npm test -- --watchAll
```



## 🚢 Deployment

### Docker Deployment

#### Production Build

```bash
# Build images
docker-compose build --no-cache

# Run in production mode
docker-compose up -d

# View logs
docker-compose logs -f

# Scale backend
docker-compose up -d --scale backend=3
```



## 📊 Performance


### Optimization Tips

1. **Backend Optimizations**:
   - Use connection pooling
   - Implement caching for static data
   - Batch WebSocket messages
   - Use Redis for distributed systems

2. **Frontend Optimizations**:
   - Implement virtual scrolling for large lists
   - Use React.memo for expensive components
   - Throttle chart updates
   - Lazy load components

## 🔧 Troubleshooting

### Common Issues

#### WebSocket Connection Fails

**Problem**: Client cannot connect to WebSocket

**Solutions**:
1. Check CORS configuration
2. Verify WebSocket URL
3. Check firewall/proxy settings
4. Ensure ticker ID exists

```javascript
// Debug WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/ITEM_00');
ws.onerror = (error) => console.error('WebSocket error:', error);
ws.onclose = (event) => console.log('WebSocket closed:', event.code, event.reason);
```

#### Price Updates Stop

**Problem**: Price generation stops after some time

**Solutions**:
1. Check backend logs for errors
2. Verify price generator is running
3. Check memory usage
4. Restart the backend service

```bash
# Check logs
docker-compose logs backend | grep ERROR

# Restart service
docker-compose restart backend
```

#### High Memory Usage

**Problem**: Application uses too much memory

**Solutions**:
1. Reduce `MAX_HISTORY_SIZE`
2. Limit number of tickers
3. Implement data archival
4. Use Redis for storage

#### CORS Errors

**Problem**: Frontend cannot access backend API

**Solutions**:
1. Update CORS_ORIGINS in backend config
2. Check proxy configuration
3. Verify API URLs in frontend

### Debug Mode

Enable debug logging:

```python
# Backend
LOG_LEVEL=DEBUG

# Frontend
localStorage.setItem('debug', 'websocket:*');
```

### Health Checks

Monitor system health:

```bash
# Check API health
curl http://localhost:8000/health

# Check WebSocket
wscat -c ws://localhost:8000/ws/ITEM_00

# Check Docker containers
docker-compose ps

# View resource usage
docker stats
```

## 🤝 Contributing

### Getting Started

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
