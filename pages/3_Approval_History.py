import streamlit as st
from utils import get_approvals

st.title(
    "✅ Approval History"
)

df = get_approvals()

search = st.text_input(
    "Search Reviewer or Drawing"
)

if search:

    mask = (
        df.astype(str)
        .apply(
            lambda col:
            col.str.contains(
                search,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    )

    df = df[mask]

st.dataframe(
    df,
    use_container_width=True
)
