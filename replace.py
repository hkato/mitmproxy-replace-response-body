import csv
from mitmproxy.models import decoded
from urlparse import urlparse

def start(context, argv):
    if len(argv) != 2:
        raise ValueError('Usage: mitmproxy -s "' + argv[0] + ' <csv file>"')
    context.data = {}
    with open(argv[1],"rb") as f:
        reader = csv.DictReader(f)
        for row in reader:
            context.data[row["from"]] = row["to"]

def response(context, flow):
    url = urlparse(flow.request.pretty_url)
    url_without_query = url.scheme + "://" + url.netloc + url.path
    if url_without_query in context.data:
        with decoded(flow.response):
            with open(context.data[url_without_query], "r") as file:
                flow.response.content = file.read()
