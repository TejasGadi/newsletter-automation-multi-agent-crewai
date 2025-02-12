from crewai.tools import BaseTool
from exa_py import Exa
from langchain_community.tools import GmailSendMessage
from datetime import datetime, timedelta
import os
from pydantic import Field
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="../credentials.json",
)
api_resource = build_resource_service(credentials=credentials)


class Search(BaseTool):
    name: str = "Search Tool"
    description: str = (
        "Searches the web based on a search query. Results are only from the last month. Uses the Exa API."
    )

    def _run(self, search_query: str) -> str:

        one_month_ago = datetime.now() - timedelta(days=30)
        date_cutoff = one_month_ago.strftime("%Y-%m-%d")

        exa = Exa(os.getenv("EXA_API_KEY"))

        search_response = exa.search_and_contents(
            search_query,
            num_results=5,
            use_autoprompt=True,
            start_published_date=date_cutoff,
            text={"include_html_tags": False, "max_characters": 300},
        )

        return search_response


class FindSimilar(BaseTool):
    name: str = "Find Similar Tool"
    description: str = (
        "Searches for similar articles to a given article using the Exa API. Takes in a URL of the article."
    )

    def _run(self, url: str) -> str:

        one_week_ago = datetime.now() - timedelta(days=4)
        date_cutoff = one_week_ago.strftime("%Y-%m-%d")

        exa = Exa(os.getenv("EXA_API_KEY"))

        search_response = exa.find_similar(url, start_published_date=date_cutoff)

        return search_response



send_message_wrapper = GmailSendMessage(api_resource=api_resource)

class GetContents(BaseTool):
    name: str = "Get Contents Tool"
    description: str = (
        "Gets the contents of a specific article using the Exa API. Takes in the IDs of the article in a list, like this: ['https://www.cnbc.com/my-news', 'https://www.bscs.com/second']"
    )

    def _run(self, ids: str) -> str:
        exa = Exa(os.getenv("EXA_API_KEY"))
        contents_response = exa.get_contents(ids, text={"include_html_tags": False, "max_characters": 300})
        return contents_response
    

class GmailSendMessageTool(BaseTool):
    name: str = "SendGmailMessage"
    description: str = (
        "Send an email with the newsletter attached. "
        "Requires 3 inputs: topic, email_message, and email_id"
    )

    def _run(self, topic: str, email_message: str, email_id: str) -> str:
        try:
            response = send_message_wrapper._run(
                message=email_message, 
                to=email_id, 
                subject=f"Automated Newsletter on {topic}"
            )
            return response
        except Exception as e:
            return f"Failed to send email: {str(e)}"