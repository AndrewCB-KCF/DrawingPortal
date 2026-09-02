import pandas as pd
import streamlit as st
import re
from contextlib import contextmanager
from psycopg2 import pool
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


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


@st.cache_resource
def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=st.secrets["SUPABASE_USER"],
        password=st.secrets["SUPABASE_PASSWORD"],
        host=st.secrets["SUPABASE_HOST"],
        port=int(st.secrets["SUPABASE_PORT"]),
        database=st.secrets["SUPABASE_DB"]
    )
    return create_engine(url)


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

    return pd.read_sql(
        """
        SELECT *
        FROM drawings
        ORDER BY drawing_number
        """,
        get_engine()
    )


@st.cache_data(ttl=60)
def get_revision_history():

    return pd.read_sql(
        """
        SELECT *
        FROM revision_history
        ORDER BY created_date DESC
        """,
        get_engine()
    )


@st.cache_data(ttl=60)
def get_approvals():

    return pd.read_sql(
        """
        SELECT *
        FROM approvals
        ORDER BY approval_date DESC
        """,
        get_engine()
    )


@st.cache_data
def get_certifications(file_modified_time):

    df = pd.read_csv(
        "data/Certifications.csv"
    )

    def extract_report_numbers(html):

        if pd.isna(html):
            return ""

        html = str(html)

        reports = re.findall(
            r'title="([^"]+)"',
            html
        )

        if reports:
            return ", ".join(reports)

        # No hyperlinks present - fall back to the plain text content
        text = re.sub(r'<[^>]+>', ' ', html)
        return re.sub(r'\s+', ' ', text).strip()

    if "Report Number" in df.columns:
        df["Report Number"] = (
            df["Report Number"]
            .apply(extract_report_numbers)
        )

    return df
