import sqlite3
import pandas as pd
from pathlib import Path
import streamlit as st

DB_PATH = Path(__file__).parent / "SMARTDrawings Database-KCF-4DPWP74 - Copy.db"


def get_connection():
    return sqlite3.connect(DB_PATH)

@st.cache_data(ttl=300)
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

@st.cache_data(ttl=300)
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

def get_certifications():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT *
        FROM certifications
        ORDER BY product_name
        """,
        conn
    )

    conn.close()

    return df
