from datetime import date, datetime
from re import compile, sub
from requests import post
from xml.sax.saxutils import escape as esc


payload = '''
{
    "locale": "en-US",
    "state": "PRODUCTION",
    "from": 0,
    "size": 911,
    "sort": [
        {
            "name": "Valid_as_Of",
            "direction": "DESC"
        },
        {
            "name": "Software_Lifecycle",
            "direction": "ASC"
        },
        {
            "name": "Action",
            "direction": "DESC"
        },
        {
            "name": "Component",
            "direction": "ASC"
        },
        {
            "name": "Title",
            "direction": "ASC"
        }
    ],
    "columns": [
        {
            "name": "Component",
            "query": []
        },
        {
            "name": "Environment",
            "query": []
        },
        {
            "name": "Title",
            "query": []
        },
        {
            "name": "Description",
            "query": []
        },
        {
            "name": "Action",
            "query": []
        },
        {
            "name": "Software_Lifecycle",
            "query": []
        },
        {
            "name": "Type",
            "query": []
        },
        {
            "name": "Line_of_Business",
            "query": [],
            "tableSearch": 0
        },
        {
            "name": "Sub_Process",
            "query": [],
            "tableSearch": 0
        },
        {
            "name": "Valid_as_Of",
            "dateFrom": "1970-01-01",
            "dateTo": "2099-12-31",
            "tableSearch": 0
        },
        {
            "name": "outputloio",
            "query": [
                "922bf2dbe0b646aaaa8cb5e077cfd799",
                "b078c7aa93ed4fc391e3323b7a255b84",
                "46aded7ad9cf4faebc6cb40af8104df3"
            ],
            "tableSearch": 0
        },
        {
            "name": "deliverable.version",
            "query": [],
            "tableSearch": 0
        }
    ]
}
'''


def join(elements):
    return '\n'.join(elements)


def generate_feed():
    now = datetime.now()
    cHTML = compile('<.*?>')

    r = post('https://help.sap.com/http.svc/whatsnew', data=payload)
    build = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z').strip()
    body = join(('<?xml version="1.0" encoding="UTF-8" ?>',
                 '<rss version="2.0">',
                 '<channel>',
                 '  <title>What\'s new for SAP BTP</title>',
                 '  <description>What\'s new for SAP BTP</description>',
                 '  <link>https://help.sap.com/doc/'
                 '43b304f99a8145809c78f292bfc0bc58/Cloud/en-US/'
                 '98bf747111574187a7c76f8ced51cfeb.html</link>',
                 f'<lastBuildDate>{build} +0000</lastBuildDate>'))

    for row in r.json()['data']['results']:
        try:
            pubDate = datetime.strptime(sub(r'[^\x00-\x7F]+', '-',
                                        row['Valid_as_Of']), '%Y-%m-%d')
        except ValueError:
            continue
        if pubDate <= now:
            title = f'{esc(" & ".join(row["Component"]))}: {esc(row["Title"])}'
            description = esc(sub(cHTML, '', row['Description']))
            pubDate = pubDate.strftime('%a, %d %b %Y 00:00:00').strip()
            body += join(('  <item>',
                          f'    <title>{title}</title>',
                          f'    <description>{description}</description>',
                          f'    <pubDate>{pubDate} +0000</pubDate>',
                          '  </item>'))

    body += join(('</channel>', '</rss>'))
    return body


def main(event, context):
    return generate_feed()
