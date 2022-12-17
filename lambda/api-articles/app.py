from pymongo import MongoClient
from bson.objectid import ObjectId
import boto3
import json
import pprint


SECRET_ID = 'mongodb-website'
REGION_NAME = 'us-west-1'
DATABASE = 'article'
COLLECTION = 'technical'


def get_secret(secret_id: str, region_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    secret_value = client.get_secret_value(SecretId=secret_id)
    secret_string = secret_value['SecretString']
    return json.loads(secret_string)


secret = get_secret(secret_id=SECRET_ID, region_name=REGION_NAME)
cluster = secret['mongodb-cluster']
username = secret['mongodb-username']
password = secret['mongodb-password']

host = f'mongodb+srv://{username}:{password}@{cluster}/{DATABASE}?retryWrites=true&w=majority'
client = MongoClient(host)
collection = client[DATABASE][COLLECTION]


def get_articles():
    body = []

    for document in collection.find({}, {'is_featured': 0, 'vote': 0, 'excerpt': 0}):
        document['id'] = str(document['_id'])
        del document['_id']
        document['view'] = int(document['view']) if 'view' in document else 0 
        document['like'] = int(document['like']) if 'like' in document else 0
        body.append(document)

    return body    


def get_article(id_: str):
    object_id = ObjectId(id_)
    document = collection.find_one(
        {'_id': object_id}, 
        {'_id': 0, 'excerpt': 0, 'is_featured': 0, 'vote': 0}
    )
    document['view'] = int(document['view']) if 'view' in document else 0 
    document['like'] = int(document['like']) if 'like' in document else 0
    return document


def handler(event, context):
    
    # Get a single article metadata by ID
    if event['queryStringParameters'] and 'id' in event['queryStringParameters']:
        body = get_article(id_=event['queryStringParameters']['id'])
        body = json.dumps(body)
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': body
        }

    # Get the metadata of all the articles
    body = get_articles()
    body = json.dumps(body)
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': body
    }


if __name__ == '__main__':
    event = {
        'queryStringParameters': {
            'id': '639ab1522ec4249ad4cecab5'
        }
    }
    # event = {
    #     'queryStringParameters': None
    # }
    pprint.pprint(handler(event, None))
