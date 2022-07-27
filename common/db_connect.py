import pymysql

conn = None

def db_connect(conf):
    """数据库连接
    根据配置信息,连接数据库
    Arguments:
        conf {dict} -- 连接配置信息
    Returns:
        MySQLConnection -- 数据库连接对象
    Raises:
        e -- 连接报错异常
    """
    
    global conn
    try:
        if isinstance(conn, pymysql.Connection):
            conn.ping(True,10,3)
            return conn
    except Exception as e:
        print("数据没有连接")
        
    
    try:
        conn = pymysql.connect(**conf)
        print("创建新的连接")
        return conn
    except Exception as e:
        raise e 