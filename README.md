# Elastic Twitter Lists
## Visualize Twitter lists Data via kibana

![Kibana Tweets Visualization](https://ik.imagekit.io/cxazzw3yew/twitter-data-kibana.png?tr=w-650)

## Requirements 

* Python 3.8
* pendulum (for converting twitter datetime)
* elasticsearch (for storing data)
* typer (for cli options and things)

### Other Requirements

* Twitter Developer Account and SECRET AND ACCESS KEY FOR PROJECT
  * Save as `$TWITTER_ACCESS_KEY` and `$TWITTER_SECRET_KEY` respectively

* elasticsearch and kibana instances
  * Save elasticsearch cluster host as `$ES_HOST` if not `localhost`

## Quickstart

* Get/Save/Setup [Other Requirements](#Other Requirements)
* Get your Twitter List and Index Name
* Install requirements `pip install -r requirements.txt`
* run `python es_twitter_list init <TWITTERLIST> <INDEXNAME>`

[![asciicast](https://asciinema.org/a/8lnUCpYqt9FalwB3jPvexfRHz.svg)](https://asciinema.org/a/8lnUCpYqt9FalwB3jPvexfRHz)

### To Update Data
* run `python es_twitter_list update <TWITTERLIST> <INDEXNAME>`

## Run in the background

You can save it as a cron job. Be careful of [Rate Limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits).
