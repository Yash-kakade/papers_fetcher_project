import pytest
from papers_fetcher.api_client import PubMedAPIClient


def test_fetch_papers():
    client = PubMedAPIClient(api_key="1808ea7c5499224d1ae0e930bbccdda48209")
    query = "cancer"
    papers = client.fetch_papers(query=query, retmax=5)
    assert len(papers) <= 5
