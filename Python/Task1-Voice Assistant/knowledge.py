
import requests
from urllib.parse import quote


def answer_question(question):
    """Answer a general-knowledge question using Wikipedia."""
    question = question.strip()

    if not question:
        return "Please ask me a question."

    headers = {
        "User-Agent": "PythonVoiceAssistant/1.0 (educational project)"
    }

    # First, search for a relevant Wikipedia article.
    try:
        search_response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "list": "search",
                "srsearch": question,
                "format": "json",
                "srlimit": 1
            },
            headers=headers,
            timeout=10
        )
        search_response.raise_for_status()

        results = search_response.json()["query"]["search"]

        if not results:
            return "I could not find a relevant answer."

        title = results[0]["title"]

        # Then retrieve its introductory summary.
        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + quote(title.replace(" ", "_"), safe="_()")
        )

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        extract = data.get("extract", "")

        if extract:
            # Keep the spoken response reasonably short.
            sentences = extract.split(". ")
            summary = ". ".join(sentences[:3]).strip()

            if not summary.endswith((".", "!", "?")):
                summary += "."

            return summary

        return "I found the topic but could not retrieve its summary."

    except (requests.RequestException, ValueError, KeyError, TypeError):
        return (
            "I could not retrieve an answer right now. "
            "Please check your internet connection and try again."
        )
