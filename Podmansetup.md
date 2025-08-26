# Podman Setup Guide for Observability Agent

This guide explains how to set up and use the observability agent system with Podman instead of Docker.

## Prerequisites

1. **Podman Installation**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install -y podman

   # RHEL/CentOS/Fedora
   sudo dnf install -y podman
   ```

2. **Python Dependencies**
   ```bash
   pip3 install docker ollama flask flask-cors PyPDF2 pillow pytesseract
   ```

3. **Ollama Installation**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama3.2:1b
   ```

## Key Changes for Podman Compatibility

### 1. Docker API Compatibility

The system uses the Docker Python client (`docker-py`) which is compatible with Podman when Podman is configured to provide a Docker-compatible API.

**Enable Podman Docker API:**
```bash
# Start Podman socket service
systemctl --user enable podman.socket
systemctl --user start podman.socket

# Or start manually for testing
podman system service -t 0 unix:///run/user/$UID/podman/podman.sock
```

**Set Environment Variables:**
```bash
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock
```

### 2. Updated Log Monitor

The `log_monitor_podman.py` file includes:
- **Podman Connection**: Uses Docker-compatible API to connect to Podman
- **Container Management**: Lists and monitors Podman containers
- **Log Streaming**: Real-time log streaming from Podman containers
- **AI Integration**: Same Ollama integration for log analysis

### 3. Backend Integration

The Flask backend (`observability-backend/src/routes/logs.py`) has been updated to:
- Import `log_monitor_podman` instead of `log_monitor`
- Remove OpenShift-specific functionality
- Focus on Podman container monitoring

## Setup Instructions

### 1. Start Podman Services

```bash
# Enable and start Podman socket
systemctl --user enable podman.socket
systemctl --user start podman.socket

# Verify Podman is working
podman ps
```

### 2. Start Ollama Service

```bash
# Start Ollama in background
ollama serve &

# Pull the model
ollama pull llama3.2:1b
```

### 3. Start Test Microservice

```bash
# Build the microservice image
podman build -t observability-microservice .

# Run the microservice
podman run -d -p 8080:8080 --name test-microservice observability-microservice
```

### 4. Start the Observability Backend

```bash
cd observability-backend
source venv/bin/activate
python src/main.py
```

### 5. Access the Web UI

Open your browser and navigate to `http://localhost:5000`

## Usage

### 1. Container Monitoring

1. **Load Containers**: The web UI will automatically load available Podman containers
2. **Select Container**: Choose the container you want to monitor from the dropdown
3. **Start Monitoring**: Click "Start Docker Monitoring" (works with Podman)
4. **View Logs**: Real-time log analysis will appear in the table

### 2. Architecture Knowledge

1. **Upload Diagrams**: Use the drag-and-drop area to upload PDF or image files
2. **Processing**: Files are processed using OCR to extract text
3. **Enhanced Analysis**: The AI uses this knowledge for better log classification

### 3. Log Analysis

The system provides:
- **Real-time Processing**: Logs are analyzed as they are generated
- **Classification**: INFO vs ALERT based on content
- **Analysis**: AI-powered explanation of log entries
- **Resolution**: Suggested solutions for ALERT-level issues

## Troubleshooting

### 1. Podman Connection Issues

```bash
# Check if Podman socket is running
systemctl --user status podman.socket

# Test Podman API
curl -H "Content-Type: application/json" \
  --unix-socket /run/user/$UID/podman/podman.sock \
  http://localhost/v1.40/containers/json
```

### 2. Container Not Found

```bash
# List all containers
podman ps -a

# Check container logs
podman logs test-microservice
```

### 3. Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Test model
echo "Test message" | ollama run llama3.2:1b
```

### 4. Backend Errors

```bash
# Check Flask logs
cd observability-backend
source venv/bin/activate
python src/main.py

# Test API endpoints
curl http://localhost:5000/api/status
curl http://localhost:5000/api/containers
```

## Performance Considerations

### 1. Resource Usage

- **Ollama**: Requires 2-4GB RAM depending on model size
- **Podman**: Minimal overhead compared to Docker
- **Backend**: ~100MB RAM for Flask application

### 2. Model Selection

- **llama3.2:1b**: Lightweight, faster processing, good for testing
- **llama3.3**: More accurate but requires more resources

### 3. Log Volume

- System can handle moderate log volumes (100-1000 logs/minute)
- For high-volume scenarios, consider batching or sampling

## Security Considerations

### 1. Podman Rootless

- Run Podman in rootless mode for better security
- User-specific socket prevents privilege escalation

### 2. Network Access

- Backend only binds to localhost by default
- Use reverse proxy for external access

### 3. File Uploads

- Architecture uploads are validated for file type and size
- Files are processed in isolated environment

## Deployment Options

### 1. Local Development

Use the setup described above for local development and testing.

### 2. Server Deployment

```bash
# Use systemd service for backend
sudo cp observability-backend.service /etc/systemd/system/
sudo systemctl enable observability-backend
sudo systemctl start observability-backend
```

### 3. Container Deployment

The entire system can be containerized using Podman:

```bash
# Build backend container
podman build -t observability-backend observability-backend/

# Run with Podman socket mounted
podman run -d \
  -p 5000:5000 \
  -v /run/user/$UID/podman/podman.sock:/var/run/docker.sock \
  observability-backend
```

## Differences from Docker

### 1. Socket Location

- **Docker**: `/var/run/docker.sock`
- **Podman**: `/run/user/$UID/podman/podman.sock`

### 2. Rootless Operation

- **Docker**: Typically runs as root
- **Podman**: Can run rootless by default

### 3. Systemd Integration

- **Docker**: Uses Docker daemon
- **Podman**: Integrates with systemd for container management

### 4. Image Storage

- **Docker**: Centralized in `/var/lib/docker`
- **Podman**: User-specific in `~/.local/share/containers`

## Conclusion

The observability agent system works seamlessly with Podman through its Docker-compatible API. The main advantages of using Podman include:

- **Security**: Rootless containers by default
- **Resource Efficiency**: No daemon overhead
- **Systemd Integration**: Better integration with system services
- **Compatibility**: Drop-in replacement for Docker in most cases

For production deployments, Podman offers a more secure and efficient alternative to Docker while maintaining full compatibility with the observability agent system.