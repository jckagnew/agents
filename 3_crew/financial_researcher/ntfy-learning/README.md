# ntfy.sh Docker Learning Project

This project teaches Docker fundamentals through setting up a self-hosted push notification service.

## 🚀 Quick Start

1. **Start the service:**
   ```bash
   docker-compose up -d
   ```

2. **Test notifications:**
   ```bash
   curl -d "Hello Docker!" http://localhost:8080/mytopic
   ```

3. **Access the web interface:**
   Open http://localhost:8080 in your browser

## 🐳 Docker Commands to Learn

- `docker-compose up -d` - Start services in background
- `docker-compose down` - Stop and remove services
- `docker-compose logs ntfy` - View service logs
- `docker ps` - List running containers
- `docker logs ntfy` - View container logs
- `docker exec -it ntfy sh` - Enter the container

## 📱 Mobile Apps

- **Android**: Search "ntfy" in Google Play Store
- **iOS**: Search "ntfy" in App Store

## 🔧 Configuration

The service is configured to run on port 8080. Data is persisted in the `./ntfy_data` directory.

## 📚 Learning Objectives

- Understand Docker containers and images
- Learn Docker Compose for multi-container apps
- Practice Docker networking and port mapping
- Explore container health checks
- Learn about volume mounting for data persistence
