import streamlit as st
import sqlite3
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder

from utils import (
    get_drawings,
    get_connection,
    get_revision_history
)

st.title("📐 Drawings Library")

df = get_drawings()

search = st.text_input(
    "🔍 Search Drawings"
)

df = get_drawings()
revision_df = get_revision_history()

if search:

    df = df[
        (
            df["drawing_number"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )
        |
        (
            df["title"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )
        |
        (
            df["revision"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )
        |
        (
            df["approval_status"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        )
    ]

status_filter = st.selectbox(
    "Status",
    [
        "All",
        "Pending",
        "Approved",
        "Rejected"
    ]
)

if status_filter != "All":

    df = df[
        df["approval_status"]
        == status_filter
    ]

grid_df = df.copy()

grid_df = grid_df[
    [
        "drawing_number",
        "title",
        "revision",
        "approval_status",
        "file_path"
    ]
]

grid_df.columns = [
    "Drawing Number",
    "Title",
    "Revision",
    "Status",
    "File Path"
]
# display_df = df.copy()

# display_df["Drawing Number"] = display_df.apply(
#     lambda row:
#         f"<a href='{row['file_path']}' target='_blank'>{row['drawing_number']}</a>",
#     axis=1
# )

# display_df = display_df[
#     [
#         "Drawing Number",
#         "title",
#         "revision",
#         "approval_status"
#     ]
# ]

# display_df.columns = [
#     "Drawing Number",
#     "Title",
#     "Revision",
#     "Status"
# ]

# st.markdown(
#     display_df.to_html(
#         escape=False,
#         index=False
#     ),
#     unsafe_allow_html=True
# )

gb = GridOptionsBuilder.from_dataframe(grid_df)

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
    height=400,
    fit_columns_on_grid_load=True
)

# if len(df) > 0:

selected_rows = grid_response.get("selected_rows")

if selected_rows is not None and len(selected_rows) > 0:

    drawing_number =["
if selected_rows is not None and

    record = df[
        df["drawing_number"]
        == drawing_number
    ].iloc[0]

    st.divider()

    st.subheader(record["title"])

    st.write(
        f"[0Drawing Number: {recorddrawing_number']}"
    )

    st.write(
        f"Revision: {record['revision']}"
    )

    st.write(
        f"Status: {record['approval_status']}"
    )

    if record["file_path"]:

        st.link_button(
            "📂 Open Drawing",
            record["file_path"]
        )

    st.subheader("Revision History")

    selected_revisions = revision_df[
        revision_df["drawing_number"]
        == drawing_number
    ]

    if len(selected_revisions) > 0:

        for _, rev in selected_revisions.iterrows():

            if rev["file_path"]:

                st.link_button(
                    f"Revision {rev['revision']}",
                    rev["file_path"]
                )

    else:

        st.info("No revision history found.")
    
    reviewer = st.text_input(
        "Reviewer"
    )

    comments = st.text_area(
        "Comments"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✅ Approve"):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE drawings
                SET approval_status='Approved'
                WHERE drawing_number=?
                """,
                (
                    drawing_number,
                )
            )

            cursor.execute(
                """
                INSERT INTO approvals
                (
                    drawing_number,
                    revision,
                    reviewer,
                    decision,
                    comments,
                    approval_date
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    drawing_number,
                    record["revision"],
                    reviewer,
                    "Approved",
                    comments,
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )

            conn.commit()
            conn.close()

            st.success(
                "Drawing Approved"
            )

            st.rerun()

    with col2:

        if st.button("❌ Reject"):

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE drawings
                SET approval_status='Rejected'
                WHERE drawing_number=?
                """,
                (
                    drawing_number,
                )
            )

            cursor.execute(
                """
                INSERT INTO approvals
                (
                    drawing_number,
                    revision,
                    reviewer,
                    decision,
                    comments,
                    approval_date
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    drawing_number,
                    record["revision"],
                    reviewer,
                    "Rejected",
                    comments,
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
            )

            conn.commit()
            conn.close()

            st.success(
                "Drawing Rejected"
            )

            st.rerun()

st.divider()

with st.expander("➕ Add Drawing"):

    drawing_number = st.text_input(
        "Drawing Number"
    )

    title = st.text_input(
        "Title"
    )

    revision = st.text_input(
        "Revision",
        value="A"
    )

    file_path = st.text_input(
        "SharePoint Link"
    )

    if st.button("Save Drawing"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO drawings
            (
                drawing_number,
                title,
                revision,
                file_path,
                approval_status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                drawing_number,
                title,
                revision,
                file_path,
                "Pending"
            )
        )

        conn.commit()
        conn.close()

        st.success(
            "Drawing Added"
        )

        st.rerun()
