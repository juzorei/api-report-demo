# Public repository API report demo

Fetch a public GitHub user's repositories and report non-fork repository names
and total stars. A page limit prevents an unbounded API loop. This is a demo,
not evidence of paid integration work.

```powershell
py -3 -X utf8 -m pip install -e '.[dev]'
py -3 -X utf8 -m pytest -q
py -3 -X utf8 report.py juzorei
```

Only the last command uses the network. No token is read. Each request has a
20-second timeout. Rate limits and connection errors stop the run; the script
does not silently turn a partial response into a successful complete report.
If the page budget is exhausted, the JSON field `complete` is false.

Offline tests inject page responses, validate schema handling and confirm that
pagination stops on an empty page. Repeated repository names are counted once.
This example does not implement automatic retries, caching or incremental sync.
