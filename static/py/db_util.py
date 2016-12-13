import psycopg2 as psy
from functools import wraps

def db_connection(db):

    def tag_dec(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            connection = psy.connect('dbname = %s host = localhost' % (db))
            cursor = connection.cursor()

            result = f(cursor, *args, **kwargs)

            cursor.close()
            connection.close()
            return result

        return wrapper

    return tag_dec

@db_connection('temperature')
def get_state(cursor, state):
    sql_cmd = "select Name, ST_AsGeoJSON(Geom) from us_states where Name = '%s';" % (state)
    cursor.execute(sql_cmd)
    results = cursor.fetchall()
    return results

@db_connection('temperature')
def get_points(cursor, state):
    sql_cmd = """ SELECT c.Pedon_key, c.Temp, ST_AsGeoJSON(c.Geom)
                  FROM temperature c, us_states st
                  WHERE ST_Within(c.Geom, st.Geom)=true
                  AND st.Name='%s'; """ % state
    cursor.execute(sql_cmd)
    results = cursor.fetchall()
    return results
