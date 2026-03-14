from fastapi import APIRouter, HTTPException, status
from typing import List
from models import Enrollment, EnrollmentCreate
from datetime import datetime
from email_service import email_service
import logging
import urllib.parse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/enrollments", tags=["enrollments"])

# Database will be injected from server.py
db = None

def set_db(database):
    global db
    db = database

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_enrollment(enrollment: EnrollmentCreate):
    """Create a new enrollment request"""
    try:
        # Convert to dict and add metadata
        enrollment_dict = enrollment.model_dump(by_alias=False)
        enrollment_dict['status'] = 'pending'
        enrollment_dict['created_at'] = datetime.utcnow()
        enrollment_dict['updated_at'] = datetime.utcnow()
        
        # Insert into database
        result = await db.enrollments.insert_one(enrollment_dict)
        enrollment_dict['_id'] = result.inserted_id
        
        # Send email notification to company
        email_sent = False
        try:
            enrollment_dict['created_at'] = enrollment_dict['created_at'].strftime("%B %d, %Y at %I:%M %p")
            email_sent = email_service.send_enrollment_notification(enrollment_dict)
        except Exception as e:
            logger.error(f"Email notification failed: {str(e)}")
        
        # Generate WhatsApp confirmation message
        whatsapp_number = "+917990612407"
        whatsapp_message = f"""Hi! I just enrolled my child for a free demo class at Coding Stars.

*Child Details:*
Name: {enrollment.child_name}
Age: {enrollment.child_age} years
Interested Course: {enrollment.course}

*Parent Details:*
Name: {enrollment.parent_name}
Phone: {enrollment.phone}
Email: {enrollment.email}

Looking forward to the demo class!"""
        
        # URL encode the message
        encoded_message = urllib.parse.quote(whatsapp_message)
        whatsapp_url = f"https://wa.me/{whatsapp_number.replace('+', '')}?text={encoded_message}"
        
        return {
            "success": True,
            "message": "Enrollment request submitted successfully!",
            "enrollment_id": str(result.inserted_id),
            "email_sent": email_sent,
            "whatsapp_url": whatsapp_url,
            "whatsapp_number": whatsapp_number
        }
        
    except Exception as e:
        logger.error(f"Error creating enrollment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create enrollment: {str(e)}"
        )

@router.get("", response_model=List[dict])
async def get_enrollments(skip: int = 0, limit: int = 100):
    """Get all enrollment requests (for admin)"""
    try:
        enrollments = await db.enrollments.find().skip(skip).limit(limit).sort("created_at", -1).to_list(limit)
        
        # Convert ObjectId to string
        for enrollment in enrollments:
            enrollment['_id'] = str(enrollment['_id'])
            enrollment['created_at'] = enrollment['created_at'].isoformat()
            enrollment['updated_at'] = enrollment['updated_at'].isoformat()
            
        return enrollments
        
    except Exception as e:
        logger.error(f"Error fetching enrollments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch enrollments: {str(e)}"
        )

@router.get("/{enrollment_id}", response_model=dict)
async def get_enrollment(enrollment_id: str):
    """Get a specific enrollment by ID"""
    try:
        from bson import ObjectId
        
        enrollment = await db.enrollments.find_one({"_id": ObjectId(enrollment_id)})
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        enrollment['_id'] = str(enrollment['_id'])
        enrollment['created_at'] = enrollment['created_at'].isoformat()
        enrollment['updated_at'] = enrollment['updated_at'].isoformat()
        
        return enrollment
        
    except Exception as e:
        logger.error(f"Error fetching enrollment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch enrollment: {str(e)}"
        )

@router.patch("/{enrollment_id}/status", response_model=dict)
async def update_enrollment_status(enrollment_id: str, status_update: dict):
    """Update enrollment status (for admin)"""
    try:
        from bson import ObjectId
        
        new_status = status_update.get('status')
        if new_status not in ['pending', 'contacted', 'enrolled', 'cancelled']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status value"
            )
        
        result = await db.enrollments.update_one(
            {"_id": ObjectId(enrollment_id)},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        return {
            "success": True,
            "message": "Enrollment status updated successfully"
        }
        
    except Exception as e:
        logger.error(f"Error updating enrollment status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update enrollment status: {str(e)}"
        )
