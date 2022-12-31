import redis
from pymongo import MongoClient
import boto3
import json
import pprint


SECRET_ID_01 = 'redis'
SECRET_ID_02 = 'mongodb-website'
REGION_NAME = 'us-west-1'
# DATABASE = 'article'
DATABASE = 'redis'
# COLLECTION = 'technical'
COLLECTION = 'article'


def get_secret(secret_id: str, region_name: str) -> dict:
    session = boto3.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    secret_value = client.get_secret_value(SecretId=secret_id)
    secret_string = secret_value['SecretString']
    return json.loads(secret_string)


def main():

    # Get secrets
    secret_redis = get_secret(secret_id=SECRET_ID_01, region_name=REGION_NAME)
    host_redis = secret_redis['host']
    port_redis = secret_redis['port']
    password_redis = secret_redis['password']
    secret_mongodb = get_secret(secret_id=SECRET_ID_02, region_name=REGION_NAME)
    cluster_mongodb = secret_mongodb['mongodb-cluster']
    username_mongodb = secret_mongodb['mongodb-username']
    password_mongodb = secret_mongodb['mongodb-password']
    
    # Connect to Redis
    r = redis.Redis(
        host=host_redis,
        port=port_redis,
        password=password_redis,
        decode_responses=True
    )
    
    # Check connection
    if r.ping():
        print('Connected to redis')
    else:
        print('Connection to redis failed')
    
    keys = r.keys('article:*')
    print(keys)
    
    # Get data from Redis
    documents = []
    for key in r.keys('article:*'):
        
        # if key != 'article:':
        #     value = r.hgetall(key)
        #     if 'image' in value and 'content' not in value:
        #         documents.append(value)
    
        value = r.hgetall(key)
        documents.append(value)
                
    print(f'Number of documents: {len(documents)}')
    # pprint.pprint(documents)
    
    # MongoDB client
    host_mongodb = f'mongodb+srv://{username_mongodb}:{password_mongodb}@{cluster_mongodb}/{DATABASE}?retryWrites=true&w=majority'
    client_mongodb = MongoClient(host_mongodb)
    collection = client_mongodb[DATABASE][COLLECTION]
    
    # Upload to Mongodb
    collection.insert_many(documents, ordered=True)
    print('Uploaded to Mongodb')


if __name__ == '__main__':
    main()
