#!/usr/bin/env python3
"""
Simple Email Sender Utility
Uses Gmail SMTP for quick, lightweight email sending
Perfect for one-off emails, notifications, and simple communications
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from typing import Optional, List
import mimetypes

class SimpleEmailSender:
    """Simple email sender using Gmail SMTP"""
    
    def __init__(self, from_email: str = None, from_name: str = "AI Assistant"):
        """
        Initialize the simple email sender
        
        Args:
            from_email: Sender email (defaults to GMAIL_USER env var)
            from_name: Display name for sender
        """
        load_dotenv(override=True)
        
        self.from_email = from_email or os.getenv("GMAIL_USER", "jckagnew@gmail.com")
        self.from_name = from_name
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")
        
        if not self.gmail_password:
            raise ValueError(
                "GMAIL_APP_PASSWORD not found in environment variables!\n"
                "Please set up Gmail App Password:\n"
                "1. Go to https://myaccount.google.com/security\n"
                "2. Enable 2-Factor Authentication if not already enabled\n"
                "3. Go to 'App passwords' and generate a new app password for 'Mail'\n"
                "4. Add it to your .env file as GMAIL_APP_PASSWORD=your_16_character_app_password"
            )
    
    def send_email(self, 
                   to_emails: List[str], 
                   subject: str, 
                   content: str, 
                   is_html: bool = True,
                   cc_emails: List[str] = None,
                   bcc_emails: List[str] = None,
                   attachments: List[str] = None) -> bool:
        """
        Send an email using Gmail SMTP
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            content: Email content (HTML or plain text)
            is_html: Whether content is HTML (default: True)
            cc_emails: List of CC email addresses (optional)
            bcc_emails: List of BCC email addresses (optional)
            attachments: List of file paths to attach (optional)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = ', '.join(to_emails)
            
            if cc_emails:
                msg['Cc'] = ', '.join(cc_emails)
            
            # Create content
            if is_html:
                # Create both HTML and text versions
                text_content = self._html_to_text(content)
                text_part = MIMEText(text_content, 'plain')
                html_part = MIMEText(content, 'html')
                msg.attach(text_part)
                msg.attach(html_part)
            else:
                text_part = MIMEText(content, 'plain')
                msg.attach(text_part)
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    self._add_attachment(msg, file_path)
            
            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Enable TLS
                server.login(self.from_email, self.gmail_password)
                
                # Combine all recipients
                all_recipients = to_emails.copy()
                if cc_emails:
                    all_recipients.extend(cc_emails)
                if bcc_emails:
                    all_recipients.extend(bcc_emails)
                
                server.send_message(msg, to_addrs=all_recipients)
            
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
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False
    
    def send_simple_notification(self, 
                                to_email: str, 
                                subject: str, 
                                message: str) -> bool:
        """
        Send a simple text notification
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            message: Simple text message
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        return self.send_email(
            to_emails=[to_email],
            subject=subject,
            content=message,
            is_html=False
        )
    
    def send_html_email(self, 
                       to_emails: List[str], 
                       subject: str, 
                       html_content: str,
                       cc_emails: List[str] = None) -> bool:
        """
        Send an HTML email
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            html_content: HTML content
            cc_emails: List of CC email addresses (optional)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        return self.send_email(
            to_emails=to_emails,
            subject=subject,
            content=html_content,
            is_html=True,
            cc_emails=cc_emails
        )
    
    def send_file_as_email(self, 
                          to_emails: List[str], 
                          subject: str, 
                          file_path: str,
                          cc_emails: List[str] = None) -> bool:
        """
        Send a file as email content
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            file_path: Path to file to send
            cc_emails: List of CC email addresses (optional)
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determine if it's markdown or HTML
            if file_path.endswith('.md'):
                html_content = self._markdown_to_html(content)
                return self.send_html_email(to_emails, subject, html_content, cc_emails)
            elif file_path.endswith('.html'):
                return self.send_html_email(to_emails, subject, content, cc_emails)
            else:
                return self.send_email(to_emails, subject, content, is_html=False, cc_emails=cc_emails)
                
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return False
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
            return False
    
    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """Add attachment to email message"""
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(file_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            
            msg.attach(part)
            print(f"📎 Added attachment: {filename}")
            
        except FileNotFoundError:
            print(f"❌ Warning: Attachment file not found: {file_path}")
        except Exception as e:
            print(f"❌ Warning: Error adding attachment {file_path}: {str(e)}")
    
    def _markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML"""
        html = markdown_text
        
        # Headers
        html = html.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
        html = html.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')
        html = html.replace('### ', '<h3>').replace('\n### ', '</h3>\n<h3>')
        
        # Bold and italic
        html = html.replace('**', '<strong>').replace('**', '</strong>')
        html = html.replace('*', '<em>').replace('*', '</em>')
        
        # Code blocks
        html = html.replace('```python', '<pre><code>').replace('```', '</code></pre>')
        html = html.replace('```', '<pre><code>').replace('```', '</code></pre>')
        html = html.replace('`', '<code>').replace('`', '</code>')
        
        # Lists
        html = html.replace('- ', '<li>').replace('\n- ', '</li>\n<li>')
        html = html.replace('✅ ', '<span style="color: #27ae60; font-weight: bold;">✅ ').replace('✅ ', '</span>')
        html = html.replace('❌ ', '<span style="color: #e74c3c; font-weight: bold;">❌ ').replace('❌ ', '</span>')
        
        # Line breaks
        html = html.replace('\n', '<br>\n')
        
        return html
    
    def _html_to_text(self, html_content: str) -> str:
        """Basic HTML to text conversion"""
        import re
        
        # Remove HTML tags
        text = re.sub('<[^<]+?>', '', html_content)
        
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()
        
        return text

# Convenience functions for quick use
def send_quick_email(to_email: str, subject: str, message: str, from_name: str = "AI Assistant") -> bool:
    """Quick function to send a simple email"""
    try:
        sender = SimpleEmailSender(from_name=from_name)
        return sender.send_simple_notification(to_email, subject, message)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def send_html_email(to_emails: List[str], subject: str, html_content: str, cc_emails: List[str] = None) -> bool:
    """Quick function to send an HTML email"""
    try:
        sender = SimpleEmailSender()
        return sender.send_html_email(to_emails, subject, html_content, cc_emails)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    """Example usage"""
    try:
        sender = SimpleEmailSender(from_name="Test Sender")
        
        # Example: Send a simple notification
        success = sender.send_simple_notification(
            to_email="test@example.com",
            subject="Test Notification",
            message="This is a test email from the Simple Email Sender."
        )
        
        if success:
            print("\n🎉 Test email sent successfully!")
        else:
            print("\n❌ Failed to send test email.")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
