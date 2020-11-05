"""load slack messages from bigquery
"""
from google.cloud import bigquery


class DlgDwhLoader:
    def __init__(self, project_id: str):
        self.client = bigquery.Client(project=project_id)
    
    def users(self, deleted_user: bool=False, bot_user: bool=False) -> bigquery.job.QueryJob:
        """Load DWH.users
            Arguments:
                deleted_user: True=include deleted users(All users), False=Remove deleted_users.
                bot_user: True=include bot(All users), False=Remove bot.

            Returns:
                bigquery.job.QueryJob obj. (using to_dataframe function to trans)
        """
        where_clause = ''
        if (deleted_user is False) and (bot_user is True):
            where_clause = """
            WHERE
                u.deleted = false
            """
        elif (deleted_user is True) and (bot_user is False):
            where_clause = """
            WHERE
                u.is_bot = false
            """
        elif (deleted_user is False) and (bot_user is False):
            where_clause = """
            WHERE
                u.deleted = false AND
                u.is_bot = false
            """

        query = """
        SELECT
            *
        FROM
            slack_dwh.users AS u
        {}
        """.format(where_clause)

        query_job = self.client.query(query)
        print(type(query_job))
        return query_job

    
    def users_mart(self, deleted_user: bool=False) -> bigquery.job.QueryJob:
        """Load DataMart.users_mart
            Arguments:
                deleted_user: True=include deleted users(All users), False=Remove deleted_users.

            Returns:
                bigquery.job.QueryJob obj. (using to_dataframe function to trans)
        """
        where_clause = ''
        if (deleted_user is False):
            where_clause = """
            WHERE
                um.deleted = false
            """

        query = """
        SELECT
            *
        FROM
            slack_datamart.users_mart AS um
        {}
        """.format(where_clause)

        query_job = self.client.query(query)
        return query_job

    def msgs_by_user(self, user_id: str=None, ch_join_msg: bool=False) -> bigquery.job.QueryJob:
        """Messages by user.
            Arguments:
                user_id: メッセージを投稿したユーザーのID
                ch_join_msg: チャンネル参加メッセージを含むかどうか（False：含まない）
        """
        where_clause = """
        WHERE
            m.user_id = '{}'
        """.format(user_id)
        
        if (ch_join_msg is False):
            where_clause += "AND \n\tm.text NOT LIKE '%さんがチャンネルに参加しました'"

        query = """
        SELECT
            *
        FROM
            slack_dwh.messages AS m
        {}
        """.format(where_clause)

        query_job = self.client.query(query)
        return query_job
