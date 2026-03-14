from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Import route modules AFTER loading env
from routes import enrollments, courses, games, testimonials, schedule

# Inject database into route modules
enrollments.set_db(db)
courses.set_db(db)
games.set_db(db)
testimonials.set_db(db)
schedule.set_db(db)

# Create the main app without a prefix
app = FastAPI(title="Coding Stars API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check endpoint
@api_router.get("/")
async def root():
    return {
        "message": "Coding Stars API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

# Include all route modules
app.include_router(enrollments.router)
app.include_router(courses.router)
app.include_router(games.router)
app.include_router(testimonials.router)
app.include_router(schedule.router)

# Include the main API router
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Coding Stars API started successfully!")
    logger.info(f"📊 Database: {os.environ['DB_NAME']}")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("👋 Coding Stars API shut down")
