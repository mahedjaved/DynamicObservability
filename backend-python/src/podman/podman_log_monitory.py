"""
Implementation of log monitoring and integration with Openshift via Podman containers using the Docker API (too long winded :D TODO find podman apis if available)
"""

import re
import ollama
import docker
import time
import json
import os
import threading
import requests

architecture_knowledge = ""

processed_logs = []

# monitoring state
monitoring_active = False
monitoring_thread = None


class LogProcessor:
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name

    def process_log_message(self, log_message, timestamp):
        global architecture_knowledge

        prompt = f"""
        You are an observability agent analyzing log from a microservice. The microservice is part of a larger system with the following architecture: {architecture_knowledge if architecture_knowledge else "No architecture knowledge provided."}

        Analyze the following log entry and classify it as either 'INFO' or 'ALERT'.
        If it's an 'ALERT', provide a concise analysis of the problem and a suggested resolution.
        If it's 'INFO', just provide a brief analysis.

        Log Entry:
        Timestamp: {timestamp}
        Message: {log_message}

        Provide your response in a JSON format with the following keys: 
        - 'classification': 'INFO' or 'ALERT'
        - 'analysis': A brief analysis of the log message
        - 'resolution': (Optional) Suggested resolution if the classification is 'ALERT'.
        """

        try:
            response = ollama.chat(model=self.model_name, messages=[{
                'role': 'user',
                'content': prompt,
            }])

            content = response["message"]["content"]

            # this section of code deals in the case if LLM output response in malformed -- Call upon human intervention for manual inspection of logs!
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError as e:
                # if json output is malformed we only take the relevant parts
                print(f"Warning: Malformed JSON from LLM: {content}")
                classification = "INFO"
                analysis = "Could not parse LLM response. Original: " + \
                    content[:100] + "..."
                resolution = ""

                if "ALERT" in content.upper():
                    classification = "ALERT"
                    analysis = "Potential alert detected, but LLM response  is malformed."
                    resolution = "Manually inspect logs."

                parsed_content = {
                    "classification": classification,
                    "analysis": analysis,
                    "resolution": resolution
                }

            return parsed_content

        except Exception as e:
            print(f"Error processing log with Ollama: {str(e)}")
            return {
                "classification": "INFO",
                "analysis": f"Failed to analyze log due to LLM error: {str(e)}",
                "resolution": ""
            }


class PodmanLogMonitor:
    def __init__(self, log_processor):
        self.log_processor = log_processor
        self.client = None
        self.container_name = None

    def connect_to_podman(self):
        try:
            # Try to connect to Podman using Docker  API
            # First ensure Podman is running with `podman system service -t 0` or similar
            # Or PODMAN_HOST environment variable is set
            self.client = docker.from_env()
            self.client.ping()
            print("Successfully connected to Podman via dockerapi")
            return True
        except Exception as e:
            print(f"Could not connect to Podman: {str(e)}")
            self.client = None
            return False

    def get_running_containers(self):
        """TODO: Continue from here!"""
        pass
