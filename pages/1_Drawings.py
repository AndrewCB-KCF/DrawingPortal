import streamlit as st
import sqlite3
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder
import streamlit.components.v1 as components
from st_aggrid import JsCode
from utils import (
    get_drawings,
    get_connection,
    get_revision_history
)

st.title("📐 Drawings Library")

df = get_drawings()

if "search" not in st.session_state:
    st.session_state.search = ""

if "status_filter" not in st.session_state:
    st.session_state.status_filter = "All"

if st.session_state.get("clear_filters", False):
    st.session_state["search"] = ""
    st.session_state["status_filter"] = "All"
    st.session_state.clear_filters = False

col1, col2, col3 = st.columns([4, 2, 1])


with col1:
    search = st.text_input(
        "🔍 Search Drawings",
        key="search"
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        [
            "All",
            "Pending",
            "Approved",
            "Rejected"
        ],
        key="status_filter"
    )

with col3:
    st.write("")
    st.write("")

    if st.button("🔄 Reset Filters"):
        st.session_state.clear_filters = True
        st.rerun()

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
#Comment below if doesn't work
# link_renderer = JsCode("""
# function(params) {
#     return params.value;
# }
# """)
#
grid_df["Open"] = grid_df["File Path"]


gb = GridOptionsBuilder.from_dataframe(grid_df)
#Comment out below if doesn't work
# gb.configure_column(
#     "Drawing Number",
#     cellRenderer=link_renderer
# )

gb.configure_default_column(
    sortable=True,
    filter=True,
    resizable=True
)

gb.configure_selection(
    selection_mode="single",
    use_checkbox=False
)

gb.configure_column(
    "Open",
    header_name="Open",
    cellRenderer=JsCode("""
        class UrlCellRenderer {
            init(params) {
                this.eGui = document.createElement('a');
                this.eGui.innerText = '📂 Open';
                this.eGui.setAttribute('href', params.value);
                this.eGui.setAttribute('target', '_blank');
            }
            getGui() {
                return this.eGui;
            }
        }
    """)
)

gb.configure_column(
    "File Path",
    hide=True
)

grid_options = gb.build()

grid_response = AgGrid(
    grid_df,
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
    height=400,
    fit_columns_on_grid_load=True
)


selected_rows = grid_response.get("selected_rows")

if selected_rows is not None and len(selected_rows) > 0:

    # st.write(selected_rows.columns.tolist())
    # st.write(selected_rows.head())
    drawing_number = selected_rows.iloc[0]["Drawing Number"]

    record = df[
        df["drawing_number"]
        == drawing_number
    ].iloc[0]

    details_tab, revisions_tab, properties_tab, approvals_tab = st.tabs(
        [
            "Details",
            "Revision History",
            "Properties",
            "Approvals"
        ]
    )

    with details_tab:
    
        st.subheader(record["title"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Drawing Number",
                record["drawing_number"]
            )
        
        with col2:
            st.metric(
                "Revision",
                record["revision"]
            )
        
        with col3:
            st.metric(
                "Status",
                record["approval_status"]
            )
    
        if record["file_path"]:
        
            st.success(
                f"Current Revision: {record['revision']}"
            )

        if record["file_path"]:
        
            st.link_button(
                f"📂 Open Revision {record['revision']}",
                record["file_path"],
                use_container_width=True
            )
        
            st.divider()
        
            st.subheader("Preview")
        
            components.iframe(
                record["file_path"],
                height=800,
                scrolling=True
            )
    
            # st.link_button(
            #     f"📂 Open Revision {record['revision']}",
            #     record["file_path"],
            #     use_container_width=True
            # )
    
    with revisions_tab:
    
        st.subheader("Revision History")
    
        selected_revisions = revision_df[
            revision_df["drawing_number"]
            == drawing_number
        ]
    
        if len(selected_revisions) > 0:
    
            for _, rev in selected_revisions.iterrows():
            
                col1, col2 = st.columns([1, 3])
            
                with col1:
                    st.write(f"Rev {rev['revision']}")
            
                with col2:
            
                    if rev["file_path"]:
            
                        st.link_button(
                            "📂 Open",
                            rev["file_path"]
                        )
    
        else:
    
            st.info("No revision history found.")

    with properties_tab:
    
        with st.form(f"edit_form_{drawing_number}"):
    
            new_drawing_number = st.text_input(
                "Drawing Number",
                value=record["drawing_number"]
            )
    
            new_title = st.text_input(
                "Title",
                value=record["title"]
            )
    
            new_revision = st.text_input(
                "Revision",
                value=record["revision"]
            )
    
            new_file_path = st.text_input(
                "File Path",
                value=record["file_path"]
            )
    
            submitted = st.form_submit_button(
                "💾 Save Changes"
            )

        if submitted:
    
            conn = get_connection()
            cursor = conn.cursor()
    
            cursor.execute(
                """
                UPDATE drawings
                SET
                    drawing_number = ?,
                    title = ?,
                    revision = ?,
                    file_path = ?
                WHERE drawing_number = ?
                """,
                (
                    new_drawing_number,
                    new_title,
                    new_revision,
                    new_file_path,
                    drawing_number
                )
            )
    
            conn.commit()
            conn.close()
    
            st.success("Drawing Updated")
    
            st.rerun()

    with approvals_tab:
    
        st.subheader("✅ Approval Workflow")
    
        reviewer = st.text_input(
            "Reviewer",
            key=f"reviewer_{drawing_number}"
        )
    
        comments = st.text_area(
            "Comments",
            key=f"comments_{drawing_number}"
        )
    
        col1, col2 = st.columns(2)
    
        with col1:
    
            if st.button(
                "✅ Approve",
                key=f"approve_{drawing_number}"
            ):
    
                conn = get_connection()
                cursor = conn.cursor()
    
                cursor.execute(
                    """
                    UPDATE drawings
                    SET approval_status='Approved'
                    WHERE drawing_number=?
                    """,
                    (drawing_number,)
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
    
                st.success("Drawing Approved")
    
                st.rerun()
    
        with col2:
    
            if st.button(
                "❌ Reject",
                key=f"reject_{drawing_number}"
            ):
    
                conn = get_connection()
                cursor = conn.cursor()
    
                cursor.execute(
                    """
                    UPDATE drawings
                    SET approval_status='Rejected'
                    WHERE drawing_number=?
                    """,
                    (drawing_number,)
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
    
                st.success("Drawing Rejected")
    
                st.rerun()

else:

    st.info("Select a drawing to view details.")

with st.expander("➕ Add Drawing"):

    drawing_number = st.text_input(
        "Drawing Number",
        key="add_drawing_number"
    )

    title = st.text_input(
        "Title",
        key="add_title"
    )

    revision = st.text_input(
        "Revision",
        value="A",
        key="add_revision"
    )

    file_path = st.text_input(
        "SharePoint Link",
        key="add_file_path"
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
