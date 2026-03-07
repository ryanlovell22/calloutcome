"""
SERP analysis for CallOutcome blog keyword targets.
Uses DataForSEO SERP API to understand what currently ranks.
"""

import base64
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

LOGIN = os.environ.get("DATAFORSEO_LOGIN")
PASSWORD = os.environ.get("DATAFORSEO_PASSWORD")

if not LOGIN or not PASSWORD:
    print("ERROR: Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD env vars")
    sys.exit(1)

CREDENTIALS = base64.b64encode(f"{LOGIN}:{PASSWORD}".encode()).decode()

KEYWORDS = [
    "pay per call lead generation",
    "callrail alternatives",
    "callrail competitors",
    "best call tracking software",
]


def serp_request(keyword):
    """Fetch SERP results for a keyword via DataForSEO."""
    url = "https://api.dataforseo.com/v3/serp/google/organic/live/regular"
    payload = json.dumps([{
        "keyword": keyword,
        "location_code": 2840,  # United States
        "language_code": "en",
        "depth": 10,
    }]).encode()

    req = Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Basic {CREDENTIALS}")
    req.add_header("Content-Type", "application/json")

    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        print(f"  HTTP Error {e.code}: {e.read().decode()}")
        return None


def extract_results(data):
    """Extract top 10 organic results from DataForSEO response."""
    results = []
    if not data or "tasks" not in data:
        return results

    for task in data["tasks"]:
        if task.get("status_code") != 20000:
            continue
        for result_set in task.get("result", []):
            for item in result_set.get("items", []):
                if item.get("type") == "organic":
                    results.append({
                        "rank": item.get("rank_absolute"),
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "description": item.get("description", ""),
                    })
    return results[:10]


def main():
    all_results = {}

    for kw in KEYWORDS:
        print(f"\n{'='*60}")
        print(f"Keyword: {kw}")
        print(f"{'='*60}")

        data = serp_request(kw)
        results = extract_results(data)
        all_results[kw] = results

        if not results:
            print("  No results returned.")
            continue

        for r in results:
            print(f"  #{r['rank']}: {r['title']}")
            print(f"       {r['url']}")
            print()

    # Save raw results to JSON
    output_path = os.path.join(os.path.dirname(__file__), "serp_results_2026-03-07.json")
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
