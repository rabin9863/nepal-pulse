# import json
# import pandas as pd
# import streamlit as st
# from kafka import KafkaConsumer
# from collections import Counter
# import re
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.decomposition import LatentDirichletAllocation

# BOOTSTRAP_SERVERS = "localhost:9092"
# TOPIC = "processed-news"

# st.set_page_config(page_title="Nepal Pulse Dashboard", layout="wide")

# st.title("🇳🇵 Nepal Pulse")
# st.subheader("Real-Time Knowledge Discovery Engine for Nepali News Streams")

# @st.cache_data(ttl=10)
# def load_messages():
#     consumer = KafkaConsumer(
#         TOPIC,
#         bootstrap_servers=BOOTSTRAP_SERVERS,
#         auto_offset_reset="earliest",
#         enable_auto_commit=True,
#         consumer_timeout_ms=3000,
#         value_deserializer=lambda x: json.loads(x.decode("utf-8"))
#     )

#     rows = []
#     for message in consumer:
#         rows.append(message.value)

#     return rows

# rows = load_messages()

# if not rows:
#     st.warning("No processed news messages found yet.")
#     st.stop()

# df = pd.DataFrame(rows)

# st.metric("Total Processed Articles", len(df))

# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("Source Distribution")
#     source_counts = df["source"].value_counts()
#     st.bar_chart(source_counts)

# with col2:
#     st.subheader("Languages")
#     lang_counts = df["language"].value_counts()
#     st.bar_chart(lang_counts)

# st.subheader("🔥 Trending Topics")

# texts = df["cleaned_title"].dropna().astype(str).tolist()
# topics = []

# if len(texts) >= 5:
#     vectorizer = CountVectorizer(stop_words="english")
#     X = vectorizer.fit_transform(texts)

#     lda = LatentDirichletAllocation(n_components=3, random_state=42)
#     lda.fit(X)

#     words = vectorizer.get_feature_names_out()

#     for topic in lda.components_:
#         top_words = [words[i] for i in topic.argsort()[-5:]]
#         topics.append(", ".join(top_words))

# for i, topic in enumerate(topics):
#     st.write(f"**Topic {i+1}:** {topic}")

# st.subheader("Latest Processed News")
# st.dataframe(
#     df[["source", "title", "cleaned_title", "scraped_at", "processed_at"]],
#     use_container_width=True
# )

# st.subheader("Top Frequent Words")

# all_text = " ".join(df["cleaned_title"].dropna().astype(str).tolist()).lower()
# words = re.findall(r"\b[a-zA-Z]+\b", all_text)

# stopwords = {
#     "the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or",
#     "is", "are", "with", "from", "this", "that", "as", "by", "his", "her",
#     "its", "be", "after", "amid", "over", "into"
# }

# filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
# word_counts = Counter(filtered_words).most_common(15)

# word_df = pd.DataFrame(word_counts, columns=["word", "count"]).set_index("word")
# st.bar_chart(word_df)

# st.subheader("Raw Data Preview")
# st.json(rows[:5])

# st.markdown("---")
# st.caption("Built using Kafka, Node.js, Python, and Machine Learning")


import json
import re
from collections import Counter

import pandas as pd
import streamlit as st
from kafka import KafkaConsumer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "processed-news"

st.set_page_config(
    page_title="Nepal Pulse Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {
    background-color: #f7f8fa;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
.header-box {
    background: white;
    padding: 24px 28px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    margin-bottom: 24px;
}
.header-title {
    font-size: 34px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 6px;
}
.header-subtitle {
    font-size: 16px;
    color: #6b7280;
}
.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.metric-label {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: #111827;
}
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-top: 10px;
    margin-bottom: 12px;
}
.topic-box {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 16px 18px;
    border-radius: 14px;
    margin-bottom: 12px;
}
.topic-title {
    font-size: 15px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 6px;
}
.topic-text {
    font-size: 15px;
    color: #374151;
}
.footer {
    color: #6b7280;
    font-size: 13px;
    text-align: center;
    padding-top: 20px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=10)
def load_messages():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=3000,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    rows = []
    for message in consumer:
        rows.append(message.value)

    return rows


def get_topics(texts, number_of_topics=3):
    if len(texts) < 5:
        return []

    vectorizer = CountVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=number_of_topics,
        random_state=42
    )
    lda.fit(matrix)

    words = vectorizer.get_feature_names_out()
    topics = []

    for topic in lda.components_:
        top_words = [words[i] for i in topic.argsort()[-6:]]
        topics.append(", ".join(reversed(top_words)))

    return topics


