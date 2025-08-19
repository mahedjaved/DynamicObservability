from crewai import Crew, Process
from agents import (
    log_classifier_agent,
    log_analyzer_agent,
    resolution_advisor_agent,
    architecture_knowledge_agent
)
from tasks import (
    create_classification_task,
    create_analysis_task,
    create_resolution_task,
    create_architecture_context_task
)
import datetime


class LogAnalysisCrew:
    def __init__(self):
        self.architecture_knowledge = ""

    def update_architecture_knowledge(self, knowledge):
        """
        This updates the knowledge based on the architecture context provided.
        """
        self.architecture_knowledge = knowledge

    def process_log_message(self, log_message, timestamp=None):
        """
        Process a single log message through the crew - this is equivalent of a workflow in Langgraph. In CreweAI your typical workflow is:

        Task -> Crew -> Kickoff -> Get result
        """
        if timestamp is None:
            timestamp = datetime.datetime.now().isoformat()

        # ------------------------------------------------------- #
        # Step 1: Classify the log message
        # ------------------------------------------------------- #
        classification_task = create_classification_task(
            log_classifier_agent, log_message, timestamp)
        classification_crew = Crew(
            agents=[log_classifier_agent],
            tasks=[classification_task],
            process=Process.sequential,
            verbose=False
        )

        classification_result = classification_crew.kickoff()
        classification = classification_result.raw.strip().upper()

        # ------------------------------------------------------- #
        # Step 2: Analyse the log message
        # ------------------------------------------------------- #
        analysis_task = create_analysis_task(
            log_analyzer_agent, log_message, timestamp, classification)
        analysis_crew = Crew(
            agents=[log_analyzer_agent],
            tasks=[analysis_task],
            process=Process.sequential,
            verbose=False
        )

        analysis_result = analysis_crew.kickoff()
        analysis = analysis_result.raw.strip()

        # ------------------------------------------------------- #
        # Step 3: Get resolution for ALERTS
        # ------------------------------------------------------- #
        resolution = ""
        if classification == "ALERT":
            resolution_task = create_resolution_task(
                resolution_advisor_agent, log_message, timestamp, analysis)
            resolution_crew = Crew(
                agents=[resolution_advisor_agent],
                tasks=[resolution_task],
                process=Process.sequential,
                verbose=False
            )
            resolution_result = resolution_crew.kickoff()
            resolution = resolution_result.raw.strip()

        # ------------------------------------------------------- #
        # Step 4: Add architecture knowledge
        # ------------------------------------------------------- #
        if self.architecture_knowledge:
            context_task = create_architecture_context_task(
                architecture_knowledge_agent, log_message, self.architecture_knowledge)
            context_crew = Crew(
                agents=[architecture_knowledge_agent],
                tasks=[context_task],
                process=Process.sequential,
                verbose=False
            )

            context_result = context_crew.kickoff()
            architecture_context = context_result.raw.strip()

            # Enhance analysis with architecture context
            analysis = f"{analysis}\n\nArchitecture Context: {architecture_context}"

        return {
            "timestamp": timestamp,
            "log_message": log_message,
            "classification": classification,
            "analysis": analysis,
            "resolution": resolution
        }
