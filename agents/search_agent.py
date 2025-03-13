# import requests
# import os
# import json

# class SearchAgent:
#     def __init__(self):
#         self.serper_api_key = os.getenv("SERPER_API_KEY")
#         self.serper_api_url = "https://google.serper.dev/search"

#     def is_sena_query(self, query):
#         """Check if the query is related to Sena services."""
#         keywords = [
#             "sena services", "sena platform", "sena communication", "sena products", "sena", 
#             "sena solutions", "sena features", "sena technology", "sena support"
#         ]
#         return any(keyword in query.lower() for keyword in keywords)

#     def search_web(self, query):
#         """Search using Serper API for both Sena and non-Sena queries."""
#         headers = {
#             "X-API-KEY": self.serper_api_key,
#             "Content-Type": "application/json"
#         }

#         # For Sena-related queries, restrict results to 'sena.services'
#         if self.is_sena_query(query):
#             query = f"site:sena.services {query}"

#         data = json.dumps({"q": query, "location": "global", "gl": "us", "hl": "en"})

#         try:
#             response = requests.post(self.serper_api_url, headers=headers, data=data)
#             response.raise_for_status()

#             search_results = response.json().get("organic", [])
#             if not search_results:
#                 return "❌ No results found."

#             # Formatting results with clickable links and proper spacing using HTML
#             results_text = "<br>".join(
#                 [f"<b>{idx + 1}.</b> <a href='{result['link']}' target='_blank'>{result['title']}</a>" 
#                  for idx, result in enumerate(search_results[:5])]
#             )
#             return results_text
#         except Exception as e:
#             return f"❌ Error fetching search results: {str(e)}"

#     def get_results(self, query):
#         """Route query to Serper API search."""
#         return self.search_web(query)


import requests
import os
import json
from bs4 import BeautifulSoup

class SearchAgent:
    def __init__(self):
        self.serper_api_key = os.getenv("SERPER_API_KEY")
        self.serper_api_url = "https://google.serper.dev/search"

    def is_sena_query(self, query):
        """Check if the query is related to Sena services."""
        keywords = [
            "sena services", "sena platform", "sena communication", "sena products", "sena", 
            "sena solutions", "sena features", "sena technology", "sena support"
        ]
        return any(keyword in query.lower() for keyword in keywords)

    def extract_answer_from_page(self, url):
        """Scrape webpage content and return key information."""
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            content = ""

            # Collect content from <p> tags for meaningful text-based answers
            for paragraph in soup.find_all('p'):
                content += paragraph.get_text().strip() + " "

            # Return first 500 characters as a concise answer
            return content.strip()[:500] + "..." if content else "❌ No concise answer found."
        
        except Exception as e:
            return f"❌ Error extracting answer: {str(e)}"

    def search_web(self, query):
        """ Search using Serper API for non-Sena queries with snippet extraction."""
        headers = {
            "X-API-KEY": self.serper_api_key,
            "Content-Type": "application/json"
        }
        data = json.dumps({"q": query, "location": "global", "gl": "us", "hl": "en"})

        try:
            response = requests.post(self.serper_api_url, headers=headers, data=data)
            response.raise_for_status()

            search_results = response.json().get("organic", [])

            if not search_results:
                return "❌ No results found."

            # Extract concise answer from snippets (if available)
            concise_answer = ""
            for result in search_results:
                if "snippet" in result:
                    concise_answer = result["snippet"]
                    break  # Stop after first concise answer found

            # Format the results with clickable links
            results_text = "<br>".join(
                [f"<b>{idx + 1}.</b> <a href='{result['link']}' target='_blank'>{result['title']}</a>"
                for idx, result in enumerate(search_results[:5])]
            )

            # Combine concise answer with links
            final_answer = f"✅ <b>Answer:</b> {concise_answer}" if concise_answer else "❌ No concise answer found."
            return f"{final_answer}<br><br><b>🔗 Related Links:</b><br>{results_text}"
        
        except Exception as e:
            return f"❌ Error fetching search results: {str(e)}"


    def get_results(self, query):
        """Route query to Serper API search."""
        return self.search_web(query)
