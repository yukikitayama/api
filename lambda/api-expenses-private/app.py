from pymongo import MongoClient
from bson.objectid import ObjectId
import redis
import boto3
from datetime import datetime
import json
import pprint


SECRET_ID_01 = 'mongodb-website'
SECRET_ID_02 = 'redis'
REGION_NAME = 'us-west-1'
DATABASE = 'db-react'
COLLECTION = 'expense'


def get_secret(secret_id: str, region_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    content = client.get_secret_value(SecretId=secret_id)
    secret_string = content['SecretString']
    secret = json.loads(secret_string)
    return secret


# Get secrets
secret_mongodb = get_secret(secret_id=SECRET_ID_01, region_name=REGION_NAME)
cluster_mongodb = secret_mongodb['mongodb-cluster']
username_mongodb = secret_mongodb['mongodb-username']
password_mongodb = secret_mongodb['mongodb-password']

secret_redis = get_secret(secret_id=SECRET_ID_02, region_name=REGION_NAME)
host_redis = secret_redis['host']
port_redis = secret_redis['port']
password_redis = secret_redis['password']

# MongoDB client
host_mongodb = f'mongodb+srv://{username_mongodb}:{password_mongodb}@{cluster_mongodb}/{DATABASE}?retryWrites=true&w=majority'
client = MongoClient(host_mongodb)
collection = client[DATABASE][COLLECTION]

# Redis client
r = redis.Redis(
    host=host_redis,
    port=port_redis,
    password=password_redis,
    decode_responses=True
)


def add_document(event):
    
    # Get user input
    body = json.loads(event['body'])
    date = body['date']
    item = body['item']
    type_ = body['type']
    amount = float(body['amount'])
    place = body['place']
    memo = ''
    if 'memo' in body:
        memo = body['memo']
        
    # Make document for MongoDB
    document = {
        'date': date,
        'item': item,
        'type': type_,
        'amount': amount,
        'place': place,
        'memo': memo,
        'creation_time': datetime.utcnow()
    }
    
    # Upload it to MondoDB
    result = collection.insert_one(document)
    print(f'Added a new expense item with ObjectId: {result.inserted_id}')


def update_document(event):
    
    # Get user input
    body = json.loads(event['body'])
    date = body['date']
    item = body['item']
    type_ = body['type']
    amount = body['amount']
    place = body['place']
    memo = body['memo'] if 'memo' in body else ''
    object_id = ObjectId(body['id'])
    
    # Make document for MongoDB
    filter_ = { '_id': object_id }
    new_values = { 
        '$set': {
            'date': date,
            'item': item,
            'type': type_,
            'amount': amount,
            'place': place,
            'memo': memo,
            'last_modified': datetime.utcnow()
        }
    }
    
    # Upload 
    result = collection.update_one(filter_, new_values)
    print(f'update_one() result.modified_count: {result.modified_count}')


def delete_document(event):
    
    # Get user input
    body = json.loads(event['body'])
    object_id = ObjectId(body['id'])
    
    # Delete
    result = collection.delete_one({ '_id': object_id })
    print(f'delete_one() result.deleted_count: {result.deleted_count}')


def handler(event, context):
    
    method = event['httpMethod']
    
    body = 'Placeholder'
    
    # If uploading a new expense
    if method == 'POST':
        
        add_document(event)
        body = 'Added a new expense successfully'
    
    # If modifying an existing expense data in database
    elif method == 'PUT':
        
        update_document(event)
        body = f'Updated the expense data of ID: {json.loads(event["body"])["id"]}'
    
    # If deleting an existing expense
    elif method == 'DELETE':
        
        delete_document(event)
        body = f'Delete the expense data of ID: {json.loads(event["body"])["id"]}'
    
    # Invalidate cache in Redis 
    # because expense table and aggregation needs the updated expense data
    for key in r.keys('api:expenses*'):
        r.delete(key)
    print('Deleted all the cache of api:expenses*')
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(body)
    }


if __name__ == '__main__':
    # event = {}
    event = {
        'httpMethod': 'PATCH'
    }
    pprint.pprint(handler(event, None))
