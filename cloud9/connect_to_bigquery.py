from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('expand_frame_repr', False)


FILENAME ='../yuki-kitayama-api.json'


def main():
    
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


if __name__ == '__main__':
    main()
