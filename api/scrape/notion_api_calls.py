import requests
from datetime import datetime, timezone

NOTION_TOKEN = "secret_ziqnCdezB6z0TfvezDEjeQCKzx3jnKmzGggdEqqpP1S"
DATABASE_ID = "a827bd8f8ed7448a943d0dbbf14b8aad"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    
    data = response.json()
    
    # Comment this out to dump all data to a file
    import json
    with open('db.json', 'w', encoding='utf8') as f:
       json.dump(data, f, ensure_ascii=False, indent=4)
       
    results = data["results"]
    return results

pages = get_pages()

for page in pages:
    page_id = ["id"]
    props = page["properties"]
    url = props["URL"]["title"][0]["text"]["content"] if props["URL"]["title"] else None
    title = props["Title"]["rich_text"][0]["text"]["content"] if props["Title"]["rich_text"] else None
    
    if props["Published"]["date"]:
        published = props["Published"]["date"]["start"]
        published = datetime.fromisoformat(published)
    else:
        published = None
    
    print(url, title, published)


def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res

url_name = "GGG444"
title_name = "FTW"
published_date = datetime.now().astimezone(timezone.utc).isoformat()
data = {
    "URL": {"title": [{"text": {"content": url_name}}]},
    "Title": {"rich_text": [{"text": {"content": title_name}}]},
    "Published": {"date": {"start": published_date, "end": None}}
}

create_page(data)