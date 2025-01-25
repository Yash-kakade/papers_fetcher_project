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
from papers_fetcher.api_client import PubMedAPIClient
from papers_fetcher.data_processor import PaperDataProcessor
from papers_fetcher.utils import save_to_csv

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


def main():
    # Set up argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Fetch and process papers from PubMed.")
    
    # Add query argument (this is required)
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    
    # Add -f or --file argument to specify the output file (optional)
    parser.add_argument("-f", "--file", type=str, help="Output CSV file. If not provided, output is printed to console.")
    
    # Add -d or --debug argument to enable debug mode (optional)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode to print intermediate results.")
    
    # Parse the arguments
    args = parser.parse_args()

    # Initialize the API client with your API key
    client = PubMedAPIClient(api_key="34310e494ae7e833ac59e26c800d84072708")
    
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

        # If no papers remain after filtering, print a message and exit
        if not filtered_papers:
            print("No papers remain after filtering. Exiting.")
            return

        # Save filtered papers to CSV if --file is specified, otherwise print to console
        if args.file:
            save_to_csv(filtered_papers, args.file)
        else:
            # Print the papers to the console
            for paper in filtered_papers:
                print(paper)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
