from datetime import date, datetime
from re import compile, sub
from requests import post
from xml.sax.saxutils import escape as esc


form = {
    "draw": "1",
    "columns[0][data]": "Component",
    "columns[0][name]": "Component",
    "columns[0][searchable]": "true",
    "columns[0][orderable]": "true",
    "columns[0][search][regex]": "false",
    "columns[1][data]": "Capability",
    "columns[1][name]": "Capability",
    "columns[1][searchable]": "false",
    "columns[1][orderable]": "false",
    "columns[1][search][regex]": "false",
    "columns[2][data]": "Environment",
    "columns[2][name]": "Environment",
    "columns[2][searchable]": "true",
    "columns[2][orderable]": "true",
    "columns[2][search][regex]": "false",
    "columns[3][data]": "Title",
    "columns[3][name]": "Title",
    "columns[3][searchable]": "true",
    "columns[3][orderable]": "true",
    "columns[3][search][regex]": "false",
    "columns[4][data]": "Description",
    "columns[4][name]": "Description",
    "columns[4][searchable]": "true",
    "columns[4][orderable]": "true",
    "columns[4][search][regex]": "false",
    "columns[5][data]": "Action",
    "columns[5][name]": "Action",
    "columns[5][searchable]": "true",
    "columns[5][orderable]": "true",
    "columns[5][search][regex]": "false",
    "columns[6][data]": "Type",
    "columns[6][name]": "Type",
    "columns[6][searchable]": "true",
    "columns[6][orderable]": "true",
    "columns[6][search][regex]": "false",
    "columns[7][data]": "Valid_as_Of",
    "columns[7][name]": "Valid_as_Of",
    "columns[7][searchable]": "false",
    "columns[7][orderable]": "false",
    "columns[7][search][regex]": "true",
    "order[0][column]": "7",
    "order[0][dir]": "desc",
    "order[1][column]": "0",
    "order[1][dir]": "asc",
    "order[2][column]": "3",
    "order[2][dir]": "asc",
    "start": "0",
    "length": "-1",
    "search[regex]": "false",
}


def join(elements):
    return '\n'.join(elements)


def generate_feed():
    now = datetime.now()
    cHTML = compile('<.*?>')

    r = post(('https://help.sap.com/http.svc/datatables?'
              'deliverable=43b304f99a8145809c78f292bfc0bc58&'
              'version=Cloud&language=en-US&datafile=wn.json'), data=form)
    build = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %Z').strip()
    body = join(('<?xml version="1.0" encoding="UTF-8" ?>',
                 '<rss version="2.0">',
                 '<channel>',
                 '  <title>What\'s new for SAP BTP</title>',
                 '  <link>https://help.sap.com/doc/'
                 '43b304f99a8145809c78f292bfc0bc58/Cloud/en-US/'
                 '98bf747111574187a7c76f8ced51cfeb.html</link>',
                 f'<lastBuildDate>{build}</lastBuildDate>'))

    for row in r.json()['message']['data']:
        pubDate = datetime.strptime(row['Valid_as_Of'], '%Y‑%m‑%d')
        if pubDate <= now:
            title = f'{esc(" & ".join(row["Component"]))}: {esc(row["Title"])}'
            description = esc(sub(cHTML, '', row['Description']))
            pubDate = pubDate.strftime('%a, %d %b %Y 00:00:00').strip()
            body += join(('  <item>',
                          f'    <title>{title}</title>',
                          f'    <description>{description}</description>',
                          f'    <pubDate>{pubDate}</pubDate>',
                          '  </item>'))

    body += join(('</channel>', '</rss>'))
    return body


def main(event, context):
    return generate_feed()
