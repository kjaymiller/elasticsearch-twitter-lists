import typer
import tweepy
import os
import elasticsearch
import elasticsearch.helpers
import pendulum

auth = tweepy.OAuthHandler(
        os.environ.get('TWITTER_ACCESS_KEY', None),
        os.environ.get('TWITTER_SECRET_KEY', None),
        )
api = tweepy.API(auth)
client = elasticsearch.Elasticsearch(hosts=[os.environ.get('ES_HOST', 'localhost')])
app = typer.Typer()


def get_data(**kwargs):
    """Iterate through the a tweepy Cursor and modify data for elasticsearch"""

    for tweet in tweepy.Cursor(api.list_timeline, **kwargs).items():
        json_data = tweet._json
        json_data['_id'] = json_data['id_str']
        json_data['created_at'] = str(pendulum.parse(json_data['created_at'], strict=False))
        yield json_data


def bulk_add(**kwargs)
    elasticsearch.helpers.bulk(client=client, index=index, actions=get_data(list_id=list_id, **kwargs))


@app.command()
def init(
        *,
        list_id: int,
        es_index: str,
        include_rts: bool=False,
        include_entities: bool=False,
        ):
    """Create a new index for a Twitter List"""
    kwargs={
        "list_id": list_id,
        "include_rts": include_rts,
        "include_entities"include_entities,
        }
    bulk_add(**kwargs)

def get_latest_tweet(es_index):
    q = {
          "size": 1
          , "sort": [
            {
              "created_at": {
                "order": "desc"
              }
            }
          ]
        }
    latest_tweet_id = client.search(index=index, body=q)['hits']['hits'][0]['_id']
    return latest_tweet_id


def update(
        list_id:int,
        es_index:str,
        since_id: int=0,
        max_id: int=0,
        include_rts: bool=False,
        include_entities: bool=False,
        ):
    """Update an existing_index for a Twitter list from the (optional) since_id to the (optional) max_id. If no since_id is provided, then use latest object in es_index"""

    if not since_id:
        since_id = get_latest_tweet(es_index)

    typer.echo(f"fetching results from {last_tweet}")
    bulk_add(**kwargs)

if __name__ == '__main__':
    app()
