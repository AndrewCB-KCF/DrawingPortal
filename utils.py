import pandas as pd
import streamlit as st
import re
from contextlib import contextmanager
from psycopg2 import pool


@st.cache_resource
def get_pool():
    return pool.ThreadedConnectionPool(
        1,
        10,
        host=st.secrets["SUPABASE_HOST"],
        database=st.secrets["SUPABASE_DB"],
        user=st.secrets["SUPABASE_USER"],
        password=st.secrets["SUPABASE_PASSWORD"],
        port=st.secrets["SUPABASE_PORT"]
    )


@contextmanager
def get_conn():
    conn = get_pool().getconn()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        get_pool().putconn(conn)


@contextmanager
def get_cursor(commit=False):
    with get_conn() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            if commit:
                conn.commit()
        finally:
            cursor.close()


@st.cache_data(ttl=60)
def get_drawings():

    with get_conn() as conn:

        return pd.read_sql(
            """
            SELECT *
            FROM drawings
            ORDER BY drawing_number
            """,
            conn
        )


@st.cache_data(ttl=60)
def get_revision_history():

    with get_conn() as conn:

        return pd.read_sql(
            """
            SELECT *
            FROM revision_history
            ORDER BY created_date DESC
            """,
            conn
        )


@st.cache_data(ttl=60)
def get_approvals():

    with get_conn() as conn:

        return pd.read_sql(
            """
            SELECT *
            FROM approvals
            ORDER BY approval_date DESC
            """,
            conn
        )


@st.cache_data
def get_certifications(file_modified_time):

    df = pd.read_csv(
        "data/Certifications.csv"
    )

    def extract_report_numbers(html):

        if pd.isna(html):
            return ""

        reports = re.findall(
            r'title="([^"]+)"',
            str(html)
        )

        return ", ".join(reports)

    if "Report Number" in df.columns:
        df["Report Number"] = (
            df["Report Number"]
            .apply(extract_report_numbers)
        )

    return df
