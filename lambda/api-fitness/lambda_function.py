from pymongo import MongoClient
import certifi
import boto3
import json
import pprint


SECRET_ID = 'mongodb-website'
REGION_NAME = 'us-west-1'
DATABASE = 'fitbit'
WEIGHT_GUESS = 57


def get_secret(secret_id: str, region_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    content = client.get_secret_value(SecretId=secret_id)
    secret_string = content['SecretString']
    secret = json.loads(secret_string)
    return secret


# Get secrets
secret_mongodb = get_secret(secret_id=SECRET_ID, region_name=REGION_NAME)
cluster = secret_mongodb['mongodb-cluster']
username = secret_mongodb['mongodb-username']
password = secret_mongodb['mongodb-password']

# MongoDB client
host = f'mongodb+srv://{username}:{password}@{cluster}/{DATABASE}?retryWrites=true&w=majority'
client = MongoClient(host)
db = client[DATABASE]


def get_calories(start, end):
    collection = db['activity-calories']
    filter_ = { 'date': { '$gte': start, '$lte': end } }
    projection = { 'activities-calories': 1 }
    body = []
    for calorie in collection.find(filter_, projection):
        index = calorie['activities-calories'][0]['dateTime']
        value = int(calorie['activities-calories'][0]['value'])
        body.append({
            'index': index,
            'value': value
        })
    return body


def get_steps(start, end):
    collection = db['activity-steps']
    filter_ = { 'date': { '$gte': start, '$lte': end } }
    projection = { 'activities-steps': 1 }
    body = []
    for step in collection.find(filter_, projection):
        index = step['activities-steps'][0]['dateTime']
        value = int(step['activities-steps'][0]['value'])
        
        # When recoding of steps was not successful, 0 steps is saved
        # but it's impossible, so set a missing value
        if value == 0:
            value = None
        
        body.append({
            'index': index,
            'value': value
        })
    return body


def get_weight(start, end):
    collection = db['weight-log']
    filter_ = { 'date': { '$gte': start, '$lte': end } }
    projection = { 'date': 1, 'weight': 1 }
    body = []
    
    # When the first weight is None, set a guess
    value = WEIGHT_GUESS
    for weight in collection.find(filter_, projection):
        pprint.pprint(weight)
        index = weight['date']
    
        # When not measuring weight, weight['weight'] has an empty list
        # weight['weight'] always contain list of objects.
        # When measuring once per day, the length of the list is one
        # When measuring multiple times on the same date, 
        # weight['weight'][0] has the first measumeant, and [1] has the second, and so on.
        # If current weight is None and previous weight is available, use previous weight as current weight
        value = weight['weight'][0]['weight'] if weight['weight'] else value
        body.append({
            'index': index,
            'value': value
        })
    return body


def get_sleep(start, end):
    collection = db['sleep-log']
    filter_ = { 'date': { '$gte': start, '$lte': end } }
    projection = { 'date': 1, 'summary': 1 }
    body = []
    for sleep in collection.find(filter_, projection):
        index = sleep['date']
        
        # When sleep was not recorded successfully, it contains 0
        # But 0 minutes sleep is impossible, so assign a missing value
        value = None if sleep['summary']['totalMinutesAsleep'] == 0 else sleep['summary']['totalMinutesAsleep']
        body.append({
            'index': index,
            'value': value
        })
    return body


def get_deep_sleep(start, end):
    collection = db['sleep-log']
    filter_ = { 'date': { '$gte': start, '$lte': end } }
    projection = { 'date': 1, 'summary': 1 }
    body = []
    for sleep in collection.find(filter_, projection):
        index = sleep['date']
        
        # When sleep was not successfully recorded by fitbit device
        # or when sleep was too short to have different sleep stages
        # 'summary' doesn't have 'states' dictionary
        # In that case, return a missing value
        deep_percent = None
        if 'stages' in sleep['summary']:
            total_time_in_bed = sleep['summary']['totalTimeInBed']
            deep = sleep['summary']['stages']['deep']
            deep_percent = round(deep / total_time_in_bed, 2)

        body.append({
            'index': index,
            'value': deep_percent
        })
        
    return body


def lambda_handler(event, context):
    
    # Get parameters
    data = event['queryStringParameters']['data']
    start = event['queryStringParameters']['start']
    end = event['queryStringParameters']['end']
    
    body = []
    
    if data == 'calories':
        body = get_calories(start, end)
    
    elif data == 'steps':
        body = get_steps(start, end)
    
    elif data == 'weight':
        body = get_weight(start, end)
    
    elif data == 'sleep':
        body = get_sleep(start, end)
    
    elif data == 'deep-sleep':
        body = get_deep_sleep(start, end)
    
    body = json.dumps(body)

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': body
    }


if __name__ == '__main__':
    event = {
        'queryStringParameters': {
            'data': 'calories',
            'start': '2022-11-01',
            'end': '2022-12-01'
        }
    }
    event = {
        'queryStringParameters': {
            'data': 'steps',
            'start': '2022-11-01',
            'end': '2022-12-01'
        }
    }
    # event = {
    #     'queryStringParameters': {
    #         'data': 'weight',
    #         'start': '2022-11-01',
    #         'end': '2022-12-01'
    #     }
    # }
    # event = {
    #     'queryStringParameters': {
    #         'data': 'sleep',
    #         'start': '2022-11-01',
    #         'end': '2022-12-01'
    #     }
    # }
    # event = {
    #     'queryStringParameters': {
    #         'data': 'deep-sleep',
    #         'start': '2022-11-01',
    #         'end': '2022-12-01'
    #     }
    # }
    pprint.pprint(lambda_handler(event, ''))
