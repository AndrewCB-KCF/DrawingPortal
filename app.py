import streamlit as st
from utils import get_drawings

st.set_page_config(
    page_title="Engineering Drawing Portal",
    page_icon="📐",
    layout="wide"
)

st.title("📐 Engineering Drawing Portal")

drawings = get_drawings()

pending = len(
    drawings[
        drawings["approval_status"] == "Pending"
    ]
)

approved = len(
    drawings[
        drawings["approval_status"] == "Approved"
    ]
)

rejected = len(
    drawings[
        drawings["approval_status"] == "Rejected"
    ]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Pending", pending)

with col2:
    st.metric("Approved", approved)

with col3:
    st.metric("Rejected", rejected)

st.divider()

st.write(
    """
    Welcome to the Engineering Drawing Portal.

    Use the navigation menu on the left to:
    - View Drawings
    - Review Revisions
    - View Approval History
    """
)

# st.divider()

# st.subheader("All Drawings")

# st.dataframe(
#     drawings,
#     use_container_width=True
# )
