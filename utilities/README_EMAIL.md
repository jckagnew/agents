# 📧 Email Utilities for AI Agents

This directory contains two powerful email sending utilities for different use cases in AI agent projects.

## 🚀 Quick Start

### Simple Email (Gmail SMTP)
```python
from utilities.email_simple import SimpleEmailSender, send_quick_email

# Quick one-liner
send_quick_email("user@example.com", "Subject", "Message")

# Full control
sender = SimpleEmailSender(from_name="My AI Agent")
sender.send_email(
    to_emails=["user@example.com"],
    subject="AI Agent Notification",
    content="<h1>Hello!</h1><p>This is from an AI agent.</p>",
    is_html=True
)
```

### SendGrid Email (Production)
```python
from utilities.email_sendgrid import SendGridEmailSender, send_quick_sendgrid_email

# Quick one-liner
send_quick_sendgrid_email(["user@example.com"], "Subject", "Message")

# Full control
sender = SendGridEmailSender(from_name="My AI Agent")
sender.send_email(
    to_emails=["user@example.com"],
    subject="AI Agent Notification",
    content="<h1>Hello!</h1><p>This is from an AI agent.</p>",
    is_html=True
)
```

## 📋 Setup Instructions

### Gmail SMTP Setup (Simple Email)
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication if not already enabled
3. Go to "App passwords" and generate a new app password for "Mail"
4. Add to your `.env` file:
   ```
   GMAIL_USER=your_email@gmail.com
   GMAIL_APP_PASSWORD=your_16_character_app_password
   ```

