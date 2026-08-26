import streamlit as st

pg = st.navigation(
    [
        st.Page(
            "Overview.py",
            title="Overview",
            icon="🏠"
        ),
        st.Page(
            "pages/Drawings.py",
            title="Drawings",
            icon="📐"
        ),
        st.Page(
            "pages/Revision_History.py",
            title="Revision History",
            icon="📜"
        ),
        st.Page(
            "pages/Approval_History.py",
            title="Approval History",
            icon="✅"
        ),
        st.Page(
            "pages/Certifications.py",
            title="Certifications",
            icon="🎓"
        ),
    ]
)

pg.run()