def get_word_frequency(texts):
    all_text = " ".join(texts).lower()
    words = re.findall(r"\b[a-zA-Z]+\b", all_text)

    stopwords = {
        "the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or",
        "is", "are", "with", "from", "this", "that", "as", "by", "his", "her",
        "its", "be", "after", "amid", "over", "into", "has", "have", "was",
        "were", "will", "new", "not"
    }

    filtered = [word for word in words if word not in stopwords and len(word) > 2]
    return Counter(filtered).most_common(15)


rows = load_messages()

st.markdown("""
<div class="header-box">
    <div class="header-title">Nepal Pulse Dashboard</div>
    <div class="header-subtitle">
        Real-time news monitoring, topic discovery, and source-level insights for Nepali news streams.
    </div>
</div>
""", unsafe_allow_html=True)

if not rows:
    st.warning("No processed news found yet. Please start Kafka, run the processor, and then run the scraper.")
    st.stop()

df = pd.DataFrame(rows)

if "processed_at" in df.columns:
    df["processed_at"] = pd.to_datetime(df["processed_at"], errors="coerce")

if "scraped_at" in df.columns:
    df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")

with st.sidebar:
    st.title("Filters")

    sources = sorted(df["source"].dropna().unique().tolist())
    selected_sources = st.multiselect(
        "Select news sources",
        options=sources,
        default=sources
    )

    languages = sorted(df["language"].dropna().unique().tolist())
    selected_languages = st.multiselect(
        "Select languages",
        options=languages,
        default=languages
    )

    st.markdown("---")
    st.caption("Refresh the browser after running the scraper again.")

filtered_df = df[
    df["source"].isin(selected_sources) &
    df["language"].isin(selected_languages)
].copy()

texts = filtered_df["cleaned_title"].dropna().astype(str).tolist()

total_articles = len(filtered_df)
total_sources = filtered_df["source"].nunique()
total_languages = filtered_df["language"].nunique()
latest_time = (
    filtered_df["processed_at"].max().strftime("%Y-%m-%d %H:%M:%S")
    if "processed_at" in filtered_df.columns and pd.notna(filtered_df["processed_at"].max())
    else "N/A"
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Processed Articles</div>
        <div class="metric-value">{total_articles}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Active Sources</div>
        <div class="metric-value">{total_sources}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Languages</div>
        <div class="metric-value">{total_languages}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Last Processed</div>
        <div style="font-size:16px;font-weight:700;color:#111827;">{latest_time}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

left_col, right_col = st.columns([1.1, 1])

with left_col:
    st.markdown('<div class="section-title">Source Distribution</div>', unsafe_allow_html=True)
    source_counts = filtered_df["source"].value_counts()
    st.bar_chart(source_counts, use_container_width=True)

with right_col:
    st.markdown('<div class="section-title">Language Distribution</div>', unsafe_allow_html=True)
    language_counts = filtered_df["language"].value_counts()
    st.bar_chart(language_counts, use_container_width=True)

st.markdown('<div class="section-title">Trending Topics</div>', unsafe_allow_html=True)

topics = get_topics(texts)

if topics:
    topic_cols = st.columns(3)
    for index, topic in enumerate(topics):
        with topic_cols[index % 3]:
            st.markdown(f"""
            <div class="topic-box">
                <div class="topic-title">Topic {index + 1}</div>
                <div class="topic-text">{topic}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Not enough processed articles to generate topics yet.")

st.markdown('<div class="section-title">Top Frequent Words</div>', unsafe_allow_html=True)

word_counts = get_word_frequency(texts)

if word_counts:
    word_df = pd.DataFrame(word_counts, columns=["Word", "Count"]).set_index("Word")
    st.bar_chart(word_df, use_container_width=True)
else:
    st.info("No word frequency data available.")

st.markdown('<div class="section-title">Latest Processed News</div>', unsafe_allow_html=True)

display_columns = [
    "source",
    "language",
    "title",
    "cleaned_title",
    "url",
    "processed_at"
]

available_columns = [col for col in display_columns if col in filtered_df.columns]

st.dataframe(
    filtered_df[available_columns].sort_values(
        by="processed_at",
        ascending=False,
        na_position="last"
    ) if "processed_at" in filtered_df.columns else filtered_df[available_columns],
    use_container_width=True,
    hide_index=True
)

with st.expander("View Raw Processed JSON"):
    st.json(filtered_df.head(10).to_dict(orient="records"))

st.markdown("""
<div class="footer">
    Nepal Pulse — Built with Kafka, Node.js, Python, Machine Learning, and Streamlit.
</div>
""", unsafe_allow_html=True)