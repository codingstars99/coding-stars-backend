from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/games", tags=["games"])

# Database will be injected from server.py
db = None

def set_db(database):
    global db
    db = database

@router.get("", response_model=List[dict])
async def get_games():
    """Get all games and apps"""
    try:
        games = await db.games.find().to_list(100)
        
        # Convert ObjectId to string
        for game in games:
            game['_id'] = str(game['_id'])
            game['id'] = game.pop('_id')
            
        return games
        
    except Exception as e:
        logger.error(f"Error fetching games: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch games: {str(e)}"
        )
