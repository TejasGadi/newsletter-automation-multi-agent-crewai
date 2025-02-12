# Automated Newsletter Multi Agent using Crew AI 🤖

An intelligent multi-agent system that automates the entire newsletter creation and distribution process using Crew AI. The system employs multiple specialized agents working in collaboration to research, write, design, and distribute newsletters.

## 🌟 Features

- **Automated Research**: Intelligent agent that researches and gathers relevant content
- **Smart Content Editing**: Dedicated editor agent for content refinement
- **Professional Design**: Design agent for newsletter formatting and layout
- **Automated Distribution**: Email agent for handling newsletter distribution
- **Streamlit Interface**: User-friendly web interface for easy interaction
- **Real-time Progress Tracking**: Visual feedback on the newsletter generation process

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Gmail API credentials (for email distribution)
- OpenAI API key
- EXA API key (for web search capabilities)

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/TejasGadi/newsletter-automation-multi-agent-crewai.git
cd automated-newsletter-multi-agent
```

2. Set up environment variables:
Create a `.env` file in the `automated_newsletter_multi_agent_crew` directory with the following:
```env
MODEL=your_model_name
OPENAI_API_KEY=your_openai_api_key
EXA_API_KEY=your_exa_api_key
```

3. Set up Gmail API credentials for newsletter email:
- Go to Google Cloud Console and create credentials for Gmail API
- Download the credentials and save as `credentials.json` in the `src` folder. For this follow the [guide] ("https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application")
- This will be used for sending newsletters from your specified email account

4. Build and run with Docker:
```bash
docker-compose up
```

5. Access the application:
Open your browser and navigate to the below URL to access the streamlit app:
```
http://localhost:8501
```

## 💻 Usage

### Command Line Interface

Run the newsletter generation system:
```bash
python main.py
```

You will be prompted to enter:
- Newsletter topic
- Email ID for distribution

### Streamlit Interface

Access the web interface directly at `http://localhost:8501` by 
```bash
streamlit run src/streamlit.py
```

## 🔧 Configuration

### Agent Configuration
The system uses four specialized agents:

**Research Agent**
- Role: Research Specialist
- Goal: Gather comprehensive information on the newsletter topic
- Tools: Web search and content retrieval
- Tasks: Topic research and content gathering

**Editor Agent**
- Role: Content Editor
- Goal: Refine and structure the content professionally
- Tools: Content analysis and refinement
- Tasks: Content editing and organization

**Designer Agent**
- Role: Newsletter Designer
- Goal: Create an engaging newsletter layout
- Tasks: Layout design and formatting

**Email Agent**
- Role: Distribution Manager
- Goal: Handle newsletter distribution effectively
- Tools: Gmail integration
- Tasks: Newsletter distribution

### Task Workflow
The system follows a sequential workflow:

1. **Research Task**
   - Conducts thorough research on the topic
   - Gathers relevant information
   - Creates initial content draft

2. **Edit Task**
   - Refines the research content
   - Improves structure and readability
   - Ensures content quality

3. **Newsletter Task**
   - Designs the newsletter layout
   - Formats content for optimal presentation
   - Creates the final newsletter document

4. **Email Task**
   - Prepares the newsletter for distribution
   - Handles email sending
   - Manages recipient communication


## 📁 Project Structure

```
src/
├── __pycache__/
├── automated_newsletter_multi_agent_crew/
│   ├── __pycache__/
│   ├── config/
│   │   ├── agents.yaml      # Agent configurations
│   │   ├── tasks.yaml       # Task configurations
│   ├── __init__.py
│   ├── .env                 # Environment variables
│   ├── crew.py             # Main crew implementation
│   ├── tools.py            # Custom tools and utilities
├── logs/                    # Operation logs
├── credentials.json         # Gmail API credentials
├── main.py                 # CLI entry point
├── output_newsletter.md     # Generated newsletter
├── streamlit_app.py        # Web interface
├── tests/                  # Test suite
├── .gitignore
├── pyproject.toml          # Project metadata and dependencies
├── README.md
```