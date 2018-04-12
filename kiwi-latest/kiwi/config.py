from os import environ, path
from collections import namedtuple
from json import load

MySQLConfig = namedtuple('MySQLConfig', 'host port user password db')
AppConfig = namedtuple('AppConfig', 'host port')


def read_mysql_config():
    return MySQLConfig(
        host=environ['MSQL_HOST'],
        port=int(environ['MSQL_PORT']),
        user=environ['MSQL_USER'],
        password=environ['MSQL_PWD'],
        db=environ['MSQL_DATABASE']
    )


def read_rating_config():
    return {
        "min_rating": environ.get('MIN_RATING', 0),
        "max_rating": environ.get('MAX_RATING', 1)
    }


def read_app_config():
    with open(path.join(path.dirname(__file__), 'config.json')) as f:
        config = load(f)
        return AppConfig(**config)


def get_sql_statements():
    return {
        'latest_select': '''
            SELECT DISTINCT p.post_id, p.upload_time
            FROM products p
            WHERE p.post_id NOT IN (
                SELECT votes.product
                FROM votes
                WHERE votes.user = %s)
            ORDER BY upload_time DESC
            ''',
        'insert_vote': 'INSERT IGNORE INTO votes (user, product, vote) values(%s, %s, %s)',
        'insert_user': 'INSERT IGNORE INTO users values(%s)',
        'insert_item': 'INSERT IGNORE INTO products (post_id) VALUES(%s)',
        'select_user': 'SELECT * FROM users WHERE users.uname = %s',
        'count_posts': 'SELECT COUNT(post_id) FROM products',
        'count_votes': 'SELECT COUNT(*) FROM votes v WHERE v.user = %s'
    }
