from Bio import Entrez
import requests
from bs4 import BeautifulSoup
import json
import os
import time

# Replace with your email
Entrez.email = "yuktawalanju16gmail.com@gmail.com"


def search_pmc(query, max_results=5):
    """Search PMC Open Access articles"""
    handle = Entrez.esearch(db="pmc", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]


def get_article_text(pmc_id):
    """Fetch PMC article with full metadata parsing"""
    handle = Entrez.efetch(db="pmc", id=pmc_id, rettype="xml", retmode="text")
    xml_data = handle.read()
    soup = BeautifulSoup(xml_data, "xml")

    # Title
    title_tag = soup.find("article-title")
    title = title_tag.get_text(" ", strip=True) if title_tag else "Unknown Title"

    # Authors
    authors = []
    for contrib in soup.find_all("contrib", {"contrib-type": "author"}):
        name = contrib.find("string-name")
        if name:
            authors.append(name.get_text(strip=True))
        else:
            surname = contrib.find("surname")
            given = contrib.find("given-names")
            if surname:
                authors.append(f"{given.get_text(strip=True) if given else ''} {surname.get_text(strip=True)}".strip())

    # Journal - try multiple tag locations
    journal = "Unknown Journal"
    journal_tag = soup.find("journal-title")
    if journal_tag:
        journal = journal_tag.get_text(strip=True)
    else:
        # Try alternative
        journal_meta = soup.find("journal-meta")
        if journal_meta:
            journal_tag = journal_meta.find("journal-title")
            if journal_tag:
                journal = journal_tag.get_text(strip=True)

    # Year - try multiple locations in XML
    year = "N/A"
    # Try pub-date with pub-type
    pub_date = soup.find("pub-date", {"pub-type": "epub"}) or soup.find("pub-date", {"date-type": "pub"}) or soup.find("pub-date")
    if pub_date:
        year_tag = pub_date.find("year")
        if year_tag:
            year = year_tag.get_text(strip=True)
    # Fallback: any year tag
    if year == "N/A":
        year_tag = soup.find("year")
        if year_tag:
            year = year_tag.get_text(strip=True)

    # Body text
    body = soup.find("body")
    text = body.get_text(" ", strip=True) if body else ""

    return {
        "pmc_id": pmc_id,
        "title": title,
        "authors": authors,
        "journal": journal,
        "year": year,
        "text": text
    }


def load_pmc_articles(query="artificial intelligence healthcare", max_results=500):
    """Fetch PMC articles with rate limiting and error handling"""
    ids = search_pmc(query, max_results=max_results)
    print(f"Found {len(ids)} PMC IDs to download")

    articles = []
    failed_ids = []

    for idx, pmc_id in enumerate(ids):
        print(f"Downloading {idx+1}/{len(ids)}: PMC{pmc_id}...")

        if idx > 0:
            time.sleep(0.5)

        try:
            article = get_article_text(pmc_id)
            if article and article.get("text") and len(article["text"]) > 100:
                articles.append(article)
                print(f"  ✓ {article['title'][:50]}... | {article['journal']} ({article['year']})")
            else:
                print(f"  ✗ Empty or too short")
                failed_ids.append(pmc_id)
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:80]}")
            failed_ids.append(pmc_id)
            if "400" in str(e) or "429" in str(e):
                print("  ⏳ Rate limited. Waiting 5 seconds...")
                time.sleep(5)

    print(f"✓ Total articles loaded: {len(articles)}")
    if failed_ids:
        print(f"✗ Failed IDs ({len(failed_ids)}): {failed_ids[:10]}...")

    return articles


def save_articles(query):
    """Original function - saves to JSON file"""
    ids = search_pmc(query, max_results=10)
    articles = []

    for pmc_id in ids:
        print(f"Downloading PMC{pmc_id}")
        article = get_article_text(pmc_id)
        if article:
            articles.append(article)

    os.makedirs("data", exist_ok=True)

    with open("data/pmc_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(articles)} articles")


if __name__ == "__main__":
    save_articles("artificial intelligence healthcare")