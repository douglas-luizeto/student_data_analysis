import psycopg2
import numpy as np

conn = psycopg2.connect(
    """
        dbname='student_analysis'
        user='postgres'
        host='localhost'
        password='cherantoine'
    """
)

cur = conn.cursor()
cur.execute(
    """
        CREATE TABLE facts_students (student_id INT PRIMARY KEY);
    """
)
conn.commit()
conn.close()
cur.close()
