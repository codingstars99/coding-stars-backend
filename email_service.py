import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "codingstars99@gmail.com"
        self.sender_password = os.environ.get('GMAIL_APP_PASSWORD', '')
        
    def send_enrollment_notification(self, enrollment_data: Dict) -> bool:
        """Send enrollment notification to company email"""
        try:
            if not self.sender_password:
                logger.warning("Gmail app password not set. Skipping email notification.")
                return False
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"New Enrollment Request - {enrollment_data['child_name']}"
            message["From"] = self.sender_email
            message["To"] = self.sender_email  # Send to same email (company email)
            
            # Create HTML content
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                        <h2 style="color: #f97316; border-bottom: 3px solid #ec4899; padding-bottom: 10px;">
                            🎓 New Enrollment Request
                        </h2>
                        
                        <div style="background-color: white; padding: 20px; border-radius: 8px; margin-top: 20px;">
                            <h3 style="color: #333; margin-top: 0;">Student Information</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Child Name:</strong></td>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;">{enrollment_data['child_name']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Child Age:</strong></td>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;">{enrollment_data['child_age']} years</td>
                                </tr>
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Interested Course:</strong></td>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;">{enrollment_data['course']}</td>
                                </tr>
                            </table>
                            
                            <h3 style="color: #333; margin-top: 30px;">Parent Information</h3>
                            <table style="width: 100%; border-collapse: collapse;">
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Parent Name:</strong></td>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;">{enrollment_data['parent_name']}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Email:</strong></td>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;">
                                        <a href="mailto:{enrollment_data['email']}" style="color: #f97316;">{enrollment_data['email']}</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;"><strong>Phone:</strong></td>
                                    <td style="padding: 10px; border-bottom: 1px solid #eee;">
                                        <a href="tel:{enrollment_data['phone']}" style="color: #f97316;">{enrollment_data['phone']}</a>
                                    </td>
                                </tr>
                            </table>
                            
                            {f'''
                            <h3 style="color: #333; margin-top: 30px;">Additional Message</h3>
                            <div style="background-color: #fef3e7; padding: 15px; border-radius: 5px; border-left: 4px solid #f97316;">
                                {enrollment_data.get('message', 'No additional message provided.')}
                            </div>
                            ''' if enrollment_data.get('message') else ''}
                            
                            <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee; text-align: center;">
                                <p style="color: #666; font-size: 14px;">
                                    📅 Enrollment request received on: {enrollment_data.get('created_at', 'N/A')}
                                </p>
                                <p style="color: #f97316; font-weight: bold; font-size: 16px;">
                                    Please contact the parent within 24 hours!
                                </p>
                            </div>
                        </div>
                        
                        <div style="margin-top: 20px; text-align: center; color: #999; font-size: 12px;">
                            <p>Coding Stars - Empowering Young Minds with World-Class Coding Education</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            # Attach HTML content
            html_part = MIMEText(html, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                
            logger.info(f"Enrollment notification sent successfully for {enrollment_data['child_name']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send enrollment notification: {str(e)}")
            return False

# Initialize email service
email_service = EmailService()
