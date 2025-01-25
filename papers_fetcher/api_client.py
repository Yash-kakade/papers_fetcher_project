from typing import List, Dict
import requests

class PubMedAPIClient:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_papers(self, query: str, retmax: int = 20) -> List[str]:
        """Fetch a list of PubMed IDs based on the query."""
        url = f"{self.BASE_URL}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": retmax,
            "api_key": self.api_key,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("esearchresult", {}).get("idlist", [])

    def fetch_details(self, pubmed_ids: List[str], chunk_size: int = 5) -> List[Dict]:
        """Fetch details for a list of PubMed IDs in chunks."""
        url = f"{self.BASE_URL}esummary.fcgi"
        details = []
        
        # Split IDs into chunks
        for i in range(0, len(pubmed_ids), chunk_size):
            chunk = pubmed_ids[i:i+chunk_size]
            params = {
                "db": "pubmed",
                "id": ",".join(chunk),
                "retmode": "json",
                "api_key": self.api_key,
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            result = response.json().get("result", {})
            details.extend([result[pid] for pid in chunk if pid in result])
        
        return details
