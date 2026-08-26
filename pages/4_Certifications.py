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

if "cert_reset_count" not in st.session_state:
    st.session_state.cert_reset_count = 0

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
        key=f"cert_search_{st.session_state.cert_reset_count}",
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        status_options,
        key=f"cert_status_{st.session_state.cert_reset_count}",
    )

with col3:
    project_filter = st.selectbox(
        "Project",
        project_options,
        key=f"cert_project_{st.session_state.cert_reset_count}",
    )

with col4:
    st.write("")
    st.write("")

    if st.button("🧹 Clear"):
        st.session_state.cert_reset_count += 1
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

if project_filter != "All":
    df = df[df["project"] == project_filter]

# -----------------------------
# Metrics
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Products",
        len(df)
    )

with col2:
    st.metric(
        "Countries",
        df["country"].nunique()
    )

with col3:
    st.metric(
        "Certification Types",
        df["certification_type"].nunique()
    )

# -----------------------------
# Grid
# -----------------------------

grid_df = df.copy()

grid_df = grid_df[
    [
        "project",
        "product_name",
        "certification_type",
        "report_number",
        "standard_tested",
        "country",
        "issue_date",
        "status",
    ]
]

grid_df.columns = [
    "Project",
    "Product Name",
    "Certification Type",
    "Report Number",
    "Standard Tested",
    "Country",
    "Issue Date",
    "Status",
]

gb = GridOptionsBuilder.from_dataframe(
    grid_df
)

gb.configure_column(
    "Project",
    rowGroup=True,
    hide=True,
)

gb.configure_grid_options(
    groupDisplayType="groupRows"
)

gb.configure_default_column(
    sortable=True,
    filter=True,
    resizable=True,
)

gb.configure_selection(
    selection_mode="single",
    use_checkbox=False,
)

grid_options = gb.build()

grid_response = AgGrid(
    grid_df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=500,
    fit_columns_on_grid_load=True,
)

selected_rows = grid_response.get(
    "selected_rows"
)

# -----------------------------
# Details Panel
# -----------------------------

if (
    selected_rows is not None
    and len(selected_rows) > 0
):

    if isinstance(selected_rows, pd.DataFrame):
        record = selected_rows.iloc[0]
    else:
        record = pd.Series(selected_rows[0])

    details_tab, properties_tab = st.tabs(
        [
            "Details",
            "Properties",
        ]
    )

    with details_tab:

        st.subheader(
            record["Product Name"]
        )

        st.write(
            f"**Certification Type:** {record['Certification Type']}"
        )

        st.write(
            f"**Report Number:** {record['Report Number']}"
        )

        st.write(
            f"**Standard Tested:** {record['Standard Tested']}"
        )

        st.write(
            f"**Country:** {record['Country']}"
        )

        st.write(
            f"**Issue Date:** {record['Issue Date']}"
        )

        status = record["Status"]

        if status == "Active":
            st.success(status)

        elif status == "Expired":
            st.error(status)

        else:
            st.info(status)

    with properties_tab:

        st.text_input(
            "Product Name",
            value=record["Product Name"],
            disabled=True,
        )

        st.text_input(
            "Certification Type",
            value=record["Certification Type"],
            disabled=True,
        )

        st.text_input(
            "Report Number",
            value=record["Report Number"],
            disabled=True,
        )

        st.text_input(
            "Standard Tested",
            value=record["Standard Tested"],
            disabled=True,
        )

        st.text_input(
            "Country",
            value=record["Country"],
            disabled=True,
        )

        st.text_input(
            "Issue Date",
            value=str(record["Issue Date"]),
            disabled=True,
        )

        st.text_input(
            "Status",
            value=record["Status"],
            disabled=True,
        )
