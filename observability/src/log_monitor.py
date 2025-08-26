import ollama
import docker
import time
import json
import os
import threading
import requests

# Placeholder for architecture knowledge
architecture_knowledge = ""

# In-memory store for processed logs
processed_logs = []

# Monitoring state
monitoring_active = False
monitoring_thread = None

class LogProcessor:
    def __init__(self, model_name="llama3.2:1b"):
        self.model_name = model_name

    def process_log_message(self, log_message, timestamp):
        global architecture_knowledge
        
        prompt = f"""
        You are an observability agent analyzing logs from a microservice.
        The microservice is part of a larger system with the following architecture:
        {architecture_knowledge if architecture_knowledge else "No architecture knowledge provided."}

        Analyze the following log entry and classify it as either 'INFO' or 'ALERT'.
        If it's an 'ALERT', provide a concise analysis of the problem and a suggested resolution.
        If it's 'INFO', just provide a brief analysis.

        Log Entry:
        Timestamp: {timestamp}
        Message: {log_message}

        Provide your response in a JSON format with the following keys:
        - 'classification': 'INFO' or 'ALERT'
        - 'analysis': A brief analysis of the log message.
        - 'resolution': (Optional) Suggested resolution if the classification is 'ALERT'.
        """

        try:
            response = ollama.chat(model=self.model_name, messages=[{
                'role': 'user',
                'content': prompt,
            }])
            
            content = response["message"]["content"]
            
            # Attempt to parse JSON, handle potential malformed JSON
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError:
                # If JSON is malformed, try to extract relevant parts or default
                print(f"Warning: Malformed JSON from LLM: {content}")
                classification = "INFO"
                analysis = "Could not parse LLM response. Original: " + content[:100] + "..."
                resolution = ""
                
                if "ALERT" in content.upper():
                    classification = "ALERT"
                    analysis = "Potential alert detected, but LLM response malformed."
                    resolution = "Manually inspect logs."
                
                parsed_content = {
                    "classification": classification,
                    "analysis": analysis,
                    "resolution": resolution
                }

            return parsed_content
        except Exception as e:
            print(f"Error processing log with Ollama: {e}")
            return {
                "classification": "INFO",
                "analysis": f"Failed to analyze log due to LLM error: {e}",
                "resolution": ""
            }

class PodmanLogMonitor:
    def __init__(self, log_processor):
        self.log_processor = log_processor
        self.client = None
        self.container_name = None

    def connect_to_podman(self):
        try:
            # Try to connect to Podman using Docker-compatible API
            # Assumes Podman is running with `podman system service -t 0` or similar
            # Or PODMAN_HOST environment variable is set
            self.client = docker.from_env()
            self.client.ping()
            print("Successfully connected to Podman (Docker-compatible API).")
            return True
        except Exception as e:
            print(f"Could not connect to Podman: {e}")
            self.client = None
            return False

    def get_running_containers(self):
        if not self.client:
            if not self.connect_to_podman():
                return []
        try:
            containers = self.client.containers.list()
            return [{
                "id": c.id,
                "name": c.name,
                "status": c.status
            } for c in containers]
        except Exception as e:
            print(f"Error listing Podman containers: {e}")
            return []

    def stream_logs(self, container_name):
        if not self.client:
            if not self.connect_to_podman():
                return
        
        self.container_name = container_name
        print(f"Starting log stream for Podman container: {container_name}")
        try:
            container = self.client.containers.get(container_name)
            for line in container.logs(stream=True, follow=True):
                log_entry = line.decode("utf-8").strip()
                if log_entry:
                    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                    processed_data = self.log_processor.process_log_message(log_entry, timestamp)
                    processed_logs.append({
                        "timestamp": timestamp,
                        "log_message": log_entry,
                        "classification": processed_data.get("classification", "UNKNOWN"),
                        "analysis": processed_data.get("analysis", "N/A"),
                        "resolution": processed_data.get("resolution", "")
                    })
                    print(f"Processed Log: {processed_logs[-1]}")
        except Exception as e:
            print(f"Error streaming logs from Podman container {container_name}: {e}")

def start_monitoring(container_name):
    global monitoring_active, monitoring_thread
    if monitoring_active:
        print("Monitoring is already active.")
        return

    log_processor = LogProcessor()
    monitor = PodmanLogMonitor(log_processor)
    
    if not monitor.connect_to_podman():
        print("Failed to start monitoring: Could not connect to Podman.")
        return

    monitoring_active = True
    monitoring_thread = threading.Thread(target=monitor.stream_logs, args=(container_name,))
    monitoring_thread.daemon = True
    monitoring_thread.start()
    print(f"Monitoring started for {container_name}")

def stop_monitoring():
    global monitoring_active, monitoring_thread
    if monitoring_active:
        monitoring_active = False
        if monitoring_thread and monitoring_thread.is_alive():
            # In a real scenario, you might need a more robust way to stop the thread
            # For docker-py, stopping the container or client might break the stream
            print("Attempting to stop monitoring thread...")
        monitoring_thread = None
        print("Monitoring stopped.")
    else:
        print("Monitoring is not active.")

def get_processed_logs(limit=50, offset=0):
    return processed_logs[offset:offset+limit]

def get_monitoring_status():
    return monitoring_active

def get_architecture_knowledge():
    global architecture_knowledge
    return architecture_knowledge

def update_architecture_knowledge(new_knowledge):
    global architecture_knowledge
    architecture_knowledge = new_knowledge
    print("Architecture knowledge updated.")

if __name__ == "__main__":
    # Example Usage (for local testing)
    # Ensure you have a Podman container named 'log-test-microservice' running
    # And Ollama is running with 'llama3.2:1b' model pulled
    
    # Start a dummy microservice for testing if not already running
    # You would typically run your Java microservice here
    print("Starting dummy microservice for testing...")
    os.system("podman run -d --rm --name log-test-microservice alpine/git:latest sh -c \"while true; do echo INFO: This is an info log from dummy-app; sleep 2; echo ALERT: Something critical happened in dummy-app!; sleep 3; done\"")
    time.sleep(5)

    start_monitoring("log-test-microservice")
    
    try:
        while True:
            print(f"\nTotal processed logs: {len(processed_logs)}")
            for log in get_processed_logs(limit=5):
                print(f"[{log["classification"]}] {log["log_message"]}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopping monitoring...")
        stop_monitoring()
        print("Exited.")

    # Clean up dummy microservice
    os.system("podman stop log-test-microservice")