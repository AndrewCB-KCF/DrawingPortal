import pandas as pd
import streamlit as st
import re
import psycopg2


def get_connection():
    return psycopg2.connect(
        host=st.secrets["SUPABASE_HOST"],
        database=st.secrets["SUPABASE_DB"],
        user=st.secrets["SUPABASE_USER"],
        password=st.secrets["SUPABASE_PASSWORD"],
        port=st.secrets["SUPABASE_PORT"]
    )


@st.cache_data(ttl=60)
def get_drawings():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM drawings
        ORDER BY drawing_number
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=60)
def get_revision_history():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM revision_history
        ORDER BY created_date DESC
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=60)
def get_approvals():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM approvals
        ORDER BY approval_date DESC
        """,
        conn
    )

    conn.close()

    return df


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
