import sqlite3
import pytest
from report import summarize_repositories

def test_api_report_checks_schema_paginates_and_limits_requests():
    calls = []
    def fetch(page):
        calls.append(page)
        return ([{"name":"demo", "stargazers_count":3, "fork":False, "private":False}] if page==1 else [])
    assert summarize_repositories(fetch, max_pages=3) == {"repositories":1,"stars":3,"names":["demo"],"complete":True}
    assert calls == [1,2]
    assert summarize_repositories(lambda page: [{"name":f"r{page}","stargazers_count":1,"fork":False,"private":False}], max_pages=2)["complete"] is False
    with pytest.raises(ValueError):
        summarize_repositories(lambda page: [{"name":"x","stargazers_count":-1}], max_pages=1)
