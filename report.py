"""Bounded API pagination and validated public repository summaries."""
def summarize_repositories(fetch_page, *, max_pages=10):
    if type(max_pages) is not int or max_pages <= 0:
        raise ValueError("max_pages must be a positive integer")
    repositories = {}
    complete = False
    for page in range(1, max_pages+1):
        records = fetch_page(page)
        if not isinstance(records, list):
            raise ValueError("expected a JSON array")
        if not records:
            complete = True
            break
        for record in records:
            if (not isinstance(record, dict) or not isinstance(record.get("name"), str)
                    or not record["name"].strip() or type(record.get("stargazers_count")) is not int
                    or record["stargazers_count"] < 0 or type(record.get("fork")) is not bool
                    or type(record.get("private")) is not bool):
                raise ValueError("invalid repository response")
            if not record["fork"] and not record["private"]:
                repositories[record["name"]] = record["stargazers_count"]
    return {"repositories":len(repositories), "stars":sum(repositories.values()),
            "names":sorted(repositories), "complete":complete}


if __name__ == "__main__":
    import argparse
    import json
    import re
    from urllib.request import Request, urlopen
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9-]{1,39}", args.username):
        parser.error("invalid GitHub username")
    def fetch(page):
        req = Request(f"https://api.github.com/users/{args.username}/repos?per_page=100&page={page}",
                      headers={"User-Agent":"public-repository-report-demo", "Accept":"application/vnd.github+json"})
        with urlopen(req, timeout=20) as response:
            return json.load(response)
    print(json.dumps(summarize_repositories(fetch), indent=2))
