import os, json
from datetime import datetime, timezone
from typing import List
import requests

MAIN_USER = os.environ.get("MAIN_USER", "pinkycollie")
ORG_LIST = os.environ.get("ORG_LIST", "")
OFFICIAL_ORG = os.environ.get("OFFICIAL_ORG", "your-official-org")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
API_URL = "https://api.github.com"
HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"

def get_repositories(user_or_org: str, entity_type: str = "user") -> List[dict]:
    repos = []
    url_type = "users" if entity_type == "user" else "orgs"
    page = 1
    while True:
        url = f"{API_URL}/{url_type}/{user_or_org}/repos?type=all&per_page=100&page={page}"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch: break
        repos += batch
        page += 1
    return repos

def get_latest_commit(o, r):
    res = requests.get(f"{API_URL}/repos/{o}/{r}/commits?per_page=1", headers=HEADERS)
    if res.status_code == 200 and res.json():
        d = res.json()[0]
        return {"sha": d["sha"], "date": d["commit"]["committer"]["date"], "message": d["commit"]["message"]}
    return None

def get_latest_release(o, r):
    res = requests.get(f"{API_URL}/repos/{o}/{r}/releases/latest", headers=HEADERS)
    if res.status_code == 200:
        d = res.json()
        return {"tag": d["tag_name"], "published_at": d["published_at"], "url": d["html_url"]}
    return None

def get_open_issues(o, r):
    res = requests.get(f"{API_URL}/repos/{o}/{r}", headers=HEADERS)
    if res.status_code == 200:
        j = res.json()
        return j.get("open_issues_count", 0)
    return 0

def get_open_pull_requests(o, r):
    res = requests.get(f"{API_URL}/repos/{o}/{r}/pulls?per_page=1&state=open", headers=HEADERS)
    if 'Link' in res.headers:
        import re
        m = re.search(r'&page=(\d+)>;\s*rel="last"', res.headers['Link'])
        if m:
            return int(m.group(1))
    if res.status_code == 200:
        return len(res.json())
    return 0

def classify_repo(repo, official_org):
    owner = repo['owner']['login']
    if owner.lower() == official_org.lower():
        return "official"
    if repo.get("fork"):
        return "fork"
    return "personal"

def collect_updates():
    updates = []
    seen = set()
    orgs = [s.strip() for s in ORG_LIST.split(",") if s.strip()]
    all_entities = [("user", MAIN_USER)] + [("org", org) for org in orgs]

    for entity_type, entity in all_entities:
        for repo in get_repositories(entity, entity_type):
            full = repo["full_name"]
            if full in seen: continue
            seen.add(full)
            status = classify_repo(repo, OFFICIAL_ORG)
            info = {
                "repo": full,
                "url": repo['html_url'],
                "description": repo.get("description", ""),
                "updated_at": repo.get("updated_at"),
                "open_issues": get_open_issues(repo["owner"]["login"], repo["name"]),
                "open_prs": get_open_pull_requests(repo["owner"]["login"], repo["name"]),
                "latest_commit": get_latest_commit(repo["owner"]["login"], repo["name"]),
                "latest_release": get_latest_release(repo["owner"]["login"], repo["name"]),
                "private": repo.get("private", False),
                "owner": repo["owner"]["login"],
                "org": entity if entity_type == "org" else None,
                "status": status,
            }
            updates.append(info)
    return updates

def write_json(updates):
    os.makedirs("site", exist_ok=True)
    with open("site/updates.json", "w") as f:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(), "repos": updates}, f, indent=2)

def render_site(updates):
    from jinja2 import Template

    tmpl = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Platform-wide Project Updates</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body{font:1.1em sans-serif;max-width:46em;margin:auto;background:#fff;color:#181818;}
    a{color:#174fec}
    h1{margin-top:2em;}
    .official { font-weight:bold; background: #eeffdf; border-left: 5px solid #3ca406; padding: 2px 6px; border-radius: 4px; }
    .private { color: #888; font-style: italic }
    .repo-list { list-style: none; padding:0; }
    .repo-list > li { margin-bottom:1.2em; }
    .skip-link { position: absolute; left: -999px; }
    .skip-link:focus { left: 1em; background:#ffe; border:1px solid #888; }
  </style>
</head>
<body>
<a href="#content" class="skip-link">Skip to content</a>
<main id="content" aria-label="main">
<h1>Recent Platform-wide Project Updates</h1>
<p>Generated: {{ now }} UTC</p>
<ul class="repo-list">
{% for upd in updates %}
  <li>
    <a href="{{ upd.url }}">
      {{ upd.repo }}
      {% if upd.status == "official" %}
        <span class='official' title="Official organization repo">Official</span>
      {% endif %}
      {% if upd.private %}<span class='private'>private</span>{% endif %}
    </a>
    <br>
    <span>{{ upd.description }}</span>
    <ul>
      {% if upd.latest_release %}
        <li><strong>Latest Release:</strong> <a href="{{ upd.latest_release.url }}">{{ upd.latest_release.tag }}</a> ({{ upd.latest_release.published_at[:10] }})</li>
      {% endif %}
      {% if upd.latest_commit %}
        <li><strong>Latest Commit:</strong> {{ upd.latest_commit.date[:10] }} - <code>{{ upd.latest_commit.message.split("\\n")[0][:60] }}</code></li>
      {% endif %}
      <li><strong>Open Issues:</strong> {{ upd.open_issues }} | <strong>Open PRs:</strong> {{ upd.open_prs }}</li>
    </ul>
  </li>
{% endfor %}
</ul>
<p><small>(c) pinkycollie — <a href="updates.json">JSON Feed</a></small></p>
</main>
</body>
</html>
""")
    html = tmpl.render(updates=updates, now=datetime.now(timezone.utc).isoformat())
    with open("site/index.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    updates = collect_updates()
    write_json(updates)
    render_site(updates)

if __name__ == "__main__":
    main()
