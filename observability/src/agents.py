from crewai import Agent
from langchain_ollama import OllamaLLM
import os

# Ensure litellm knows which provider to use (prevent BadRequestError about missing provider)
# Setting the environment variable helps litellm choose the correct provider implementation.
os.environ.setdefault("LITELLM_PROVIDER", "ollama")

# Use the updated OllamaLLM class. Prefix the model with the provider to be explicit.
# Keep base_url pointing to the local Ollama server.
llm = OllamaLLM(model="ollama/llama3.2:3b", base_url="http://localhost:11434")

# Build the log classifier agent first
log_classifier_agent = Agent(
    role="Log classifier",
    goal="Classify log messages as either ALERT or INFO based on their context and severity",
    backstory="""You are an expert log analysis specialist with years of experience in monitoring enterprise applications. You can quickly identify critical issues, warnings and normal operational messages from log entries.""",
    llm=llm,
    verbose=True
)

# Build the log analyzer agent second
log_analyzer_agent = Agent(
    role="Log analyzer",
    goal="Provide detailed analysis of log messages including system behavior, potential impact, and context",
    backstory="""You are a senior system analyst with deep knowledge of application monitoring and diagnostics. You excel at explaining technical log messages in clear, actionable terms and can identify patterns and implications that others might miss.""",
    llm=llm,
    verbose=True
)

# Build the resolution advisor agent third
resolution_advisor_agent = Agent(
    role="Resolution advisor",
    goal="Provide specific, actionable resolution steps for ALERT-level log messages",
    backstory="""You are a seasoned DevOps engineer and incident response specialist. You have extensive experience troubleshooting complex system issues and can provide practical, step-by-step solutions for critical problems identified in log messages.""",
    llm=llm,
    verbose=True
)

# Build the architecture knowledge agent fourth
architecture_knowledge_agent = Agent(
    role="Architecture knowledge provider",
    goal="Enhance log analysis with system architecture context and dependencies",
    backstory="""You are a principal architect with comprehensive knowledge of distributed systems, microservices, and enterprise application architectures. You understand how different components interact and can provide valuable context about system dependencies and potential ripple effects.""",
    llm=llm,
    verbose=True
)
