from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from typing import List


@CrewBase
class LinkedinProfileFinder():
    """LinkedinProfileFinder crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    
    @agent
    def linkedin_profile_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_profile_finder'], # type: ignore[index]
            tools=[SerperDevTool()],
            inject_date=True,  # Automatically inject current date into tasks
            date_format="%B %d, %Y",  # Format as "June 12, 2025"
        )
    @task
    def linkedin_profile_finder_task(self) -> Task:
        return Task(
            config=self.tasks_config['linkedin_profile_finder_task'], # type: ignore[index]
            inject_date=True,  # Automatically inject current date into tasks
            date_format="%B %d, %Y",  # Format as "June 12, 2025"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LinkedinProfileFinder crew"""
        
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
