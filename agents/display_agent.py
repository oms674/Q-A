import logging

class DisplayAgent:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    async def format_results(self, results):
        if results:
            logging.info("✅ Results successfully formatted for display.")
            return f"📋 Results: {results}"
        else:
            logging.warning("⚠️ No results found to display.")
            return "❌ No results found."