### SendGrid Setup (Production Email)
1. Go to [SendGrid](https://sendgrid.com) and create an account
2. Generate an API key in Settings > API Keys
3. Add to your `.env` file:
   ```
   SENDGRID_API_KEY=your_sendgrid_api_key_here
   SENDGRID_FROM_EMAIL=your_verified_email@domain.com
   ```

## 🛠️ Features Comparison

| Feature | Simple Email (Gmail) | SendGrid Email |
|---------|---------------------|----------------|
| **Setup Complexity** | ⭐ Easy | ⭐⭐ Medium |
| **Cost** | ⭐ Free | ⭐⭐ Paid (free tier available) |
| **Scalability** | ⭐⭐ Limited | ⭐⭐⭐ High |
| **Delivery Rate** | ⭐⭐ Good | ⭐⭐⭐ Excellent |
| **Analytics** | ❌ None | ✅ Detailed |
| **Templates** | ❌ No | ✅ Yes |
| **Bulk Sending** | ⭐ Limited | ⭐⭐⭐ Advanced |
| **Attachments** | ✅ Yes | ✅ Yes |
| **HTML Support** | ✅ Yes | ✅ Yes |
| **Personalization** | ⭐ Basic | ⭐⭐⭐ Advanced |

## 📚 Usage Examples

### 1. Simple Notifications
```python
from utilities.email_simple import send_quick_email

# Send a simple notification
send_quick_email(
    to_email="user@example.com",
    subject="Task Complete",
    message="Your AI agent has finished processing the request."
)
```

### 2. HTML Emails with Attachments
```python
from utilities.email_simple import SimpleEmailSender

sender = SimpleEmailSender(from_name="Document Processor")

html_content = """
<html>
<body>
    <h1>Document Processing Complete</h1>
    <p>Your documents have been processed successfully.</p>
    <ul>
        <li>Document 1: ✅ Processed</li>
        <li>Document 2: ✅ Processed</li>
    </ul>
</body>
</html>
"""

sender.send_email(
    to_emails=["user@example.com"],
    subject="Document Processing Complete",
    content=html_content,
    is_html=True,
    attachments=["/path/to/processed_doc.pdf"]
)
```

### 3. Bulk Emails with Personalization
```python
from utilities.email_sendgrid import SendGridEmailSender

sender = SendGridEmailSender(from_name="Marketing AI")

recipients = [
    {"email": "user1@example.com", "name": "John", "custom_args": {"user_id": "123"}},
    {"email": "user2@example.com", "name": "Jane", "custom_args": {"user_id": "456"}}
]

sender.send_bulk_email(
    recipients=recipients,
    subject="Hello {{name}}!",
    content="<h1>Hello {{name}}!</h1><p>Your user ID is {{user_id}}</p>",
    is_html=True
)
```

### 4. Template Emails
```python
from utilities.email_sendgrid import SendGridEmailSender

sender = SendGridEmailSender()

sender.send_template_email(
    to_emails=["user@example.com"],
    template_id="d-1234567890abcdef",
    dynamic_data={"name": "John", "company": "Acme Corp"}
)
```

### 5. Agent Integration
```python
from utilities.email_simple import SimpleEmailSender

class EmailAgent:
    def __init__(self):
        self.email_sender = SimpleEmailSender(from_name="AI Assistant")
    
    def send_task_completion(self, user_email: str, task_name: str):
        html_content = f"""
        <html>
        <body>
            <h2>Task Completed: {task_name}</h2>
            <p>Your AI agent has successfully completed the requested task.</p>
            <p>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body>
        </html>
        """
        
        return self.email_sender.send_email(
            to_emails=[user_email],
            subject=f"Task Complete: {task_name}",
            content=html_content,
            is_html=True
        )

# Use in your agent
agent = EmailAgent()
agent.send_task_completion("user@example.com", "Data Analysis")
```

## 🔧 Configuration

### Environment Variables
```bash
# Gmail SMTP
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password

# SendGrid
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=your_verified_email@domain.com
```

### Error Handling
Both utilities include comprehensive error handling:
- Configuration validation
- Network error handling
- File attachment error handling
- Detailed error messages
- Graceful failure modes

## 🎯 When to Use Which

### Use Simple Email (Gmail SMTP) when:
- ✅ Quick prototyping and testing
- ✅ Low volume sending (< 100 emails/day)
- ✅ Personal projects
- ✅ Internal notifications
- ✅ Cost is a concern
- ✅ Simple setup is preferred

### Use SendGrid Email when:
- ✅ Production applications
- ✅ High volume sending (> 100 emails/day)
- ✅ Marketing campaigns
- ✅ Need delivery analytics
- ✅ Need email templates
- ✅ Need advanced personalization
- ✅ Need bulk sending capabilities
- ✅ Need professional email delivery

## 🚨 Best Practices

### Security
- Never commit API keys or passwords to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Use app-specific passwords for Gmail

### Performance
- Batch emails when possible
- Use SendGrid for high-volume sending
- Implement retry logic for failed sends
- Monitor delivery rates

### User Experience
- Use clear, descriptive subjects
- Include both HTML and text versions
- Test emails before sending
- Respect unsubscribe preferences
- Keep emails concise and actionable

## 🔍 Troubleshooting

### Common Issues

#### Gmail SMTP Issues
- **Authentication failed**: Check app password
- **Connection refused**: Check firewall settings
- **Rate limited**: Reduce sending frequency

#### SendGrid Issues
- **API key invalid**: Verify key in SendGrid dashboard
- **Sender not verified**: Verify sender email in SendGrid
- **Template not found**: Check template ID
- **Rate limited**: Check account limits

### Debug Mode
Both utilities provide detailed logging. Check console output for specific error messages.

## 📈 Monitoring and Analytics

### Simple Email
- Basic success/failure logging
- Console output for debugging

### SendGrid
- Detailed delivery analytics
- Open/click tracking
- Bounce handling
- Unsubscribe management
- Webhook support

## 🔄 Migration Guide

### From Simple to SendGrid
1. Set up SendGrid account and API key
2. Replace import: `from utilities.email_sendgrid import SendGridEmailSender`
3. Update initialization: `sender = SendGridEmailSender()`
4. Test with small batch first
5. Monitor delivery rates

### From SendGrid to Simple
1. Set up Gmail app password
2. Replace import: `from utilities.email_simple import SimpleEmailSender`
3. Update initialization: `sender = SimpleEmailSender()`
4. Test with small batch first
5. Monitor for rate limiting

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages in console output
3. Verify environment variable configuration
4. Test with minimal examples first

---

**Happy emailing! 📧✨**
