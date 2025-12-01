import psycopg2
import csv
from pathlib import Path
import sys
from dotenv import load_dotenv
import os

# Open CSV files
script_path = Path(__file__)
script_dir = script_path.parent
base_dir = script_dir.parent
fact_data_path = base_dir / "student_data-updated.csv"
stage_data_path = base_dir / "stage_data.csv"

# Converted to a list for reuse
with open(fact_data_path, encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    fact_list = list(reader)

with open(stage_data_path, encoding="utf-8") as stage_csvfile:
    stage_reader = csv.DictReader(stage_csvfile)
    stage_list = list(stage_reader)


# Connect to database
conn = None
cur = None

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )
    print("Connection sucessfully established")

    cur = conn.cursor()

    # Populate dim_advanced
    cur.execute(
        """
            INSERT INTO dim_advanced (advanced_flag, advanced_description)
            VALUES 
                (0, 'not advanced'),
                (1, 'advanced')
            ON CONFLICT DO NOTHING;
        """
    )

    # Populate dim_grade
    cur.execute(
        """
            INSERT INTO dim_grade (grade_id, grade_name) 
            VALUES 
                (-5, 'F5'),
                (-4, 'F4'),
                (-3, 'F3'),
                (-2, 'F2'),
                (-1, 'F1'),
                (0, 'EE'),
                (1, '1EF'),
                (2, '2EF'),
                (3, '3EF'),
                (4, '4EF'),
                (5, '5EF'),
                (6, '6EF'),
                (7, '7EF'),
                (8, '8EF'),
                (9, '9EF'),
                (10, '1EM'),
                (11, '2EM'),
                (12, '3EM'),
                (13, 'AD')
            ON CONFLICT DO NOTHING;
        """
    )

    # Populate dim_scholarship
    cur.execute(
        """
            INSERT INTO dim_scholarship (scholarship_flag, scholarship_description)
            VALUES
                (0, 'no scholarship'),
                (1, 'scholarship')
            ON CONFLICT DO NOTHING;
        """
    )

    # Populate dim_studytype

    cur.execute(
        """
            INSERT INTO dim_studytype (type_flag, type_description)
            VALUES
                (0, 'paper'),
                (1, 'connect')
            ON CONFLICT DO NOTHING;
        """
    )

    # Populate dim_status
    cur.execute(
        """
            INSERT INTO dim_status (status_name)
            VALUES
                ('absent'),
                ('absent_graduate'),
                ('absent_transfer'),
                ('current'),
                ('new'),
                ('new_former'),
                ('new_multi')
            ON CONFLICT DO NOTHING
        """
    )

    # Populate dim_subject
    cur.execute(
        """
            INSERT INTO dim_subject (subject)
            VALUES
                ('math'),
                ('portuguese'),
                ('english'),
                ('japanese')
            ON CONFLICT DO NOTHING
        """
    )

    # Collect surrogate_keys from dim_subject
    cur.execute(
        """
            SELECT subject, sk_subject FROM dim_subject;
        """
    )
    subject_sk = {name: sk for name, sk in cur.fetchall()}

    data_dim_stage = [
        (stage["stage_id"], stage["stage_name"], subject_sk[stage["subject"]])
        for stage in stage_list
    ]
    sql_dim_stage = """
                        INSERT INTO dim_stage (stage_id, stage_name, sk_subject)
                        VALUES (%s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """
    if data_dim_stage:
        cur.executemany(sql_dim_stage, data_dim_stage)

    # Populate dim_date

    # Collect unique date values
    unique_dim_date = {
        (fact["date"], fact["date"][0:4], fact["date"][4:])
        for fact in fact_list
        if fact["date"]
    }

    data_dim_date = list(unique_dim_date)

    sql_dim_date = """
                        INSERT INTO dim_date (date_id, year, month)
                        VALUES (%s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """

    if data_dim_date:
        cur.executemany(sql_dim_date, data_dim_date)

    # Populate dim_student

    # Helper function to convert 'date_of_birth' from DD/MM/YYYY to expected format YYYY-MM-DD
    def format_date(date_str):
        if not date_str:
            return None
        return "-".join(date_str.split("/")[::-1])

    # Collect unique student values
    unique_dim_student = {
        (
            fact["student_id"],
            fact["full_name"],
            format_date(fact["date_of_birth"]),
            fact["gender"][0],
        )
        for fact in fact_list
        if fact["student_id"]
    }

    data_dim_student = list(unique_dim_student)

    sql_dim_student = """
                        INSERT INTO dim_student (student_id, full_name, date_of_birth, gender)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                      """

    cur.executemany(sql_dim_student, data_dim_student)

    # Collect surrogate keys for all dims
    cur.execute(
        """
            SELECT advanced_flag, sk_advanced FROM dim_advanced;
        """
    )
    advanced_sk = {flag: sk for flag, sk in cur.fetchall()}

    cur.execute(
        """
            SELECT scholarship_flag, sk_scholarship FROM dim_scholarship;
        """
    )
    scholarship_sk = {flag: sk for flag, sk in cur.fetchall()}

    cur.execute(
        """
            SELECT grade_id, sk_grade FROM dim_grade;
        """
    )
    grade_sk = {id: sk for id, sk in cur.fetchall()}

    cur.execute(
        """
            SELECT stage_id, sk_stage FROM dim_stage;
        """
    )
    stage_sk = {id: sk for id, sk in cur.fetchall()}

    cur.execute(
        """
            SELECT status_name, sk_status FROM dim_status;
        """
    )
    status_sk = {name: sk for name, sk in cur.fetchall()}

    cur.execute(
        """
            SELECT subject, sk_subject FROM dim_subject;
        """
    )
    subject_sk = {name: sk for name, sk in cur.fetchall()}

    cur.execute(
        """
            SELECT date_id, sk_date FROM dim_date;
        """
    )
    date_sk = {id: sk for id, sk in cur.fetchall()}

    cur.execute(
        """
            SELECT student_id, sk_student FROM dim_student;
        """
    )
    student_sk = {id: sk for id, sk in cur.fetchall()}

    cur.execute(
        """
            SELECT type_description, sk_studytype FROM dim_studytype;
        """
    )
    studytype_sk = {type: sk for type, sk in cur.fetchall()}

    # Populate fact table

    data_fact_table = [
        (
            student_sk[fact["student_id"]],
            date_sk[fact["date"]],
            subject_sk[fact["subject"]],
            stage_sk[fact["stage_id"]],
            status_sk[fact["status"]],
            grade_sk[fact["grade_id"]],
            studytype_sk[fact["type"]],
            advanced_sk[int(fact["advanced"])],
            scholarship_sk[int(fact["scholarship"])],
            fact["current_lesson"],
            fact["total_sheets"],
        )
        for fact in fact_list
    ]

    sql_fact_table = """
                        INSERT INTO fact_student_monthly_performance (sk_student, 
                                                                      sk_date, 
                                                                      sk_subject, 
                                                                      sk_stage, 
                                                                      sk_status, 
                                                                      sk_grade,
                                                                      sk_studytype,
                                                                      sk_advanced, 
                                                                      sk_scholarship,
                                                                      current_lesson,
                                                                      total_sheets)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        ON CONFLICT DO NOTHING;
                     """
    cur.executemany(sql_fact_table, data_fact_table)

    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Database error: {error}", file=sys.stderr)
    if conn:
        conn.rollback()

finally:
    if cur:
        cur.close()
    if conn:
        conn.close()
    print("Connection closed.")
