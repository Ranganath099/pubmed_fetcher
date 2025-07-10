# PubMed Fetcher

**PubMed Fetcher** is a command-line Python tool that retrieves research papers from PubMed based on a user-defined query. It filters results to include only articles with at least one author affiliated with a pharmaceutical or biotech company, and saves the data as a CSV file.

## 🔍 Features

- Query PubMed using full-text search.
- Filter papers based on pharmaceutical/biotech company affiliations.
- Output results to a CSV file.
- Safe handling of missing fields and malformed entries.
- CLI interface with multiple options.

## 📦 Installation

```bash
git clone https://github.com/Ranganath099/pubmed_fetcher.git
cd pubmed_fetcher
pip install .
🚀 Usage

python cli.py --query "cancer immunotherapy" --output results.csv
Optional arguments:
Argument	Description
--query	The PubMed search query
--output	Path to save the CSV file (default: output.csv)
--all	Include all papers regardless of affiliation
--debug	Print debug information

🗂️ Project Structure


pubmed_fetcher_ranganath/
├── __init__.py
├── api.py          # PubMed API fetching logic
├── filter.py       # Filters for pharma/biotech affiliations
├── utils.py        # Utility functions for safe field access
├── writer.py       # CSV writing logic
cli.py              # Command-line entry point
pyproject.toml      # Build configuration
.gitignore
README.md
📄 Example Output
CSV columns include:

Title

Journal

Authors

Affiliations

Abstract

Publication Date

DOI

PMID

🧪 Development
To run the code locally:


python cli.py --query: poetry run get-papers-list "lung cancer AND immunotherapy" -f output.csv -d
📃 License
MIT License. See LICENSE for details.

Author: B. Sri Ranganath
GitHub: @Ranganath099
