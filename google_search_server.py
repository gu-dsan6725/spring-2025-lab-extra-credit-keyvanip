"""
Google Search MCP Server

This server allows Claude to perform Google searches and fetch webpage content.
"""

from mcp.server.fastmcp import FastMCP
from mcp import tool
from googlesearch import search
from bs4 import BeautifulSoup
import requests

# Initialize the FastMCP server
mcp = FastMCP("google_search_tool")

@tool()
def google_search(query: str, num_results: int = 1) -> str:
    """
    Performs a Google search and returns the text from the top result.

    Args:
        query (str): The search query string.
        num_results (int): Number of results to fetch (default: 1).

    Returns:
        str: Text content of the first search result's page.
    """
    try:
        search_results = list(search(query, num_results=num_results))
        if not search_results:
            return "No search results found."

        url = search_results[0]
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator="\n", strip=True)
        return f"Top URL: {url}\n\nPage Content:\n{text[:1000]}..."  # Limit to 1000 chars

    except Exception as e:
        return f"Error during Google search: {str(e)}"

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()