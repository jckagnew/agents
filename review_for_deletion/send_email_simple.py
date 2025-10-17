#!/usr/bin/env python3
"""
Simple Email Sender - Alternative to SendGrid for one-off emails
Uses Gmail SMTP with jckagnew@gmail.com as sender
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

def send_simple_email():
    """Send the framework comparison via Gmail SMTP"""
    
    load_dotenv(override=True)
    
    # Try different possible environment variable names
    gmail_password = (
        os.getenv("GMAIL_APP_PASSWORD") or 
        os.getenv("GOOGLE_APP_PW") or 
        os.getenv("GMAIL_PASSWORD")
    )
    
    gmail_user = os.getenv("GMAIL_USER", "jckagnew@gmail.com")
    
    if not gmail_password:
        print("❌ Gmail App Password not found!")
        print("\n🔧 Setup Instructions:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2-Factor Authentication if not already enabled")
        print("3. Go to 'App passwords' and generate a new app password for 'Mail'")
        print("4. Add one of these to your .env file:")
        print("   GMAIL_APP_PASSWORD=your_16_character_app_password")
        print("   OR")
        print("   GOOGLE_APP_PW=your_16_character_app_password")
        print("   OR")
        print("   GMAIL_PASSWORD=your_16_character_app_password")
        print("\n💡 The app password will be 16 characters long (no spaces)")
        return False
    
    # Read the framework comparison document
    try:
        with open('/Users/jackagnew/projects/agents/AI_AGENT_FRAMEWORK_COMPARISON.md', 'r') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print("❌ Framework comparison document not found!")
        return False
    
    # Convert markdown to basic HTML
    html_content = convert_markdown_to_html(markdown_content)
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "🤖 AI Agent Framework Comparison Assessment - Complete Analysis"
        msg['From'] = f"Jack Agnew <{gmail_user}>"
        msg['To'] = "jack@clevelsalesguy.com"
        
        # Create HTML content with basic styling
        full_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                h3 {{ color: #7f8c8d; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #f2f2f2; font-weight: bold; }}
                code {{ background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-family: 'Courier New', monospace; }}
                pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                hr {{ border: none; border-top: 2px solid #eee; margin: 30px 0; }}
            </style>
        </head>
        <body>
            {html_content}
            <hr>
            <p><em>This comprehensive analysis was generated based on your current codebase and implementations. Use this as your guide for choosing the right AI agent framework for different problems after completing your class!</em></p>
            <p><strong>Sent from:</strong> {gmail_user}</p>
        </body>
        </html>
        """
        
        # Create text version
        text_content = f"""
AI Agent Framework Comparison Assessment

{markdown_content}

---
This comprehensive analysis was generated based on your current codebase and implementations. 
Use this as your guide for choosing the right AI agent framework for different problems after completing your class!

Sent from: {gmail_user}
        """
        
        # Attach parts
        text_part = MIMEText(text_content, 'plain')
        html_part = MIMEText(full_html, 'html')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Send email
        print(f"📧 Sending email from {gmail_user} to jack@clevelsalesguy.com...")
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable TLS
            server.login(gmail_user, gmail_password)
            server.send_message(msg)
        
        print("✅ Framework comparison successfully sent!")
        print(f"📧 From: Jack Agnew <{gmail_user}>")
        print(f"📧 To: jack@clevelsalesguy.com")
        print(f"📋 Subject: 🤖 AI Agent Framework Comparison Assessment - Complete Analysis")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        print("\n💡 Common issues:")
        print("   - App password might be incorrect")
        print("   - 2-Factor Authentication might not be enabled")
        print("   - Gmail might be blocking the login attempt")
        return False

def convert_markdown_to_html(markdown_text):
    """Basic markdown to HTML conversion"""
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
    
    # Tables (basic)
    lines = html.split('\n')
    in_table = False
    result_lines = []
    
    for line in lines:
        if '|' in line and not line.strip().startswith('|'):
            if not in_table:
                result_lines.append('<table>')
                in_table = True
            if '---' in line:
                continue  # Skip separator lines
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells:
                result_lines.append('<tr>')
                for cell in cells:
                    result_lines.append(f'<td>{cell}</td>')
                result_lines.append('</tr>')
        else:
            if in_table:
                result_lines.append('</table>')
                in_table = False
            result_lines.append(line)
    
    if in_table:
        result_lines.append('</table>')
    
    html = '\n'.join(result_lines)
    
    # Line breaks
    html = html.replace('\n', '<br>\n')
    
    return html

if __name__ == "__main__":
    print("🚀 Sending AI Agent Framework Comparison to jack@clevelsalesguy.com...")
    print("📧 Using Gmail SMTP with jckagnew@gmail.com as sender")
    print("🔧 This avoids SendGrid sender/recipient conflicts")
    print()
    
    success = send_simple_email()
    
    if success:
        print("\n🎉 Email sent successfully!")
        print("📋 The comprehensive framework comparison is now in your inbox.")
        print("💡 Use this as your reference guide for choosing the right AI agent framework!")
    else:
        print("\n❌ Failed to send email. Please check your Gmail configuration.")
        print("\n📝 Quick Setup:")
        print("1. Go to https://myaccount.google.com/security")
        print("2. Enable 2-Factor Authentication")
        print("3. Generate an App Password for 'Mail'")
        print("4. Add GMAIL_APP_PASSWORD=your_password to your .env file")

