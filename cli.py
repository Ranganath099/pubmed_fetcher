import argparse
from pubmed_fetcher_ranganath import api, filter, utils, writer
from typing import List, Dict


def process_papers(papers: List[Dict], debug: bool = False, include_all: bool = False) -> List[Dict[str, str]]:
    results = []

    for article in papers:
        citation = utils.safe_get(article, "MedlineCitation")
        article_data = utils.safe_get(citation, "Article") or {}
        pmid_obj = utils.safe_get(citation, "PMID") or {}
        pubmed_id = pmid_obj.get("#text", "N/A") if isinstance(pmid_obj, dict) else str(pmid_obj)
        title = utils.safe_get(article_data, "ArticleTitle") or "N/A"
        pub_date = utils.safe_get(citation, "Article", "Journal", "JournalIssue", "PubDate", "Year") or "N/A"

        authors = utils.safe_get(article_data, "AuthorList", "Author") or []
        if isinstance(authors, dict):
            authors = [authors]

        non_academic_authors, companies = filter.extract_non_academic_authors(authors)

        abstract = utils.safe_get(article_data, "Abstract", "AbstractText")
        if isinstance(abstract, list):
            abstract = " ".join(
                item if isinstance(item, str)
                else item.get("#text", str(item))
                for item in abstract
            )
        elif isinstance(abstract, dict):
            abstract = abstract.get("#text", str(abstract))

        email = utils.extract_email(str(abstract))

        # Filtering logic
        if not companies and not include_all:
            if debug:
                print(f"Skipping PubMed ID {pubmed_id} (no company affiliations)")
            continue

        if not companies and include_all and debug:
            print(f"(Academic-only) Including PubMed ID {pubmed_id}")

        try:
            result_row = {
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academicAuthor(s)": ", ".join(map(str, non_academic_authors)),
                "CompanyAffiliation(s)": ", ".join(map(str, companies)),
                "Corresponding Author Email": email or "N/A"
            }
            results.append(result_row)

        except Exception as e:
            print(f"\n Failed to process paper (PubmedID: {pubmed_id}): {e}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with pharma/biotech authors.")
    parser.add_argument("query", type=str, help="PubMed query string (e.g., 'cancer therapy')")
    parser.add_argument("-f", "--file", help="Output CSV filename (optional)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--include-all", action="store_true", help="Include all papers (even academic-only)")
    args = parser.parse_args()

    try:
        pubmed_ids = api.search_pubmed(args.query)
        if not pubmed_ids:
            print("No results found.")
            return

        articles = api.fetch_details(pubmed_ids)
        processed_data = process_papers(articles, debug=args.debug, include_all=args.include_all)

        if args.file:
            writer.write_csv(processed_data, args.file)
            print(f"Results written to: {args.file}")
        else:
            writer.print_csv(processed_data)

        if args.debug and processed_data:
            sample = processed_data[0]
            print("\nSample Output:")
            print(f"PubmedID: {sample['PubmedID']}")
            print(f"Title: {sample['Title']}")
            print(f"Date: {sample['Publication Date']}")
            print(f"Non-Academic Author(s): {sample['Non-academicAuthor(s)']}")
            print(f"Company Affiliation(s): {sample['CompanyAffiliation(s)']}")
            print(f"Email: {sample['Corresponding Author Email']}")


    except Exception:
        import traceback
        print("\nUnhandled Error:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
