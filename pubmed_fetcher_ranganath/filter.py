from typing import List, Tuple

ACADEMIC_KEYWORDS = [
    "university", "institute", "college", "hospital", "school",
    "department", "centre", "center", "faculty", "clinic"
]

COMPANY_KEYWORDS = [
    "pharma", "biotech", "inc", "corp", "ltd", "llc", "gmbh", "solutions",
    "therapeutics", "research", "labs", "laboratories", "diagnostics"
]

def is_non_academic(affiliation: str) -> bool:
    affiliation = affiliation.lower()
    return not any(keyword in affiliation for keyword in ACADEMIC_KEYWORDS)

def extract_non_academic_authors(authors: List[dict]) -> Tuple[List[str], List[str]]:
    non_academic_authors = []
    companies = set()

    for author in authors:
        if not isinstance(author, dict):
            continue

        affiliation_info = author.get("AffiliationInfo")
        if not affiliation_info:
            continue

        if isinstance(affiliation_info, list):
            affiliations = [a.get("Affiliation", "") for a in affiliation_info if isinstance(a, dict)]
        else:
            affiliations = [affiliation_info.get("Affiliation", "")]

        for aff in affiliations:
            if aff and is_non_academic(aff):
                lastname = author.get("LastName", "").strip()
                forename = author.get("ForeName", "").strip()
                name = f"{forename} {lastname}".strip()
                if name:
                    non_academic_authors.append(name)

                for keyword in COMPANY_KEYWORDS:
                    if keyword.lower() in aff.lower():
                        companies.add(str(aff).strip())
                        break

    return non_academic_authors, list(companies)
