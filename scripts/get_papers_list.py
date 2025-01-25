# import argparse
# from papers_fetcher.api_client import PubMedAPIClient
# from papers_fetcher.data_processor import PaperDataProcessor
# from papers_fetcher.utils import save_to_csv


# def main():
#     parser = argparse.ArgumentParser(description="Fetch and process papers from PubMed.")
#     parser.add_argument("query", type=str, help="Search query for PubMed.")
#     parser.add_argument("-f", "--file", type=str, default="output.csv", help="Output CSV file.")
#     parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
#     args = parser.parse_args()

#     client = PubMedAPIClient(api_key="1808ea7c5499224d1ae0e930bbccdda48209")
#     try:
#         pubmed_ids = client.fetch_papers(query=args.query)
#         if args.debug:
#             print(f"Fetched PubMed IDs: {pubmed_ids}")

#         papers = client.fetch_details(pubmed_ids)
#         if args.debug:
#             print(f"Fetched Paper Details: {papers}")

#         filtered_papers = PaperDataProcessor.filter_by_non_academic_authors(papers)
#         save_to_csv(filtered_papers, args.file)
#         print(f"Saved results to {args.file}")

#     except Exception as e:
#         print(f"Error: {e}")


# if __name__ == "__main__":
#     main()


import sys
import os
import argparse
import csv
import openai
from typing import List, Dict
import requests

# Add the parent directory (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Function to save papers to CSV
def save_to_csv(papers, file_path):
    if not papers:
        print("No data to save.")
        return

    # Assuming papers is a list of dictionaries
    keys = papers[0].keys()  # Get the headers from the first paper (dict)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(papers)
    print(f"Data successfully saved to {file_path}")


# Function to summarize paper abstract using OpenAI's GPT
def summarize_abstract(abstract: str) -> str:
    if not abstract:
        return "No abstract provided."

    openai.api_key = "your_openai_api_key_here"  # Add your OpenAI API key

    try:
        response = openai.Completion.create(
            model="gpt-4",  # You can use a different model if needed
            prompt=f"Summarize the following scientific abstract:\n\n{abstract}",
            max_tokens=150,
            temperature=0.5,
        )
        return response.choices[0].text.strip()  # Extract the summary
    except Exception as e:
        print(f"Error summarizing abstract: {e}")
        return abstract  # Return the original abstract if an error occurs


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
            chunk = pubmed_ids[i:i + chunk_size]
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


class PaperDataProcessor:
    @staticmethod
    def filter_by_non_academic_authors(papers: List[Dict]) -> List[Dict]:
        """Relaxed filter for debugging."""
        # Relax filter: Include all papers for now
        return papers


def main():
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Fetch and process papers from PubMed.")

    # Add query argument (this is required)
    parser.add_argument("query", type=str, help="Search query for PubMed.")

    # Add -f or --file argument to specify the output file (optional)
    parser.add_argument("-f", "--file", type=str,
                        help="Output CSV file. If not provided, output is printed to console.")

    # Add -s or --summarized argument to specify the summary file (optional)
    parser.add_argument("-s", "--summarized", type=str, help="Output CSV file for summarized abstracts.")

    # Add -d or --debug argument to enable debug mode (optional)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode to print intermediate results.")

    # Parse the arguments
    args = parser.parse_args()

    # Initialize the API client with your API key
    client = PubMedAPIClient(api_key="34310e494ae7e833ac59e26c800d84072708")  # Use your actual PubMed API key

    try:
        # Fetch PubMed IDs
        pubmed_ids = client.fetch_papers(query=args.query)
        if args.debug:
            print(f"Fetched PubMed IDs: {pubmed_ids}")

        if not pubmed_ids:
            print("No PubMed IDs found. Exiting.")
            return

        # Fetch paper details
        papers = client.fetch_details(pubmed_ids)
        if args.debug:
            print(f"Fetched Paper Details: {papers}")

        if not papers:
            print("No paper details fetched. Exiting.")
            return

        # Print out the raw structure of the papers (for debugging)
        if args.debug:
            print(f"Paper structure: {papers[0]}")

        # Filter papers based on non-academic authors
        print("Filtering papers by non-academic authors...")
        filtered_papers = PaperDataProcessor.filter_by_non_academic_authors(papers)

        if args.debug:
            print(f"Filtered Papers: {filtered_papers}")

        # Summarize the abstracts using GPT and store summarized data separately
        summarized_papers = []
        for paper in filtered_papers:
            abstract = paper.get("abstract", "")
            summarized_abstract = summarize_abstract(abstract)
            summarized_papers.append({
                "title": paper.get("title", ""),
                "summary": summarized_abstract
            })

        # If no papers remain after filtering, print a message and exit
        if not filtered_papers:
            print("No papers remain after filtering. Exiting.")
            return

        # Save original papers and summarized abstracts to CSV if --file and --summarized are specified
        if args.file:
            save_to_csv(filtered_papers, args.file)

        if args.summarized:
            save_to_csv(summarized_papers, args.summarized)

        # Print the summarized papers if no file is provided
        if not args.summarized:
            for paper in summarized_papers:
                print(paper)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
