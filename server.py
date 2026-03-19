from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")  # Ignore MongoDB's _id field
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class DemoRequest(BaseModel):
    name: str
    email: str
    phone: str
    message: Optional[str] = ""

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    # Convert to dict and serialize datetime to ISO string for MongoDB
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    # Exclude MongoDB's _id field from the query results
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    # Convert ISO string timestamps back to datetime objects
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

@api_router.post("/send-demo-request")
async def send_demo_request(request: DemoRequest):
    """
    Send demo request email to company
    """
    try:
        # Get email credentials from environment
        gmail_email = os.environ.get('GMAIL_EMAIL')
        gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
        
        if not gmail_email or not gmail_password:
            logger.error("Email credentials not configured")
            raise HTTPException(status_code=500, detail="Email service not configured")
        
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f'New Demo Class Request from {request.name}'
        msg['From'] = gmail_email
        msg['To'] = gmail_email  # Send to company email
        
        # Create HTML email body
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #FF6B6B 0%, #FFB88C 100%); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .info-row {{ margin: 15px 0; padding: 10px; background: white; border-left: 4px solid #FF6B6B; }}
                    .label {{ font-weight: bold; color: #FF6B6B; }}
                    .footer {{ margin-top: 20px; padding-top: 20px; border-top: 2px solid #ddd; font-size: 12px; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2 style="margin: 0;">🌟 New Demo Class Request</h2>
                        <p style="margin: 5px 0 0 0;">Coding Stars - Demo Booking</p>
                    </div>
                    <div class="content">
                        <p>A new student has requested a free demo class. Here are the details:</p>
                        
                        <div class="info-row">
                            <span class="label">👤 Name:</span> {request.name}
                        </div>
                        
                        <div class="info-row">
                            <span class="label">📧 Email:</span> {request.email}
                        </div>
                        
                        <div class="info-row">
                            <span class="label">📱 Phone:</span> {request.phone}
                        </div>
                        
                        <div class="info-row">
                            <span class="label">💬 Message:</span><br/>
                            {request.message if request.message else 'No message provided'}
                        </div>
                        
                        <div class="footer">
                            <p><strong>Action Required:</strong> Please contact the student as soon as possible to schedule their demo class.</p>
                            <p>Received: {datetime.now(timezone.utc).strftime('%B %d, %Y at %I:%M %p UTC')}</p>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send email via Gmail SMTP
        logger.info(f"Sending email for demo request from {request.name}")
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(gmail_email, gmail_password)
            smtp_server.send_message(msg)
        
        logger.info("Email sent successfully")
        
        return {
            "success": True,
            "message": "Demo request email sent successfully"
        }
        
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP Authentication failed - check email credentials")
        raise HTTPException(status_code=500, detail="Email authentication failed")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
