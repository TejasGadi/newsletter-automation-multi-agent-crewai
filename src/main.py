#!/usr/bin/env python
from automated_newsletter_multi_agent_crew.crew import AutomatedNewsletterMultiAgentCrew

def run():  
    inputs = {
        "topic": input("Enter the topic: "),
        'email_id': input('Enter your email ID: '),
    }
    result = AutomatedNewsletterMultiAgentCrew().crew().kickoff(inputs=inputs)
    print(f"result: {result}")

run()
