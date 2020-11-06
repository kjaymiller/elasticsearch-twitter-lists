import tweepy
import os
import pathlib
import elasticsearch
import elasticsearch.helpers
import pendulum

auth = tweepy.OAuthHandler(
        os.environ['TWITTER_ACCESS_KEY'],
        os.environ['TWITTER_SECRET_KEY'],
        )
api = tweepy.API(auth)
elasticsearch_auth = (
        'elastic',
        os.environ['ELASTIC_PASSWORD'],
        )
client = elasticsearch.Elasticsearch(
        hosts=['localhost'],
        http_auth=elasticsearch_auth,
        )

def latest_tweet(index='dei-groups-tweets'):
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


def get_data(list_id, last_tweet):
    for tweet in tweepy.Cursor(api.list_timeline, list_id=list_id, include_rts=False, since_id=last_tweet, include_entities=False).items():
        json_data = tweet._json
        json_data['_id'] = json_data['id_str']
        json_data['created_at'] = str(pendulum.parse(json_data['created_at'], strict=False))

        yield json_data

def main(list_id=1324740237013078016, index='dei-groups-tweets', last_tweet=latest_tweet()):

    print(last_tweet)
    elasticsearch.helpers.bulk(client=client, index=index, actions=get_data(list_id=list_id, last_tweet=last_tweet))

if __name__ == '__main__':
    main()
