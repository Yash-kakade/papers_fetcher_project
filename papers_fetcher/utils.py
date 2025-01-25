import pandas as pd
from typing import List, Dict


def save_to_csv(papers: List[Dict], filename: str) -> None:
    """Save papers data to a CSV file."""
    data = [
        {
            "PubmedID": paper.get("uid"),
            "Title": paper.get("title"),
            "Publication Date": paper.get("pubdate"),
            "Non-academic Author(s)": "; ".join(
                [aff for aff in paper.get("affiliations", []) if "Inc." in aff or "Pharma" in aff]
            ),
            "Company Affiliation(s)": "; ".join(
                [aff for aff in paper.get("affiliations", []) if "Inc." in aff or "Pharma" in aff]
            ),
            "Corresponding Author Email": paper.get("email", "N/A"),
        }
        for paper in papers
    ]
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
