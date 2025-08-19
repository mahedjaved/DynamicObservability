import ollama
import re
import datetime
from typing import Dict, Any


class SimpleLogAnalyzer:
    """
    The stratergy here is to setup the following workflow: Each task its own function -> its own prompt 
    """

    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name

    def classify_log(self, log_message: str) -> str:
        """
        Classify log messages as ALERT or INFO
        The pompt defined here is no where close to what an actual production ready model would use, this is just a starter example
        """
        prompt = f"""
        Analyze this log messages and classify it as either "ALERT" or "INFO": 

        Log: {log_message}

        Classification critieria:
        - ALERT: Error messages, exceptions, critical warnings, system failures, performance issues, security concerns
        - INFO: Normal operational messages, successful operations, routine status updates

        Respond with only one word: ALERT or INFO
        """
        try:
            response = ollama.generate(
                model=self.model_name, prompt=prompt)
            classification = response["response"].strip().upper()

            # fallback classification based on log levels keywords - simply looks for keywords in the log and classifies as shown
            if classification not in ["ALERT", "INFO"]:
                if any(keyword in log_message.upper() for keyword in ['ERROR', 'CRITICAL', 'FATAL', 'EXCEPTION', 'FAILED', 'ALERT']):
                    classification = 'ALERT'
                elif any(keyword in log_message.upper() for keyword in ['WARN', 'WARNING']):
                    classification = 'ALERT'
                else:
                    classification = 'INFO'

            return classification
        except Exception as e:
            print(f"Error in classification: {e}")
            # Fallback classification
            if any(keyword in log_message.upper() for keyword in ['ERROR', 'CRITICAL', 'FATAL', 'EXCEPTION', 'FAILED', 'ALERT', 'WARN']):
                return 'ALERT'
            return 'INFO'

    def analyze_logs(self, log_message: str, classification: str) -> str:
        """
        Analyze logs and provide insights, resolution etc.
        """
        prompt = f"""
        Provide a brief analysis of this log message:

        Log: {log_message}
        Classification: {classification}

        Explain in 2-3 sentences:
        1. What this log indicates about system behavior
        2. Potential impact on the system or users
        3. Severity assessment if it's an ALERT

        Keep it concise and technical.
        """
        try:
            response = ollama.generate(
                model=self.model_name, prompt=prompt)
            return response['response'].strip()
        except Exception as e:
            print(f"Error in analysis: {e}")
            return f"Analysis unavailable. Log classified as {classification}."

    def get_resolution(self, log_message: str, analysis: str) -> str:
        """Get resolution steps for ALERT messages"""
        prompt = f"""
        Based on this ALERT log and analysis, provide specific resolution steps:

        Log: {log_message}
        Analysis: {analysis}

        Provide 3-4 actionable steps:
        1. Immediate actions
        2. Investigation steps  
        3. Potential fixes
        4. Prevention measures

        Keep recommendations practical and brief.
        """

        try:
            response = ollama.generate(
                model=self.model_name, prompt=prompt)
            return response['response'].strip()
        except Exception as e:
            print(f"Error getting resolution: {e}")
            return "Resolution steps unavailable. Please investigate manually."

    def process_log_message(self, log_message: str, timestamp: str = None) -> Dict[str, Any]:
        """Process a complete log message"""
        if not timestamp:
            timestamp = datetime.datetime.now().isoformat()

        # Step 1: Classify
        classification = self.classify_log(log_message)

        # Step 2: Analyze
        analysis = self.analyze_logs(log_message, classification)

        # Step 3: Get resolution if ALERT
        resolution = ""
        if classification == "ALERT":
            resolution = self.get_resolution(log_message, analysis)

        return {
            "timestamp": timestamp,
            "log_message": log_message,
            "classification": classification,
            "analysis": analysis,
            "resolution": resolution
        }


def test_analyzer():
    """
    Test the log analyzer
    """
    analyzer = SimpleLogAnalyzer()

    test_logs = [
        "2025-08-16 05:07:37.945 [http-nio-8080-exec-2] INFO  c.e.o.controller.LogController - INFO: Regular operation - User session created successfully",
        "2025-08-16 05:07:37.957 [http-nio-8080-exec-3] WARN  c.e.o.controller.LogController - WARNING: High memory usage detected - Current usage: 85%",
        "2025-08-16 05:07:38.416 [http-nio-8080-exec-5] ERROR c.e.o.controller.LogController - ALERT: Critical error in simulate-error endpoint - Database connection failed"
    ]

    print("Testing Simple Log Analyzer")
    print("=" * 50)

    for i, log_msg in enumerate(test_logs, 1):
        print(f"\nTest {i}:")
        print(f"Log: {log_msg}")

        try:
            result = analyzer.process_log_message(log_msg)

            print(f"Classification: {result['classification']}")
            print(f"Analysis: {result['analysis']}")
            if result['resolution']:
                print(f"Resolution: {result['resolution']}")

        except Exception as e:
            print(f"Error processing log: {e}")

        print("-" * 50)


if __name__ == "__main__":
    test_analyzer()