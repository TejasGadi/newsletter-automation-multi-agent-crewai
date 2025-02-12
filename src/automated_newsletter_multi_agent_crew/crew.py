from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from typing import Dict, List, Tuple, Union
from langchain_core.agents import AgentFinish
from langchain_openai import ChatOpenAI

from .tools import Search, FindSimilar, GetContents, GmailSendMessageTool

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["MODEL"] = os.getenv("MODEL")

# print(f"GmailSendMessage: {GmailSendMessageTool}")

import datetime
import json
import os

@CrewBase
class AutomatedNewsletterMultiAgentCrew:
    """NewsletterGen crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def llm(self):
        llm = "gpt-4o-mini"
        return llm

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[Search(), GetContents()],
            verbose=True,
            llm=self.llm(),
            max_iter=3
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
            verbose=True,
            tools=[Search(), GetContents()],
            llm=self.llm(),
            max_iter=3
        )

    @agent
    def designer(self) -> Agent:
        return Agent(
            config=self.agents_config["designer"],
            verbose=True,
            llm=self.llm(),
            allow_delegation=False,
            max_iter=3
        )
    
    @agent
    def email_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_agent"],
            verbose=True,
            tools=[GmailSendMessageTool()],
            llm=self.llm(),
            allow_delegation=False,
            max_iter=3
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.researcher(),
            output_file=f'logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}_research_task.md',
            max_retries=3
        )

    @task
    def edit_task(self) -> Task:
        return Task(
            config=self.tasks_config["edit_task"],
            agent=self.editor(),
            output_file=f'logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}_edit_task.md',
            max_retries=3
        )

    @task
    def newsletter_task(self) -> Task:
        return Task(
            config=self.tasks_config["newsletter_task"],
            agent=self.designer(),
            output_file=f'./output_newsletter.md',
            max_retries=3
        )

    @task
    def send_email_task(self) -> Task:
        return Task(
            config=self.tasks_config["send_email_task"],
            agent=self.email_agent(),
            max_retries=3
        )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsletterGen crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )