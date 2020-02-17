try:
    import unzip_requirements
except ImportError:
    pass
import json


def ping(event, context):
    body = {
        "ping": "pong"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
