"""
    sse.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Code for Server Sent Event test
    :copyright: © 2018 by Sungshik Jou.
    :license: BSD, see LICENSE for more details.
"""

from flask import Flask, Response
import redis

app = Flask(__name__)
channel = 'sse_channel'
r = redis.Redis(host='localhost', port=6379)


def event_stream():
    try:
        pub = r.pubsub()
        pub.subscribe(channel)
        for msg in pub.listen():
            # print("data: {0}".format(msg))
            yield u'data: {0}\n\n'.format(msg['data'])
    except Exception as e:
        print(e)


@app.route('/stream', methods=["GET"])
def send():
    response = Response(event_stream(), mimetype="text/event-stream")
    response.headers['Cache-control'] = "no-cache"
    return response


