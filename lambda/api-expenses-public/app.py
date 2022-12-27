from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
import pandas as pd
import boto3
from datetime import datetime
import json
import pprint


SECRET_ID = 'mongodb-website'
REGION_NAME = 'us-west-1'
DATABASE = 'db-react'
COLLECTION = 'expense'
CATEGORY_NUM = 7


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
collection = client[DATABASE][COLLECTION]


def get_single_expense(id_):
    expense = collection.find_one({'_id': ObjectId(id_)})
    expense = json.loads(json_util.dumps(expense))
    expense['id'] = expense['_id']['$oid']
    del expense['_id']
    # Webapp side doesn't need creation time
    del expense['creation_time']
    return expense


def get_all_expenses():
    expenses = []
    # Sort data by descending date order
    # because I wanna show the recent expense to the top in webapp
    for expense in collection.find().sort('date', -1):
        # Use json_util for BSON ID
        expense = json.loads(json_util.dumps(expense))
        expense['id'] = expense['_id']['$oid']
        del expense['_id']
        # Webapp side doesn't need creation time
        del expense['creation_time']
        expenses.append(expense)
    return expenses


def get_daily_expenses(start, end):
    dt_start = datetime.strptime(start, '%Y-%m-%d')
    dt_end = datetime.strptime(end, '%Y-%m-%d')
    
    pipeline = [
        # Convert date string to datetime
        { '$addFields': { 'convertedDate': { '$toDate': '$date' } } },
        # Filter documents by start date and end date
        { '$match': { 'convertedDate': { '$gte': dt_start, '$lte': dt_end } } },
        # Calculate daily total
        { '$group': {
            '_id': {
                'date': { '$dateToString': { 'format': '%Y-%m-%d', 'date': '$convertedDate' } }
            },
            'value': { '$sum': '$amount' }
        } },
        # Sort by calendar
        { '$sort': { '_id.date': 1 } }
    ]
    
    # Make a list of date strings because the above query doesn't give us 
    # a value for a date when no expense happened, but I want API to
    # return daily amount 0 for such a date
    dates = [d.strftime('%Y-%m-%d') for d in pd.date_range(start=start, end=end, freq='D')]
    i = 0
    
    expenses = []
    for expense in collection.aggregate(pipeline):
        index = expense['_id']['date']
        value = round(expense['value'], 2)

        if index == dates[i]:
            expenses.append({
                'index': index,
                'value': value
            })

        else:
            # Keep adding daily expense 0 while MongoDB didn't give us a date without daily sum
            while index != dates[i]:
                expenses.append({
                    'index': dates[i],
                    'value': 0
                })
                i += 1
            
            # After imputing missing daily sum, append current daily sum
            expenses.append({
                'index': index,
                'value': value
            })

        # Iterate to the next index
        i += 1
    
    # Here index contains the final date value from MongoDB
    # Keep adding daily expense 0 when the final data in MongoDB is 
    # less than the end date parameter
    if index != dates[-1]:
        while i < len(dates):
            expenses.append({
                'index': dates[i],
                'value': 0
            })
            i += 1

    return expenses


def get_monthly_expenses(start, end):
    dt_start = datetime.strptime(start, '%Y-%m-%d')
    dt_end = datetime.strptime(end, '%Y-%m-%d')

    pipeline = [
        # Convert date string to datetime
        { '$addFields': { 'convertedDate': { '$toDate': '$date' } } },
        # Filter documents by start date and end date
        { '$match': { 'convertedDate': {'$gte': dt_start, '$lte': dt_end} } },
        # Calculate monthly total
        { '$group': {
            '_id': { 
                'year': { '$year': '$convertedDate' },
                'month': { '$month': '$convertedDate' }
            },
            'value': { '$sum': '$amount' }
        } },
        # Sort by calendar
        { '$sort': { '_id.year': 1, '_id.month': 1 } }
    ]
    
    expenses = []
    for expense in collection.aggregate(pipeline):
        year = expense['_id']['year']
        month = expense['_id']['month']
        expense['index'] = f'{year}-0{month}' if month < 10 else f'{year}-{month}'
        del expense['_id']
        expense['value'] = round(expense['value'], 2)
        expenses.append(expense)
    
    return expenses


def get_expenses_by_category(start, end):
    dt_start = datetime.strptime(start, '%Y-%m-%d')
    dt_end = datetime.strptime(end, '%Y-%m-%d')

    # Get total expense by item
    pipeline = [
        { '$addFields': { 'convertedDate': { '$toDate': '$date' } } },
        { '$match': { 'convertedDate': { '$gte': dt_start, '$lte': dt_end } } },
        { '$group': {
            '_id': { 'item': '$item' },
            'expense': { '$sum': '$amount' }
        } },
        { '$sort': { 'expense': -1 } }
    ]
    
    # Divide the total by the number of months to get monthly average
    expenses = []
    diff_month = (dt_end - dt_start).days / 30
    i = 0
    other = 0
    for expense in collection.aggregate(pipeline):
        category = expense['_id']['item']
        amount = round(expense['expense'] / diff_month, 1)
        i += 1
        if i >= CATEGORY_NUM:
            other += amount
        else:
            expenses.append({ 'index': category, 'value': amount })
    expenses.append({ 'index': 'other', 'value': round(other, 2)})

    return expenses


def handler(event, context):
    
    method = event['httpMethod']
    
    body = []
    
    # Getting expense data
    if method == 'GET':
        
        params = {}
        # When no parameters are passed, event['queryStringParameters'] is None 
        # from API Gateway
        if 'queryStringParameters' in event and event['queryStringParameters'] is not None:
            params = event['queryStringParameters']

        # Get single expense data by ID
        if 'id' in params:
            id_ = params['id']
            body = get_single_expense(id_=id_)

        # Get aggregated expense data
        elif 'aggregation' in params:
            
            aggregation = params['aggregation']
            start = params['start']
            end = params['end']
        
            # Daily
            if aggregation == 'daily':
                body = get_daily_expenses(start, end)
            
            # TODO: Daily by normal and special
            
            # Monthly
            elif aggregation == 'monthly':
                body = get_monthly_expenses(start, end)
                
            # TODO: Monthly by normal and special

            # By category
            elif aggregation == 'category':
                body = get_expenses_by_category(start, end)
            
        # TODO: Get paginated data
        
        # Get all expense data
        else:
            body = get_all_expenses()
    
    body = json.dumps(body)
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': body
    }


if __name__ == '__main__':
    event = {
        'httpMethod': 'GET'
    }
    event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'id': '61fb56929b5253e4d2114600'
        }
    }
    event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'aggregation': 'daily',
            'start': '2022-11-01',
            'end': '2022-11-05'
        }
    }
    event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'aggregation': 'monthly',
            'start': '2022-10-01',
            'end': '2022-12-05'
        }
    }
    event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'aggregation': 'category',
            'start': '2022-09-01',
            'end': '2022-11-30'
        }
    }
    # event = {
    #     'httpMethod': 'GET',
    #     'queryStringParameters': None
    # }
    event = {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'aggregation': 'daily',
            'start': '2022-12-07',
            'end': '2022-12-22'
        }
    }
    pprint.pprint(handler(event, None))
