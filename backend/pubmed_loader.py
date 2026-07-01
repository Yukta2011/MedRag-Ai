from Bio import Entrez
import json
import os

Entrez.email = "yuktawalanju16gmail.com@gmail.com"


def search_pubmed(query, max_results=10):
    """Search PubMed abstracts"""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]


def get_pubmed_abstract(pmid):
    """Fetch PubMed abstract"""
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
    return handle.read()


def load_pubmed_abstracts(query="artificial intelligence healthcare", max_results=50):
    """Load PubMed abstracts"""
    ids = search_pubmed(query, max_results=max_results)
    abstracts = []

    for pmid in ids:
        try:
            abstract = get_pubmed_abstract(pmid)
            if abstract and len(abstract) > 50:
                abstracts.append({
                    "pmid": pmid,
                    "text": abstract,
                    "title": f"PubMed:{pmid}",
                    "authors": [],
                    "journal": "PubMed",
                    "year": "N/A"
                })
        except Exception as e:
            print(f"Error fetching PubMed {pmid}: {e}")

    return abstracts


if __name__ == "__main__":
    abstracts = load_pubmed_abstracts()
    print(f"Loaded {len(abstracts)} PubMed abstracts")
    