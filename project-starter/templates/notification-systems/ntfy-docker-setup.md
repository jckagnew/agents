# 🐳 ntfy.sh Docker Setup - Project Starter Template

## Overview

This template provides a complete, automated setup for ntfy.sh push notifications using Docker. It includes both local development and cloud deployment options.

## Quick Start

### Option A: Automated Local Setup (Recommended for Development)

```bash
# Clone and setup
git clone <your-repo>
cd your-project
./auto-start.sh
```

**Features:**
- ✅ Automatic IP detection
- ✅ Dynamic configuration updates
- ✅ One-command startup
- ✅ iPhone app integration
- ✅ Test notifications

### Option B: Cloud Hosting (Recommended for Production)

```bash
# Deploy to cloud
./deploy-cloud.sh
```

**Features:**
- ✅ Always accessible
- ✅ No IP management
- ✅ Professional domain
- ✅ Scales automatically

### Option C: Website Integration (Recommended for Business)

```bash
# Integrate with existing website
cd your-website
# Add API endpoints and deploy
```

**Features:**
- ✅ Professional integration
- ✅ User management
- ✅ Analytics and reporting
- ✅ Multi-tenant support

## File Structure

```
your-project/
├── auto-start.sh              # Automated startup script
├── deploy-cloud.sh            # Cloud deployment script
├── docker-compose.yml         # Docker configuration
├── .env                       # Environment variables
├── README.md                  # Documentation
├── test-interface.html        # Web testing interface
└── migrate-from-pushover.sh   # Migration helper
```

## Configuration

### Environment Variables

```bash
# .env file (auto-generated)
NTFY_SERVER_IP=192.168.0.146
NTFY_SERVER_URL=http://192.168.0.146:8080
NTFY_TOPIC=mytopic
DOCKER_COMPOSE_FILE=docker-compose.yml
```

### Docker Compose

```yaml
services:
  ntfy:
    image: binwiederhier/ntfy:latest
    container_name: ntfy
    command:
      - serve
      - --base-url=http://192.168.0.146:8080
    ports:
      - "0.0.0.0:8080:80"
    volumes:
      - ./ntfy_data:/var/lib/ntfy
    environment:
      - NTFY_BASE_URL=http://192.168.0.146:8080
    restart: unless-stopped
```

## Usage

### Basic Commands

```bash
# Start service
./auto-start.sh

# Stop service
docker compose down

# View logs
docker logs ntfy

# Test notification
curl -d "Hello World!" http://localhost:8080/mytopic
```

### iPhone Configuration

1. Download ntfy app from App Store
2. Add server: `http://YOUR_IP:8080`
3. Subscribe to topic: `mytopic`

### API Integration

```bash
# Send notification
curl -X POST http://localhost:8080/mytopic \
  -H "Content-Type: text/plain" \
  -H "X-Title: My Title" \
  -H "X-Priority: 5" \
  -d "Hello World!"

# Send with actions
curl -X POST http://localhost:8080/mytopic \
  -H "Content-Type: text/plain" \
  -H "X-Actions: view, Open Link, https://example.com" \
  -d "Click here!"
```

## Migration from Pushover

### API Comparison

| Pushover | ntfy.sh |
|----------|---------|
| `curl -s --form-string "token=TOKEN" --form-string "user=USER" --form-string "message=Hello" https://api.pushover.net/1/messages.json` | `curl -d "Hello" http://localhost:8080/mytopic` |
| `--form-string "priority=1"` | `-H "X-Priority: 5"` |
| `--form-string "title=Title"` | `-H "X-Title: Title"` |
| `--form-string "url=https://example.com"` | `-H "X-Actions: view, Open Link, https://example.com"` |

### Migration Script

```bash
# Run migration helper
./migrate-from-pushover.sh
```

## Cloud Deployment

### Railway (Recommended)

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Deploy: `railway up`
4. Get URL: `railway domain`

### Render

1. Push to GitHub
2. Connect to Render
3. Use `render.yaml` configuration
4. Deploy automatically

### Vercel Integration

1. Add API routes to Next.js app
2. Deploy to Vercel
3. Use public ntfy.sh service
4. Integrate with existing features

## Troubleshooting

### Common Issues

**Service not accessible:**
- Check IP address: `./auto-start.sh`
- Verify firewall settings
- Test localhost: `curl http://localhost:8080/health`

**iPhone can't connect:**
- Ensure both devices on same WiFi
- Check server URL in app
- Verify port 8080 is open

**Notifications not received:**
- Check topic subscription
- Verify message format
- Test with web interface

### Debug Commands

```bash
# Check service status
docker ps | grep ntfy

# View logs
docker logs ntfy

# Test connectivity
curl -v http://localhost:8080/health

# Check IP address
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## Advanced Features

### Custom Topics

```bash
# Create user-specific topics
curl -d "User message" http://localhost:8080/user123
curl -d "System alert" http://localhost:8080/system
curl -d "Marketing" http://localhost:8080/marketing
```

### Priority Levels

```bash
# Min priority
curl -d "Low priority" -H "X-Priority: 1" http://localhost:8080/mytopic

# Max priority
curl -d "URGENT!" -H "X-Priority: 5" http://localhost:8080/mytopic
```

### Rich Notifications

```bash
# With title and actions
curl -d "Check this out!" \
  -H "X-Title: Important Update" \
  -H "X-Actions: view, Open Link, https://example.com" \
  http://localhost:8080/mytopic
```

## Integration Examples

### Home Assistant

```yaml
notify:
  - platform: rest
    name: ntfy
    resource: http://192.168.0.146:8080/mytopic
    method: POST
```

### Node.js

```javascript
const sendNotification = async (message, title, priority = 3) => {
  const response = await fetch('http://192.168.0.146:8080/mytopic', {
    method: 'POST',
    headers: {
      'Content-Type': 'text/plain',
      'X-Title': title,
      'X-Priority': priority.toString()
    },
    body: message
  });
  return response.json();
};
```

### Python

```python
import requests

def send_notification(message, title=None, priority=3):
    headers = {'Content-Type': 'text/plain'}
    if title:
        headers['X-Title'] = title
    headers['X-Priority'] = str(priority)
    
    response = requests.post(
        'http://192.168.0.146:8080/mytopic',
        headers=headers,
        data=message
    )
    return response.json()
```

## Best Practices

1. **Use descriptive topics** for different types of notifications
2. **Set appropriate priorities** to avoid notification fatigue
3. **Include actionable content** with X-Actions when possible
4. **Test thoroughly** before deploying to production
5. **Monitor logs** for debugging issues
6. **Backup configuration** for easy restoration
7. **Use environment variables** for different environments
8. **Implement error handling** in your applications

## Support

- **Documentation**: https://ntfy.sh/docs
- **GitHub**: https://github.com/binwiederhier/ntfy
- **Issues**: https://github.com/binwiederhier/ntfy/issues
- **Community**: https://github.com/binwiederhier/ntfy/discussions
