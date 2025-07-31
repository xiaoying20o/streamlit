import streamlit as st
import pandas as pd
import re

# hilight_keywords 
KEYWORDS = [
    'climate', 'global warming', 'weather', 'natural disaster',
    'hurricane', 'flood', 'storm', 'wildfire', 'drought', 'heatwave',
    'extreme weather', 'sea level', 'carbon', 'emission', 'sustainability',
    'environmental', 'temperature', 'greenhouse',
    'ESG', 'climate risk', 'climate change'
]

# donwload dataset
#change if you need
df = pd.read_csv(r"D:\cyber risk\data\positive_subset.csv")

# the column names to search
#change if you need 
searchable_columns = ['hurricane_context', 'Mgm_climate_context', 'RF_climate_context']

# the column showing additional information
#change if you need
info_columns = ['permno', 'label-finbert', 'score-finbert', 'Positive_pct', 'group']

# ---------------- Sidebar ----------------
st.sidebar.title("🔍 Search Climate Disclosure")

search_col = st.sidebar.selectbox("Choose context column to search:", searchable_columns)

keyword_input = st.sidebar.text_input("Enter one or more keywords (comma-separated):", "")
user_keywords = [k.strip().lower() for k in keyword_input.split(",") if k.strip() != ""]

# ---------------- main body ----------------
st.title("🌍 Climate Disclosure Dashboard")

# show dataset info
st.subheader("📋 Full Dataset (highlighting climate terms)")
def highlight_keywords(text, keywords):
    for word in keywords:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub(f"<mark>{word}</mark>", text)
    return text

# table preview with highlighted keywords
preview_df = df.copy()
for col in searchable_columns:
    if col in preview_df.columns:
        preview_df[col] = preview_df[col].fillna("").apply(lambda x: highlight_keywords(x, KEYWORDS))

st.dataframe(preview_df[searchable_columns + info_columns].fillna(""))

# search functionality
if user_keywords:
    st.subheader("🔎 Matched Results")

    # avoid NaN values in the search column
    df[search_col] = df[search_col].fillna("")

    def matches_any_keyword(text):
        text_lower = text.lower()
        return any(k in text_lower for k in user_keywords)

    matched_df = df[df[search_col].apply(matches_any_keyword)]

    st.markdown(f"Found **{len(matched_df)}** matches in `{search_col}`:")

    # show matched results with highlighted keywords
    for _, row in matched_df.iterrows():
        sentence = row[search_col]
        highlighted = highlight_keywords(sentence, user_keywords)

        st.markdown(f"<p style='margin-bottom:5px'>👉 {highlighted}</p>", unsafe_allow_html=True)

        # additional information
        extra_info = []
        for col in info_columns:
            val = row[col] if pd.notnull(row[col]) else "N/A"
            extra_info.append(f"**{col}**: {val}")
        st.markdown(", ".join(extra_info), unsafe_allow_html=True)
        st.markdown("---")
else:
    st.info("⬅️ To search, enter one or more keywords in the sidebar (e.g. hurricane, flood)")
