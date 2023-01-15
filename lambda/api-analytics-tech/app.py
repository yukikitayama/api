from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import pprint
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('expand_frame_repr', False)


FILENAME ='./yuki-kitayama-api.json'


def get_data():
    
    credentials = service_account.Credentials.from_service_account_file(
        filename=FILENAME
    )
    bq = bigquery.Client(credentials=credentials)
    
    query = """
    select
      *
    from
      `bigquery-public-data.stackoverflow.posts_questions`
    limit
      1
    """
    df = bq.query(query).to_dataframe()
    
    print(df.head())
    
    return df


def handler(event, context):
    
    # Get query parameters
    query = event['queryStringParameters']
    category = query['category']
    type_ = query['type']
    
    print(f'category: {category}, type: {type_}')
    
    # Get data
    df = get_data()


if __name__ == '__main__':
    event = {
        'queryStringParameters': {
            'category': 'programming-language',
            'type': 'time-series'
        }
    }
    pprint.pprint(handler(event, None))
