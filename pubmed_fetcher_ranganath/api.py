import requests
import xmltodict
from typing import List, Dict

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def search_pubmed(query: str, retmax: int = 20) -> List[str]:
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": retmax,
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    ids = response.json()["esearchresult"]["idlist"]
    return ids

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    data = xmltodict.parse(response.text)
    articles = data["PubmedArticleSet"].get("PubmedArticle", [])
    if isinstance(articles, dict):
        articles = [articles]
    return articles
