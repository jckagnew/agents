#!/usr/bin/env python3
"""
Lightweight Email Sender Utility
Uses Gmail SMTP with jckagnew@gmail.com as sender to avoid SendGrid conflicts
Perfect for one-off emails to jack@clevelsalesguy.com and other recipients
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from typing import Optional

class LightweightEmailSender:
    """Simple email sender using Gmail SMTP"""
    
    def __init__(self):
        load_dotenv(override=True)
        self.gmail_user = os.getenv("GMAIL_USER", "jckagnew@gmail.com")
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD")
        
        if not self.gmail_password:
            raise ValueError("GMAIL_APP_PASSWORD not found in environment variables!")
    
    def send_email(self, 
                   to_email: str, 
                   subject: str, 
                   content: str, 
                   is_html: bool = True,
                   from_name: str = "Jack Agnew") -> bool:
        """
        Send an email using Gmail SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            content: Email content (HTML or plain text)
            is_html: Whether content is HTML (default: True)
            from_name: Display name for sender (default: "Jack Agnew")
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{from_name} <{self.gmail_user}>"
            msg['To'] = to_email
            
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
            
            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Enable TLS
                server.login(self.gmail_user, self.gmail_password)
                server.send_message(msg)
            
            print(f"✅ Email sent successfully!")
            print(f"📧 From: {from_name} <{self.gmail_user}>")
            print(f"📧 To: {to_email}")
            print(f"📋 Subject: {subject}")
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {str(e)}")
            return False
    
    def send_markdown_email(self, 
                           to_email: str, 
                           subject: str, 
                           markdown_content: str,
                           from_name: str = "Jack Agnew") -> bool:
        """
        Send an email with markdown content converted to HTML
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            markdown_content: Markdown content to convert and send
            from_name: Display name for sender
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        
        html_content = self._markdown_to_html(markdown_content)
        return self.send_email(to_email, subject, html_content, is_html=True, from_name=from_name)
    
    def send_file_as_email(self, 
                          to_email: str, 
                          subject: str, 
                          file_path: str,
                          from_name: str = "Jack Agnew") -> bool:
        """
        Send a file as email content
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            file_path: Path to file to send
            from_name: Display name for sender
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Determine if it's markdown or HTML
            if file_path.endswith('.md'):
                return self.send_markdown_email(to_email, subject, content, from_name)
            elif file_path.endswith('.html'):
                return self.send_email(to_email, subject, content, is_html=True, from_name=from_name)
            else:
                return self.send_email(to_email, subject, content, is_html=False, from_name=from_name)
                
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return False
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
            return False
    
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

def main():
    """Example usage"""
    try:
        sender = LightweightEmailSender()
        
        # Example: Send the framework comparison
        success = sender.send_file_as_email(
            to_email="jack@clevelsalesguy.com",
            subject="🤖 AI Agent Framework Comparison Assessment - Complete Analysis",
            file_path="/Users/jackagnew/projects/agents/AI_AGENT_FRAMEWORK_COMPARISON.md"
        )
        
        if success:
            print("\n🎉 Email sent successfully!")
        else:
            print("\n❌ Failed to send email.")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Please set up Gmail App Password:")
        print("   1. Go to Google Account settings")
        print("   2. Security > 2-Step Verification > App passwords")
        print("   3. Generate an app password for 'Mail'")
        print("   4. Add it to your .env file as GMAIL_APP_PASSWORD=your_app_password")

if __name__ == "__main__":
    main()

