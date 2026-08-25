import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid import GridUpdateMode
from utils import get_certifications

st.title("🎓 Certifications")

df = get_certifications()

# Search

search = st.text_input(
    "🔍 Search Certifications"
)

if search:

    df = df[
        (
            df["product_name"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )
        |
        (
            df["report_number"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )
        |
        (
            df["certification_type"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )
    ]

# Status Filter

status_filter = st.selectbox(
    "Status",
    [
        "All"
    ]
    +
    sorted(
        df["status"]
        .dropna()
        .unique()
    )
)

if status_filter != "All":

    df = df[
        df["status"]
        == status_filter
    ]

# Metrics

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

# Grid

grid_df = df.copy()

grid_df = grid_df[
    [
        "product_name",
        "certification_type",
        "report_number",
        "standard_tested",
        "country",
        "issue_date",
        "status"
    ]
]

grid_df.columns = [
    "Product Name",
    "Certification Type",
    "Report Number",
    "Standard Tested",
    "Country",
    "Issue Date",
    "Status"
]

gb = GridOptionsBuilder.from_dataframe(
    grid_df
)

gb.configure_default_column(
    sortable=True,
    filter=True,
    resizable=True
)

gb.configure_selection(
    selection_mode="single",
    use_checkbox=False
)

grid_options = gb.build()

grid_response = AgGrid(
    grid_df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=400,
    fit_columns_on_grid_load=True
)

selected_rows = grid_response.get(
    "selected_rows"
)

if (
    selected_rows is not None
    and
    len(selected_rows) > 0
):

    record = selected_rows.iloc[0]

    details_tab, properties_tab = st.tabs(
        [
            "Details",
            "Properties"
        ]
    )

    with details_tab:

        st.subheader(
            record["Product Name"]
        )

        st.write(
            f"Certification Type: {record['Certification Type']}"
        )

        st.write(
            f"Report Number: {record['Report Number']}"
        )

        st.write(
            f"Standard Tested: {record['Standard Tested']}"
        )

        st.write(
            f"Country: {record['Country']}"
        )

        st.write(
            f"Issue Date: {record['Issue Date']}"
        )

        status = record["Status"]

        if status == "Active":

            st.success(status)

        elif status == "Expired":

            st.error(status)

        else:

            st.info(status)

    with properties_tab:

        with st.form(
            f"cert_form_{product_name}"
        ):

            new_product_name = st.text_input(
                "Product Name",
                value=record["Product Name"]
            )

            new_cert_type = st.text_input(
                "Certification Type",
                value=record["Certification Type"]
            )

            new_report_number = st.text_input(
                "Report Number",
                value=record["Report Number"]
            )

            new_standard = st.text_input(
                "Standard Tested",
                value=record["Standard Tested"]
            )

            new_country = st.text_input(
                "Country",
                value=record["Country"]
            )

            new_issue_date = st.text_input(
                "Issue Date",
                value=str(record["Issue Date"])
            )

            new_status = st.text_input(
                "Status",
                value=record["Status"]
            )

            submitted = st.form_submit_button(
                "💾 Save Changes"
            )

        if submitted:

            st.success(
                "Certification Updated"
            )

            # Add UPDATE query here
