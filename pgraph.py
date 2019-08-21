import os
from string import Template

from addict import Dict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from jinja2 import Template

url = "https://api.github.com/graphql"


api_token = os.environ["TOKEN"]

_transport = RequestsHTTPTransport(
    url=url,
    use_json=True,
    headers={
        "Authorization": "token %s" % api_token,
        "Accept": "application/vnd.github.vixen-preview+json",
    },
)

client = Client(transport=_transport, fetch_schema_from_transport=True)


def query(name, **kwargs):
    queries = {}
    for filename in os.listdir("query"):
        with open(f"query/{filename}") as query_file:
            queries[filename.split(".")[0]] = query_file.read()
    query_template = Template(queries[name])
    full_query = query_template.render(**kwargs)
    query = gql(full_query)
    return Dict(client.execute(query))
