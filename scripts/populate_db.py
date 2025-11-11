import psycopg2
import csv
from pathlib import Path
import sys

# Open CSV file
script_path = Path(__file__)
script_dir = script_path.parent
base_dir = script_dir.parent
student_data_path = base_dir / "student_data.csv"
stage_data_path = base_dir / "stage_data.csv"

# with open(student_data_path, encoding="utf-8") as student_csvfile:
#     reader = csv.DictReader(student_csvfile)

# Connect to database
conn = None
cur = None

try:
    with open(student_data_path, encoding="utf-8") as student_csvfile:
        reader = csv.DictReader(student_csvfile)

        conn = psycopg2.connect(
            host="localhost",
            database="student_analysis",
            user="postgres",
            password="cherantoine",
            port=5432,
        )
        print("Connection sucessfully established")

        cur = conn.cursor()

        # populate dim_advanced
        cur.execute(
            """
                INSERT INTO dim_advanced (advanced_flag, advanced_description)
                VALUES 
                    (0, 'not advanced'),
                    (1, 'advanced')
                ON CONFLICT DO NOTHING;
            """
        )

        # populate dim_grade
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

        # populate dim_scholarship
        cur.execute(
            """
                INSERT INTO dim_scholarship (scholarship_flag, scholarship_description)
                VALUES
                    (0, 'no scholarship'),
                    (1, 'scholarship')
                ON CONFLICT DO NOTHING;
            """
        )

        # populate dim_status
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

        # populate dim_subject
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

        conn.commit()

        # open stage_data
        with open(stage_data_path, encoding="utf-8") as stage_csvfile:
            stage_reader = csv.DictReader(stage_csvfile)

            # collect surrogate_keys from dim_subject
            cur.execute(
                """
                    SELECT subject, sk_subject FROM dim_subject;
                """
            )
            subject_sk = {name: sk for name, sk in cur.fetchall()}

            # populate dim_stage
            for stage in stage_reader:
                cur.execute(
                    f"""
                    INSERT INTO dim_stage (stage_id, stage_name, sk_subject)
                    VALUES ('{stage['stage_id']}', '{stage['stage_name']}', {subject_sk[stage['subject']]})
                    ON CONFLICT DO NOTHING;
                    """
                )

        # populate dim_date and dim_student
        for fact in reader:
            date_id = fact["date"]
            cur.execute(
                f"""
                    INSERT INTO dim_date (date_id, year, month)
                    VALUES ({date_id}, {date_id[0:4]}, {date_id[4:]})
                    ON CONFLICT DO NOTHING;
                """
            )

            # converts date: DD/MM/YYYY -> YYYY-MM-DD
            date_of_birth = "-".join(fact["date_of_birth"].split("/")[::-1])

            cur.execute(
                f"""
                    INSERT INTO dim_student (student_id, full_name, date_of_birth)
                    VALUES ('{fact['student_id']}', '{fact['full_name']}', '{date_of_birth}')
                    ON CONFLICT DO NOTHING;
                """
            )

        conn.commit()

    # collect surrogate keys for all dims
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

    # populate fact table
    with open(student_data_path, encoding="utf-8") as student_csvfile:
        reader = csv.DictReader(student_csvfile)

        for fact in reader:
            cur.execute(
                f"""
                    INSERT INTO fact_student_monthly_performance (sk_student, sk_date, sk_subject, sk_stage, sk_status, sk_grade, sk_advanced, sk_scholarship, current_lesson, total_sheets)
                    VALUES
                        (
                            {student_sk[fact['student_id']]},
                            {date_sk[fact['date']]},
                            {subject_sk[fact['subject']]},
                            {stage_sk[fact['stage_id']]},
                            {status_sk[fact['status']]},
                            {grade_sk[fact['grade_id']]},
                            {advanced_sk[int(fact['advanced'])]},
                            {scholarship_sk[int(fact['scholarship'])]},
                            {fact['current_lesson']},
                            {fact['total_sheets']}
                        )
                    ON CONFLICT DO NOTHING;
                """
            )

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
