from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/testimonials", tags=["testimonials"])

# Database will be injected from server.py
db = None

def set_db(database):
    global db
    db = database

@router.get("", response_model=List[dict])
async def get_testimonials():
    """Get all approved testimonials"""
    try:
        testimonials = await db.testimonials.find({"is_approved": True}).to_list(100)
        
        # Convert ObjectId to string
        for testimonial in testimonials:
            testimonial['_id'] = str(testimonial['_id'])
            testimonial['id'] = testimonial.pop('_id')
            
        return testimonials
        
    except Exception as e:
        logger.error(f"Error fetching testimonials: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch testimonials: {str(e)}"
        )
