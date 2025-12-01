import psycopg2
import sys
from dotenv import load_dotenv
import os


def create_schema():

    conn = None
    cur = None

    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_PORT = os.getenv("DB_PORT")

    try:
        # database connection
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )

        cur = conn.cursor()

        print("Connection established successfully.")

        # removing old tables (if any) to rebuild schema

        print("Removing old table (if any)...")
        cur.execute("DROP TABLE IF EXISTS fact_student_monthly_performance CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_student CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_date CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_subject CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_stage CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_status CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_grade CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_advanced CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_scholarship CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dim_studytype CASCADE;")

        conn.commit()

        # create dimension tables
        cur.execute(
            """
                CREATE TABLE dim_date (
                    sk_date SERIAL PRIMARY KEY,
                    date_id VARCHAR(6) UNIQUE NOT NULL,
                    year INT NOT NULL,
                    month INT NOT NULL
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE dim_subject (
                    sk_subject SERIAL PRIMARY KEY,
                    subject VARCHAR(15) UNIQUE NOT NULL
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE dim_status (
                    sk_status SERIAL PRIMARY KEY,
                    status_name VARCHAR(15) UNIQUE NOT NULL
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE dim_grade (
                    sk_grade SERIAL PRIMARY KEY,
                    grade_id VARCHAR(3) UNIQUE NOT NULL,
                    grade_name VARCHAR(3) NOT NULL 
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE dim_advanced (
                    sk_advanced SERIAL PRIMARY KEY,
                    advanced_flag INT UNIQUE NOT NULL,
                    advanced_description VARCHAR(15) NOT NULL
                );
            """
        )
        cur.execute(
            """
                CREATE TABLE dim_scholarship (
                    sk_scholarship SERIAL PRIMARY KEY,
                    scholarship_flag INT UNIQUE NOT NULL,
                    scholarship_description VARCHAR(15) NOT NULL
                ); 
            """
        )

        cur.execute(
            """
                CREATE TABLE dim_studytype (
                    sk_studytype SERIAL PRIMARY KEY,
                    type_flag INT UNIQUE NOT NULL,
                    type_description VARCHAR(15) NOT NULL
                ); 
            """
        )

        cur.execute(
            """
                CREATE TABLE dim_student (
                    sk_student SERIAL PRIMARY KEY, 
                    student_id VARCHAR(13) UNIQUE NOT NULL,
                    full_name VARCHAR(255),
                    date_of_birth DATE NOT NULL,
                    gender CHAR
                );
            """
        )

        cur.execute(
            """
                CREATE TABLE dim_stage (
                sk_stage SERIAL PRIMARY KEY,
                stage_id VARCHAR(3) UNIQUE NOT NULL,
                stage_name VARCHAR(3) NOT NULL,
                sk_subject INT REFERENCES dim_subject(sk_subject) NOT NULL,
                UNIQUE(stage_id, sk_subject) -- stage B in math is different from stage B in japanese
                );
            """
        )

        # create fact table
        cur.execute(
            """
                CREATE TABLE fact_student_monthly_performance (
                    fact_id SERIAL PRIMARY KEY,
                    
                    -- foreign keys
                    sk_student INT NOT NULL REFERENCES dim_student (sk_student),
                    sk_date INT NOT NULL REFERENCES dim_date (sk_date),
                    sk_subject INT NOT NULL REFERENCES dim_subject (sk_subject),
                    sk_stage INT NOT NULL REFERENCES dim_stage (sk_stage),
                    sk_status INT NOT NULL REFERENCES dim_status (sk_status),
                    sk_grade INT NOT NULL REFERENCES dim_grade (sk_grade),
                    sk_studytype INT NOT NULL REFERENCES dim_studytype (sk_studytype),
                    sk_advanced INT NOT NULL REFERENCES dim_advanced (sk_advanced),           
                    sk_scholarship INT NOT NULL REFERENCES dim_scholarship (sk_scholarship),
                    
                    -- measurements
                    current_lesson INT NOT NULL,
                    total_sheets INT NOT NULL,

                    -- constraint
                    UNIQUE(sk_student, sk_date, sk_subject)                     
                );           
            """
        )

        print("Schema (re)created successfully.")
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to create schema: {error}", file=sys.stderr)
        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    create_schema()
