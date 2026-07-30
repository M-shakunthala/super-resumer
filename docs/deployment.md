# AI Job Agent - Production Deployment Guide

## 🐳 Docker Deployment

### Prerequisites
- Docker Desktop installed
- `.env` file with OPENAI_API_KEY configured

### Quick Start

1. **Build and Run with Docker Compose** (Recommended):
```bash
docker-compose up -d
```

This will start:
- **Bot Service**: Runs the AI job agent continuously
- **Dashboard Service**: Streamlit dashboard on port 8501

2. **Access Dashboard**:
```
http://localhost:8501
```

3. **View Logs**:
```bash
# Bot logs
docker-compose logs bot

# Dashboard logs  
docker-compose logs dashboard

# All logs
docker-compose logs -f
```

4. **Stop Services**:
```bash
docker-compose down
```

### Manual Docker Commands

**Build Image**:
```bash
docker build -t ai-job-agent .
```

**Run Bot**:
```bash
docker run -d \
  --name ai-job-agent-bot \
  --env-file .env \
  -v $(pwd)/jobs.db:/app/jobs.db \
  -v $(pwd)/resumes:/app/resumes \
  ai-job-agent
```

**Run Dashboard**:
```bash
docker run -d \
  --name ai-job-agent-dashboard \
  -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/jobs.db:/app/jobs.db \
  ai-job-agent \
  streamlit run ui/dashboard.py --server.port=8501 --server.address=0.0.0.0
```

### Docker Installation

**Mac (Homebrew)**:
```bash
brew install --cask docker
```

**Linux (Ubuntu)**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

**Alternative: Use Podman**
```bash
brew install podman
podman machine init
podman machine start
```

### Troubleshooting

**Homebrew Ruby Error**:
If you encounter Ruby syntax errors with Homebrew:
```bash
# Fix Homebrew
cd /usr/local/Homebrew
git fetch origin
git reset --hard origin/master

# Or reinstall Ruby
brew install ruby
```

**Docker Permission Issues**:
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

**Port Already in Use**:
```bash
# Change port in docker-compose.yml
# Or kill existing process
lsof -ti:8501 | xargs kill
```

## 🌐 Cloud Deployment Options

### Option 1: Railway (Simplest)
1. Push code to GitHub
2. Connect repository to Railway
3. Set environment variables
4. Deploy automatically

### Option 2: AWS EC2
1. Launch EC2 instance
2. Install Docker
3. Clone repository
4. Run docker-compose up

### Option 3: Google Cloud Run
1. Containerize application
2. Push to Container Registry
3. Deploy to Cloud Run
4. Set up scheduler

## 🔄 Automated Scheduling

### Using Cron (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Run every 6 hours
0 */6 * * * cd /path/to/project && docker-compose run bot
```

### Using Docker Cron
Add to docker-compose.yml:
```yaml
scheduler:
  image: ai-job-agent
  command: |
    sh -c "while true; do python run.py; sleep 21600; done"
  restart: unless-stopped
```

## 📊 Monitoring

### Health Checks
Add to docker-compose.yml:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8501"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Log Management
```bash
# View logs
docker-compose logs -f --tail=100 bot

# Export logs
docker-compose logs bot > bot_logs.txt
```

## 🔒 Security Considerations

1. **Environment Variables**: Never commit `.env` file
2. **Database Backups**: Regular backups of `jobs.db`
3. **API Keys**: Use secure secret management
4. **Network Isolation**: Use Docker networks for service isolation

## 🚀 Performance Optimization

1. **Resource Limits**: Set memory/CPU limits in docker-compose.yml
2. **Database Indexing**: Add indexes to frequently queried fields
3. **Log Rotation**: Implement log rotation to prevent disk filling
4. **Caching**: Add Redis for caching job results

## 📈 Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
bot:
  deploy:
    replicas: 3
```

### Load Balancing
Use Nginx or HAProxy for load balancing multiple instances

## 🛠️ Maintenance

**Update Application**:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Database Backup**:
```bash
docker run --rm -v $(pwd)/data:/data -v $(pwd)/backups:/backups \
  alpine tar czf /backups/jobs.db.$(date +%Y%m%d).tar.gz /data/jobs.db
```

**Clean Up**:
```bash
# Remove old images
docker image prune -a

# Remove stopped containers
docker container prune

# Remove unused volumes
docker volume prune
```