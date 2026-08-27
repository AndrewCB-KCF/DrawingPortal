import streamlit as st
from utils import get_revision_history

st.title(
    "🕒 Revision History"
)

df = get_revision_history()

search = st.text_input(
    "Search Drawing Number"
)

if search:

    df = df[
        df["drawing_number"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

st.dataframe(
    df,
    use_container_width=True
)

if not df.empty:

    selected = st.selectbox(
        "Drawing Number",
        df["drawing_number"].unique()
    )

    filtered = df[
        df["drawing_number"]
        == selected
    ]

    st.subheader(
        f"Revision History - {selected}"
    )

    st.dataframe(
        filtered,
        use_container_width=True
    )
