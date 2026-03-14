from fastapi import APIRouter, HTTPException, status
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/courses", tags=["courses"])

# Database will be injected from server.py
db = None

def set_db(database):
    global db
    db = database

@router.get("", response_model=List[dict])
async def get_courses():
    """Get all courses"""
    try:
        courses = await db.courses.find().to_list(100)
        
        # Convert ObjectId to string
        for course in courses:
            course['_id'] = str(course['_id'])
            course['id'] = course.pop('_id')
            
        return courses
        
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch courses: {str(e)}"
        )

@router.get("/{course_id}", response_model=dict)
async def get_course(course_id: str):
    """Get a specific course by ID"""
    try:
        from bson import ObjectId
        
        course = await db.courses.find_one({"_id": ObjectId(course_id)})
        
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Course not found"
            )
        
        course['_id'] = str(course['_id'])
        course['id'] = course.pop('_id')
        
        return course
        
    except Exception as e:
        logger.error(f"Error fetching course: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch course: {str(e)}"
        )
