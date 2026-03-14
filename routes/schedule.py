from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/schedule", tags=["schedule"])

# Database will be injected from server.py
db = None

def set_db(database):
    global db
    db = database

@router.get("", response_model=List[dict])
async def get_schedule():
    """Get weekly class schedule"""
    try:
        schedules = await db.schedule.find({"is_active": True}).to_list(7)
        
        # Convert ObjectId to string
        for schedule in schedules:
            schedule['_id'] = str(schedule['_id'])
            schedule['id'] = schedule.pop('_id')
            
        return schedules
        
    except Exception as e:
        logger.error(f"Error fetching schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch schedule: {str(e)}"
        )
