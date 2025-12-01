"""Main FastAPI application for Artificial Consciousness Architecture backend."""

from contextlib import asynccontextmanager

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from backend.api import router, websocket_endpoint
from backend.services import get_session_manager
from src.utils.logger import configure_logging

# Load environment variables
load_dotenv()

# Configure logging
configure_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events.

    Args:
        app: The FastAPI application
    """
    # Startup
    logger.info("backend_server_starting")

    # Initialize session manager
    session_manager = get_session_manager()
    logger.info("session_manager_initialized")

    yield

    # Shutdown
    logger.info("backend_server_shutting_down")


# Create FastAPI app
app = FastAPI(
    title="Artificial Consciousness Architecture API",
    description="Backend API for Phase 0 - Foundation",
    version="0.5.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)

# WebSocket endpoint
app.add_websocket_route("/ws", websocket_endpoint)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information.

    Returns:
        HTML page with API documentation links
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Artificial Consciousness Architecture API</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #0a0a0a;
                color: #e0e0e0;
            }
            h1 {
                color: #3b82f6;
                border-bottom: 2px solid #3b82f6;
                padding-bottom: 10px;
            }
            h2 {
                color: #10b981;
                margin-top: 30px;
            }
            a {
                color: #3b82f6;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            code {
                background: #1a1a1a;
                padding: 2px 6px;
                border-radius: 3px;
                color: #f59e0b;
            }
            .endpoint {
                background: #1a1a1a;
                padding: 15px;
                margin: 10px 0;
                border-left: 3px solid #3b82f6;
                border-radius: 3px;
            }
            .method {
                display: inline-block;
                padding: 2px 8px;
                border-radius: 3px;
                font-weight: bold;
                margin-right: 10px;
            }
            .get { background: #10b981; color: #000; }
            .post { background: #3b82f6; color: #000; }
            .websocket { background: #8b5cf6; color: #000; }
        </style>
    </head>
    <body>
        <h1>🧠 Artificial Consciousness Architecture API</h1>
        <p><strong>Phase:</strong> 0.5 (Foundation + Web GUI)</p>
        <p><strong>Status:</strong> Running</p>

        <h2>📚 Documentation</h2>
        <ul>
            <li><a href="/docs">Interactive API Documentation (Swagger UI)</a></li>
            <li><a href="/redoc">Alternative Documentation (ReDoc)</a></li>
        </ul>

        <h2>🔌 API Endpoints</h2>

        <div class="endpoint">
            <span class="method post">POST</span>
            <code>/api/v1/interactions</code>
            <p>Process a user interaction and get response</p>
        </div>

        <div class="endpoint">
            <span class="method get">GET</span>
            <code>/api/v1/state</code>
            <p>Get current emotional state</p>
        </div>

        <div class="endpoint">
            <span class="method post">POST</span>
            <code>/api/v1/state/reset</code>
            <p>Reset emotional state to defaults</p>
        </div>

        <div class="endpoint">
            <span class="method get">GET</span>
            <code>/api/v1/memories</code>
            <p>Get episodic memories (paginated)</p>
        </div>

        <div class="endpoint">
            <span class="method get">GET</span>
            <code>/api/v1/memories/{memory_id}</code>
            <p>Get specific memory by ID</p>
        </div>

        <div class="endpoint">
            <span class="method get">GET</span>
            <code>/api/v1/memories/network</code>
            <p>Get memory network for visualization</p>
        </div>

        <div class="endpoint">
            <span class="method get">GET</span>
            <code>/api/v1/system/status</code>
            <p>Get overall system status</p>
        </div>

        <div class="endpoint">
            <span class="method get">GET</span>
            <code>/api/v1/system/timeline</code>
            <p>Get timeline of recent events</p>
        </div>

        <h2>⚡ WebSocket</h2>

        <div class="endpoint">
            <span class="method websocket">WS</span>
            <code>/ws</code>
            <p>Real-time updates (state changes, triggers, memory consolidation)</p>
            <p><strong>Channels:</strong> <code>state</code>, <code>triggers</code>, <code>memory</code>, <code>all</code></p>
        </div>

        <h2>🎯 Quick Test</h2>
        <p>Test the API with curl:</p>
        <pre style="background: #1a1a1a; padding: 15px; border-radius: 5px; overflow-x: auto;">
curl -X POST http://localhost:8000/api/v1/interactions \\
  -H "Content-Type: application/json" \\
  -d '{"message": "¿Cómo te sientes?"}'
        </pre>

        <h2>🔗 Links</h2>
        <ul>
            <li><a href="http://localhost:5173" target="_blank">Frontend (if running)</a></li>
            <li><a href="https://github.com/anthropics/martin-consienscy">GitHub Repository</a></li>
        </ul>

        <footer style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #2a2a2a; color: #606060;">
            <p>Artificial Consciousness Architecture - Phase 0.5</p>
            <p>Built with FastAPI • Integrated with Claude API</p>
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """Health check endpoint.

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "phase": "0.5",
        "service": "backend_api",
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("starting_backend_server", port=8000)

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload during development
        log_level="info",
    )
