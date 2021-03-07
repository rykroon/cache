from redis import ConnectionPool, Redis 


connection_pool = None


def connect(*args, **kwargs):
    global connection_pool
    connection_pool = ConnectionPool(*args, **kwargs)
    return connection_pool


def get_client():
    return Redis(connection_pool=connection_pool)