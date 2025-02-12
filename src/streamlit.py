import sys
import time
import streamlit as st
from automated_newsletter_multi_agent_crew.crew import AutomatedNewsletterMultiAgentCrew
import datetime
import re
import os

# Custom stream handler for Streamlit output
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']
        self.color_index = 0

    def write(self, data):
        # Filter out ANSI escape codes
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)
        
        # Check for agent activities and color-code them
        agents = ["researcher", "editor", "designer", "email_agent"]
        for agent in agents:
            if agent in cleaned_data.lower():
                self.color_index = (self.color_index + 1) % len(self.colors)
                cleaned_data = cleaned_data.replace(agent, f":{self.colors[self.color_index]}[{agent}]")

        # Handle task notifications
        task_match = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        if task_match:
            st.toast(":robot_face: " + task_match.group(1).strip())

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []

def run_newsletter_app():
    st.title("AI Newsletter Generation System")
    
    # About section
    with st.expander("About the Newsletter Crew"):
        st.subheader("Team Structure")
        st.markdown("""
        ### Researcher
        - Conducts in-depth research on the specified topic
        - Uses search and content retrieval tools
        
        ### Editor
        - Refines and structures the content
        - Ensures quality and coherence
        
        ### Designer
        - Creates the newsletter layout
        - Formats content for optimal presentation
        
        ### Email Agent
        - Handles email distribution
        - Manages recipient communication
        """)

    # Input form
    st.header("Newsletter Configuration")
    with st.form("newsletter_form"):
        topic = st.text_input("Newsletter Topic", placeholder="Enter the main topic for your newsletter")
        email_id = st.text_input("Email ID", placeholder="Enter your email address")
        
        submit_button = st.form_submit_button("Generate Newsletter")

    if submit_button:
        if not all([topic, email_id]):
            st.error("Please fill in all fields")
            return

        # Placeholder for stopwatch
        stopwatch_placeholder = st.empty()
        start_time = time.time()

        # Process the newsletter generation
        with st.expander("Processing Newsletter Generation", expanded=True):
            sys.stdout = StreamToExpander(st)
            with st.spinner("Generating Newsletter..."):
                crew = AutomatedNewsletterMultiAgentCrew()
                inputs = {
                    "topic": topic,
                    "email_id": email_id
                }
                result = crew.crew().kickoff(inputs=inputs)

        # Display completion time
        end_time = time.time()
        total_time = end_time - start_time
        stopwatch_placeholder.text(f"Total Time Elapsed: {total_time:.2f} seconds")

        # Display results
        st.header("Generated Newsletter")
        st.markdown(result)

        # Display output file location
        output_file = f'output_newsletter.md'
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                newsletter_content = f.read()
            st.download_button(
                label="Download Newsletter",
                data=newsletter_content,
                file_name=f"newsletter_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    run_newsletter_app()