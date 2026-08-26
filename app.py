import streamlit as st

pg = st.navigation(
    [
        st.Page(
            "Overview.py",
            title="Overview",
            icon="🏠"
        ),
        st.Page(
            "pages/1_Drawings.py",
            title="Drawings",
            icon="📐"
        ),
        st.Page(
            "pages/2_Revision_History.py",
            title="Revision History",
            icon="📜"
        ),
        st.Page(
            "pages/3_Approval_History.py",
            title="Approval History",
            icon="✅"
        ),
        st.Page(
            "pages/4_Certifications.py",
            title="Certifications",
            icon="🎓"
        ),
    ]
)

pg.run()
