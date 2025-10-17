# trading_app/app/main.py

from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.v1 import auth, ai  # Import new ai router
from app.clients.librarian import librarian_client

# Use lifespan events to manage the aiohttp session
@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup, the client session is created implicitly on first use
    yield
    # On shutdown, gracefully close the client session
    await librarian_client.close()
    
# Using uvloop for performance, as specified in the tech stack
# uvicorn automatically detects and uses it if installed.
try:
    import uvloop
    uvloop.install()
except ImportError:
    print("uvloop not available, falling back to default event loop.")

app = FastAPI(
    title="Trading App",
    version="0.1.0",
    description="API for portfolio and asset management.",
    default_response_class=ORJSONResponse, # High-performance JSON library
)


# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"]) # Add the new router

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}

# This part is for local development and will not be used by Uvicorn in production
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)