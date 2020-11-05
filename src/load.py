"""load slack messages from bigquery
"""
from google.cloud import bigquery


client = bigquery.Client(project='salck-visualization')

query = """
SELECT
    um.user_id, um.name, um.deleted, um.staying_days
FROM
    slack_datamart.users_mart AS um
ORDER BY
    um.user_id
"""

query_job = client.query(query)

print('the query data')
print('==============')
print('user_id\tname\tdeleted\tstaying_days')
for row in query_job:
    print('{0}\t{1}\t{2}\t{3}'.format(row['user_id'], row['name'], row['deleted'], row['staying_days']))
