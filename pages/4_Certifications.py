import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from utils import get_certifications
import pandas as pd

# -----------------------------
# Load Data
# -----------------------------

with st.spinner("Loading certifications..."):
    df = get_certifications()

st.title("🎓 Certifications")

st.info(
    "Need to edit or add certifications? Open the SharePoint list below."
)

st.link_button(
    "📂 Open SharePoint Certifications List",
    "https://kcftech.sharepoint.com/sites/HardwareDepartment/Lists/Certification%20Tracker/AllItems.aspx",
    use_container_width=True,
)

# -----------------------------
# Prepare Data
# -----------------------------

df = df[
    [
        "Title",
        "Certification Type",
        "Report Number",
        "Standard Tested",
        "Country",
        "Issue Date",
        "Status",
    ]
]

df.columns = [
    "product_name",
    "certification_type",
    "report_number",
    "standard_tested",
    "country",
    "issue_date",
    "status",
]

df["project"] = (
    df["product_name"]
    .fillna("")
    .astype(str)
    .str.split(" - ")
    .str[0]
)

# -----------------------------
# Filter State
# -----------------------------

if "cert_search" not in st.session_state:
    st.session_state.cert_search = ""

if "cert_status" not in st.session_state:
    st.session_state.cert_status = "All"

if "cert_project" not in st.session_state:
    st.session_state.cert_project = "All"

status_options = ["All"] + sorted(
    df["status"].dropna().unique().tolist()
)

project_options = ["All"] + sorted(
    df["project"].dropna().unique().tolist()
)

# -----------------------------
# Filters
# -----------------------------

col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

with col1:
    search = st.text_input(
        "🔍 Search Certifications",
        key="cert_search",
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        status_options,
        key="cert_status",
    )

with col3:
    project_filter = st.selectbox(
        "Project",
        project_options,
        key="cert_project",
    )

with col4:
    st.write("")
    st.write("")
    if st.button("🧹 Clear"):
        st.session_state.cert_search = ""
        st.session_state.cert_status = "All"
        st.session_state.cert_project = "All"
        st.rerun()

# -----------------------------
# Apply Filters
# -----------------------------

if search:
    df = df[
        (
            df["product_name"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        )
        |
        (
            df["report_number"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        )
        |
        (
            df["certification_type"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        )
    ]

if status_filter != "All":
    df = df[df["status"] == status_filter]

if project_filter !
