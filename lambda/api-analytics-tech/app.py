from google.cloud import bigquery
from google.oauth2 import service_account
from sklearn.linear_model import LinearRegression
import pandas as pd
import json
from typing import List
import pprint
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('expand_frame_repr', False)


FILENAME ='./yuki-kitayama-api.json'
CATEGORY_TO_TAGS = {
    'programming-language': [
        'python', 'javascript', 'typescript',
        'java', 'scala', 'kotlin', 'c++', 'c#', 'ruby', 'go',
        'dart', 'swift'
    ],
    'frontend': [
        'reactjs', 'angular', 'vue.js',
        'next.js', 'flutter',
        'django', 'gatsby'
    ],
    'database': [
        'mongodb', 'redis', 'cassandra', 
        'google-bigquery', 'amazon-dynamodb', 'amazon-redshift', 
        'snowflake-cloud-data-platform'
    ]
}
YEAR = 5
ROUND = 6


def get_data(tags: List[str]) -> pd.DataFrame:
    
    tags_string = ', '.join([f"'{tag}'" for tag in tags])
    
    query = f"""
    with
    
    -- Get the recent data
    cte1 as (
      select
        format_timestamp('%Y%m', creation_date) as index,
        tags
      from
        `bigquery-public-data.stackoverflow.posts_questions`
      where
        (
          12 * extract(year from creation_date)
          + extract(month from creation_date)
        ) >= (
          12 * extract(year from timestamp_sub(current_timestamp(), interval 365 * {YEAR} day))
          + extract(month from timestamp_sub(current_timestamp(), interval 365 * {YEAR} day))
        )
    ),
    
    -- Monthly number of questions posted
    cte2 as (
      select
        index,
        count(*) as num_questions
      from
        cte1
      group by
        1
    ),
    
    -- Monthly number of questions posted with a certain tag
    cte3 as (
      select
        index,
        tag,
        count(*) as num_tags
      from
        cte1,
        -- Stack tag vertically
        unnest(split(tags, '|')) as tag
      where
        tag in ({tags_string})
      group by
        1,
        2
    )
    
    select
      a.index,
      a.tag,
      a.num_tags / b.num_questions as proportion
    from
      cte3 as a
    left join
      cte2 as b
    on
      a.index = b.index
    order by
      1,
      3 desc
    ;
    """

    credentials = service_account.Credentials.from_service_account_file(
        filename=FILENAME
    )
    df = bigquery.Client(credentials=credentials).query(query).to_dataframe()

    return df


def compute_growth_and_popularity(df: pd.DataFrame, tags: List[str]):

    data = []
    
    for tag in tags:
        
        # Prepare data
        tmp = df.loc[df['tag'] == tag]
        tmp = tmp.sort_values(by='index')
        tmp['id'] = [i for i in range(len(tmp))]
    
        # Apply linear regression
        reg = LinearRegression()
        reg.fit(tmp[['id']], tmp[['proportion']])
    
        # Compute metrics
        growth = reg.coef_[0][0]
        popularity = reg.predict(tmp.tail(1)[['id']])[0][0]
    
        # Collect data
        data.append({
            'tag': tag,
            'growth': round(growth, ROUND),
            'popularity': round(popularity, ROUND)
        })

    return data


def handler(event, context):
    
    # Get query parameters
    query = event['queryStringParameters']
    category = query['category']
    type_ = query['type']
    
    print(f'category: {category}, type: {type_}')
    
    # Return the cache if it exists in Redis
    
    # Get data
    tags = CATEGORY_TO_TAGS[category]
    df = get_data(tags=tags)
    
    # Apply analytics
    
    if type_ == 'time-series':
        
        body = []
        
        for _, row in df.iterrows():
            body.append({
                'index': row['index'],
                'tag': row['tag'],
                'proportion': round(row['proportion'], ROUND)
            })
        
        body = json.dumps(body)
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': body
        }
            
    elif type_ == 'scatter':
        
        body = compute_growth_and_popularity(df, tags)
        
        body = json.dumps(body)

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': body
        }


if __name__ == '__main__':
    # event = {
    #     'queryStringParameters': {
    #         'category': 'programming-language',
    #         'type': 'time-series'
    #     }
    # }
    # event = {
    #     'queryStringParameters': {
    #         'category': 'database',
    #         'type': 'time-series'
    #     }
    # }
    # event = {
    #     'queryStringParameters': {
    #         'category': 'programming-language',
    #         'type': 'scatter'
    #     }
    # }
    event = {
        'queryStringParameters': {
            'category': 'database',
            'type': 'scatter'
        }
    }
    event = {
        'queryStringParameters': {
            'category': 'frontend',
            'type': 'scatter'
        }
    }
    event = {
        'queryStringParameters': {
            'category': 'frontend',
            'type': 'time-series'
        }
    }
    pprint.pprint(handler(event, None))
