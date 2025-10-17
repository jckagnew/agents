#!/usr/bin/env python3
"""
SendGrid Email Sender Utility
Scalable, professional email sending using SendGrid API
Perfect for production applications, marketing campaigns, and high-volume sending
"""

import os
import base64
from typing import List, Optional, Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, 
    Email, 
    To, 
    Cc, 
    Bcc, 
    Subject, 
    Content, 
    Attachment, 
    FileContent, 
    FileName, 
    FileType, 
    Disposition,
    Personalization,
    CustomArg,
    Header
)
from dotenv import load_dotenv

class SendGridEmailSender:
    """Professional email sender using SendGrid API"""
    
    def __init__(self, from_email: str = None, from_name: str = "AI Assistant"):
        """
        Initialize the SendGrid email sender
        
        Args:
            from_email: Sender email (defaults to SENDGRID_FROM_EMAIL env var)
            from_name: Display name for sender
        """
        load_dotenv(override=True)
        
        self.api_key = os.getenv('SENDGRID_API_KEY')
        if not self.api_key:
            raise ValueError(
                "SENDGRID_API_KEY not found in environment variables!\n"
                "Please set up SendGrid:\n"
                "1. Go to https://sendgrid.com and create an account\n"
                "2. Generate an API key in Settings > API Keys\n"
                "3. Add it to your .env file as SENDGRID_API_KEY=your_api_key_here"
            )
        
        self.from_email = from_email or os.getenv("SENDGRID_FROM_EMAIL", "jckagnew@gmail.com")
        self.from_name = from_name
        self.sg = SendGridAPIClient(api_key=self.api_key)
    
    def send_email(self, 
                   to_emails: List[str], 
                   subject: str, 
                   content: str, 
                   is_html: bool = True,
                   cc_emails: List[str] = None,
                   bcc_emails: List[str] = None,
                   attachments: List[str] = None,
                   custom_args: Dict[str, str] = None,
                   headers: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Send an email using SendGrid API
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            content: Email content (HTML or plain text)
            is_html: Whether content is HTML (default: True)
            cc_emails: List of CC email addresses (optional)
            bcc_emails: List of BCC email addresses (optional)
            attachments: List of file paths to attach (optional)
            custom_args: Custom arguments for tracking (optional)
            headers: Custom headers (optional)
        
        Returns:
            Dict with status information
        """
        
        try:
            # Create the email
            from_email = Email(self.from_email, self.from_name)
            to_email = To(to_emails[0]) if len(to_emails) == 1 else None
            
            # Create content
            if is_html:
                content_type = "text/html"
            else:
                content_type = "text/plain"
            
            content_obj = Content(content_type, content)
            
            # Create mail object
            if to_email:
                mail = Mail(from_email, to_email, subject, content_obj)
            else:
                mail = Mail(from_email, subject, content_obj)
            
            # Add additional recipients
            if len(to_emails) > 1:
                for email in to_emails[1:]:
                    mail.add_to(To(email))
            
            if cc_emails:
                for email in cc_emails:
                    mail.add_cc(Cc(email))
            
            if bcc_emails:
                for email in bcc_emails:
                    mail.add_bcc(Bcc(email))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    attachment = self._create_attachment(file_path)
                    if attachment:
                        mail.add_attachment(attachment)
            
            # Add custom arguments
            if custom_args:
                for key, value in custom_args.items():
                    mail.add_custom_arg(CustomArg(key, value))
            
            # Add custom headers
            if headers:
                for key, value in headers.items():
                    mail.add_header(Header(key, value))
            
            # Send email
            response = self.sg.send(mail)
            
            result = {
                "success": response.status_code in [200, 202],
                "status_code": response.status_code,
                "message": "Email sent successfully" if response.status_code in [200, 202] else "Email sending failed",
                "response": response.body.decode('utf-8') if response.body else None
            }
            
            if result["success"]:
                print(f"✅ Email sent successfully!")
                print(f"📧 From: {self.from_name} <{self.from_email}>")
                print(f"📧 To: {', '.join(to_emails)}")
                if cc_emails:
                    print(f"📋 CC: {', '.join(cc_emails)}")
                if bcc_emails:
                    print(f"📋 BCC: {', '.join(bcc_emails)}")
                if attachments:
                    print(f"📎 Attachments: {len(attachments)} files")
                print(f"📋 Subject: {subject}")
            else:
                print(f"❌ Email sending failed with status {response.status_code}")
                print(f"Response: {result['response']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error sending email: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "status_code": None,
                "message": error_msg,
                "response": None
            }
    
    def send_bulk_email(self, 
                       recipients: List[Dict[str, Any]], 
                       subject: str, 
                       content: str, 
                       is_html: bool = True,
                       attachments: List[str] = None) -> Dict[str, Any]:
        """
        Send bulk emails with personalization
        
        Args:
            recipients: List of dicts with 'email' and optional 'name', 'custom_args'
            subject: Email subject (can use {{name}} for personalization)
            content: Email content (can use {{name}} for personalization)
            is_html: Whether content is HTML (default: True)
            attachments: List of file paths to attach (optional)
        
        Returns:
            Dict with status information
        """
        
        try:
            from_email = Email(self.from_email, self.from_name)
            content_type = "text/html" if is_html else "text/plain"
            content_obj = Content(content_type, content)
            
            mail = Mail(from_email, subject, content_obj)
            
            # Add personalizations
            for recipient in recipients:
                personalization = Personalization()
                personalization.add_to(To(recipient['email'], recipient.get('name')))
                
                # Add custom arguments if provided
                if 'custom_args' in recipient:
                    for key, value in recipient['custom_args'].items():
                        personalization.add_custom_arg(CustomArg(key, value))
                
                mail.add_personalization(personalization)
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    attachment = self._create_attachment(file_path)
                    if attachment:
                        mail.add_attachment(attachment)
            
            # Send email
            response = self.sg.send(mail)
            
            result = {
                "success": response.status_code in [200, 202],
                "status_code": response.status_code,
                "message": f"Bulk email sent to {len(recipients)} recipients" if response.status_code in [200, 202] else "Bulk email sending failed",
                "recipients_count": len(recipients),
                "response": response.body.decode('utf-8') if response.body else None
            }
            
            if result["success"]:
                print(f"✅ Bulk email sent successfully to {len(recipients)} recipients!")
            else:
                print(f"❌ Bulk email sending failed with status {response.status_code}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error sending bulk email: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "status_code": None,
                "message": error_msg,
                "recipients_count": 0,
                "response": None
            }
    
    def send_template_email(self, 
                          to_emails: List[str], 
                          template_id: str, 
                          dynamic_data: Dict[str, Any] = None,
                          cc_emails: List[str] = None,
                          bcc_emails: List[str] = None) -> Dict[str, Any]:
        """
        Send email using SendGrid template
        
        Args:
            to_emails: List of recipient email addresses
            template_id: SendGrid template ID
            dynamic_data: Data to populate template variables
            cc_emails: List of CC email addresses (optional)
            bcc_emails: List of BCC email addresses (optional)
        
        Returns:
            Dict with status information
        """
        
        try:
            from_email = Email(self.from_email, self.from_name)
            
            mail = Mail()
            mail.from_email = from_email
            mail.template_id = template_id
            
            # Add recipients
            for email in to_emails:
                mail.add_to(To(email))
            
            if cc_emails:
                for email in cc_emails:
                    mail.add_cc(Cc(email))
            
            if bcc_emails:
                for email in bcc_emails:
                    mail.add_bcc(Bcc(email))
            
            # Add dynamic data
            if dynamic_data:
                personalization = Personalization()
                for key, value in dynamic_data.items():
                    personalization.add_custom_arg(CustomArg(key, str(value)))
                mail.add_personalization(personalization)
            
            # Send email
            response = self.sg.send(mail)
            
            result = {
                "success": response.status_code in [200, 202],
                "status_code": response.status_code,
                "message": "Template email sent successfully" if response.status_code in [200, 202] else "Template email sending failed",
                "template_id": template_id,
                "response": response.body.decode('utf-8') if response.body else None
            }
            
            if result["success"]:
                print(f"✅ Template email sent successfully!")
                print(f"📧 Template ID: {template_id}")
            else:
                print(f"❌ Template email sending failed with status {response.status_code}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error sending template email: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                "success": False,
                "status_code": None,
                "message": error_msg,
                "template_id": template_id,
                "response": None
            }
    
    def _create_attachment(self, file_path: str) -> Optional[Attachment]:
        """Create SendGrid attachment from file"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encoded_file = base64.b64encode(data).decode()
            filename = os.path.basename(file_path)
            
            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            attachment = Attachment(
                FileContent(encoded_file),
                FileName(filename),
                FileType(mime_type),
                Disposition('attachment')
            )
            
            print(f"📎 Added attachment: {filename}")
            return attachment
            
        except FileNotFoundError:
            print(f"❌ Warning: Attachment file not found: {file_path}")
            return None
        except Exception as e:
            print(f"❌ Warning: Error creating attachment {file_path}: {str(e)}")
            return None

# Convenience functions for quick use
def send_quick_sendgrid_email(to_emails: List[str], subject: str, content: str, is_html: bool = True) -> Dict[str, Any]:
    """Quick function to send an email using SendGrid"""
    try:
        sender = SendGridEmailSender()
        return sender.send_email(to_emails, subject, content, is_html)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"success": False, "message": str(e)}

def send_bulk_sendgrid_email(recipients: List[Dict[str, Any]], subject: str, content: str, is_html: bool = True) -> Dict[str, Any]:
    """Quick function to send bulk emails using SendGrid"""
    try:
        sender = SendGridEmailSender()
        return sender.send_bulk_email(recipients, subject, content, is_html)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"success": False, "message": str(e)}

if __name__ == "__main__":
    """Example usage"""
    try:
        sender = SendGridEmailSender(from_name="Test Sender")
        
        # Example: Send a simple email
        result = sender.send_email(
            to_emails=["test@example.com"],
            subject="Test SendGrid Email",
            content="<h1>Test Email</h1><p>This is a test email from SendGrid.</p>",
            is_html=True
        )
        
        if result["success"]:
            print("\n🎉 Test email sent successfully!")
        else:
            print(f"\n❌ Failed to send test email: {result['message']}")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
