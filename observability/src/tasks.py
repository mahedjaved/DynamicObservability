from crewai import Task


def create_classification_task(agent, log_message, timestamp):
    """
    Create a task to classify a log message
    """
    return Task(
        description=f"""
        Analyze the following log message and classify it as either "ALERT" or "INFO":

        Timestamp: {timestamp}
        Log message: {log_message}

        Classification criteria:
        - ALERT: Error messages, exceptions, critical warnings, system failures, performance issues, security concerns, or any message indicating problems
        - INFO: Normal operational messages, successful operations, routine status updates

        Respond with only one word: either "ALERT" or "INFO"
        """,
        expected_output="A single word classification: ALERT or INFO",
        agent=agent
    )


def create_analysis_task(agent, log_message, timestamp, classification):
    """
    Creates a task to analyse a log message
    """
    return Task(
        description=f"""
        Provide a detailed description of the log message:

        Timestamp: {timestamp}
        Log Message: {log_message}
        Classification: {classification}

        Your analysis should include:
        1. What the log message indicates about system behavior
        2. Potential impact on the system or users
        3. Context about the component or operation involved
        4. Severity assessment if it's an ALERT
        
        Keep the analysis concise but informative (2-3 sentences).
        """,
        expected_output="A concise analysis of the log message explaining its significance and potential impact",
        agent=agent
    )


def create_resolution_task(agent, log_message, timestamp, analysis):
    """
    Create a task to provide resolution steps for ALERT messages
    """
    return Task(
        description=f"""
        Based on this ALERT-level log message and analysis, provide specific resolution steps:
        
        Timestamp: {timestamp}
        Log Message: {log_message}
        Analysis: {analysis}
        
        Provide:
        1. Immediate actions to take
        2. Investigation steps
        3. Potential fixes or workarounds
        4. Prevention measures
        
        Keep recommendations practical and actionable (3-4 bullet points).
        """,
        expected_output="Specific, actionable resolution steps for addressing the alert",
        agent=agent
    )


def create_architecture_context_task(agent, log_message, architecture_knowledge):
    """Create a task to incorporate architecture knowledge"""
    return Task(
        description=f"""
        Using the system architecture knowledge provided, enhance the analysis of this log message:
        
        Log Message: {log_message}
        Architecture Context: {architecture_knowledge}
        
        Provide additional context about:
        1. Which system components are likely involved
        2. How this issue might affect other services
        3. Dependencies that should be checked
        4. Architecture-specific considerations
        
        Keep the context brief but valuable (2-3 sentences).
        """,
        expected_output="Architecture-aware context that enhances understanding of the log message",
        agent=agent
    )