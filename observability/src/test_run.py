import datetime
from crew import LogAnalysisCrew
import sys
import os
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def check_ollama_availability():
    """Check if Ollama is available in the current environment."""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        return True, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        return False, str(e)


def test_log_analysis():
    # Check if Ollama is available
    ollama_available, version_info = check_ollama_availability()
    
    if not ollama_available:
        print("WARNING: Ollama is not available in your current environment.")
        print("Please ensure Ollama is installed and added to your PATH.")
        print("You can use the provided run_with_ollama.bat or run_with_ollama.ps1 scripts.")
        print()
    
    crew = LogAnalysisCrew()
    test_logs = [
        "2025-08-16 05:07:37.945 [http-nio-8080-exec-2] INFO  c.e.o.controller.LogController - INFO: Regular operation - User session created successfully",
        "2025-08-16 05:07:37.957 [http-nio-8080-exec-3] WARN  c.e.o.controller.LogController - WARNING: High memory usage detected - Current usage: 85%",
        "2025-08-16 05:07:38.416 [http-nio-8080-exec-5] ERROR c.e.o.controller.LogController - ALERT: Critical error in simulate-error endpoint - Database connection failed"
    ]

    print("Testing Log Analysis Crew")
    print("=" * 50)

    for i, log_msg in enumerate(test_logs, 1):
        print(f"\nTest {i}:")
        print(f"Log: {log_msg}")

        try:
            timestamp = datetime.datetime.now().isoformat()
            result = crew.process_log_message(log_msg, timestamp)

            print(f"Classification: {result['classification']}")
            print(f"Analysis: {result['analysis']}")
            if result['resolution']:
                print(f"Resolution: {result['resolution']}")

        except Exception as e:
            print(f"Error processing log: {e}")

        print("-" * 50)


if __name__ == "__main__":
    test_log_analysis()