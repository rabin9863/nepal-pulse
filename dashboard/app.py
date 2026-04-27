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


# import json
# import re
# from collections import Counter

# import pandas as pd
# import streamlit as st
# from kafka import KafkaConsumer
# from sklearn.decomposition import LatentDirichletAllocation
# from sklearn.feature_extraction.text import CountVectorizer

# BOOTSTRAP_SERVERS = "localhost:9092"
# TOPIC = "processed-news"

# st.set_page_config(
#     page_title="Nepal Pulse Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.markdown("""
# <style>
# .main {
#     background-color: #f7f8fa;
# }
# .block-container {
#     padding-top: 2rem;
#     padding-bottom: 2rem;
# }
# .header-box {
#     background: white;
#     padding: 24px 28px;
#     border-radius: 16px;
#     border: 1px solid #e5e7eb;
#     margin-bottom: 24px;
# }
# .header-title {
#     font-size: 34px;
#     font-weight: 700;
#     color: #111827;
#     margin-bottom: 6px;
# }
# .header-subtitle {
#     font-size: 16px;
#     color: #6b7280;
# }
# .card {
#     background: white;
#     padding: 22px;
#     border-radius: 16px;
#     border: 1px solid #e5e7eb;
#     box-shadow: 0 1px 3px rgba(0,0,0,0.04);
# }
# .metric-label {
#     font-size: 14px;
#     color: #6b7280;
#     margin-bottom: 8px;
# }
# .metric-value {
#     font-size: 30px;
#     font-weight: 700;
#     color: #111827;
# }
# .section-title {
#     font-size: 22px;
#     font-weight: 700;
#     color: #111827;
#     margin-top: 10px;
#     margin-bottom: 12px;
# }
# .topic-box {
#     background: #ffffff;
#     border: 1px solid #e5e7eb;
#     padding: 16px 18px;
#     border-radius: 14px;
#     margin-bottom: 12px;
# }
# .topic-title {
#     font-size: 15px;
#     font-weight: 700;
#     color: #111827;
#     margin-bottom: 6px;
# }
# .topic-text {
#     font-size: 15px;
#     color: #374151;
# }
# .footer {
#     color: #6b7280;
#     font-size: 13px;
#     text-align: center;
#     padding-top: 20px;
# }
# </style>
# """, unsafe_allow_html=True)


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


# def get_topics(texts, number_of_topics=3):
#     if len(texts) < 5:
#         return []

#     vectorizer = CountVectorizer(stop_words="english")
#     matrix = vectorizer.fit_transform(texts)

#     lda = LatentDirichletAllocation(
#         n_components=number_of_topics,
#         random_state=42
#     )
#     lda.fit(matrix)

#     words = vectorizer.get_feature_names_out()
#     topics = []

#     for topic in lda.components_:
#         top_words = [words[i] for i in topic.argsort()[-6:]]
#         topics.append(", ".join(reversed(top_words)))

#     return topics


# def get_word_frequency(texts):
#     all_text = " ".join(texts).lower()
#     words = re.findall(r"\b[a-zA-Z]+\b", all_text)

#     stopwords = {
#         "the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or",
#         "is", "are", "with", "from", "this", "that", "as", "by", "his", "her",
#         "its", "be", "after", "amid", "over", "into", "has", "have", "was",
#         "were", "will", "new", "not"
#     }

#     filtered = [word for word in words if word not in stopwords and len(word) > 2]
#     return Counter(filtered).most_common(15)


# rows = load_messages()

# st.markdown("""
# <div class="header-box">
#     <div class="header-title">Nepal Pulse Dashboard</div>
#     <div class="header-subtitle">
#         Real-time news monitoring, topic discovery, and source-level insights for Nepali news streams.
#     </div>
# </div>
# """, unsafe_allow_html=True)

# if not rows:
#     st.warning("No processed news found yet. Please start Kafka, run the processor, and then run the scraper.")
#     st.stop()

# df = pd.DataFrame(rows)

# if "processed_at" in df.columns:
#     df["processed_at"] = pd.to_datetime(df["processed_at"], errors="coerce")

# if "scraped_at" in df.columns:
#     df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")

# with st.sidebar:
#     st.title("Filters")

#     sources = sorted(df["source"].dropna().unique().tolist())
#     selected_sources = st.multiselect(
#         "Select news sources",
#         options=sources,
#         default=sources
#     )

#     languages = sorted(df["language"].dropna().unique().tolist())
#     selected_languages = st.multiselect(
#         "Select languages",
#         options=languages,
#         default=languages
#     )

#     st.markdown("---")
#     st.caption("Refresh the browser after running the scraper again.")

# filtered_df = df[
#     df["source"].isin(selected_sources) &
#     df["language"].isin(selected_languages)
# ].copy()

# texts = filtered_df["cleaned_title"].dropna().astype(str).tolist()

# total_articles = len(filtered_df)
# total_sources = filtered_df["source"].nunique()
# total_languages = filtered_df["language"].nunique()
# latest_time = (
#     filtered_df["processed_at"].max().strftime("%Y-%m-%d %H:%M:%S")
#     if "processed_at" in filtered_df.columns and pd.notna(filtered_df["processed_at"].max())
#     else "N/A"
# )

# kpi1, kpi2, kpi3, kpi4 = st.columns(4)

# with kpi1:
#     st.markdown(f"""
#     <div class="card">
#         <div class="metric-label">Processed Articles</div>
#         <div class="metric-value">{total_articles}</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi2:
#     st.markdown(f"""
#     <div class="card">
#         <div class="metric-label">Active Sources</div>
#         <div class="metric-value">{total_sources}</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi3:
#     st.markdown(f"""
#     <div class="card">
#         <div class="metric-label">Languages</div>
#         <div class="metric-value">{total_languages}</div>
#     </div>
#     """, unsafe_allow_html=True)

# with kpi4:
#     st.markdown(f"""
#     <div class="card">
#         <div class="metric-label">Last Processed</div>
#         <div style="font-size:16px;font-weight:700;color:#111827;">{latest_time}</div>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)

# left_col, right_col = st.columns([1.1, 1])

# with left_col:
#     st.markdown('<div class="section-title">Source Distribution</div>', unsafe_allow_html=True)
#     source_counts = filtered_df["source"].value_counts()
#     st.bar_chart(source_counts, use_container_width=True)

# with right_col:
#     st.markdown('<div class="section-title">Language Distribution</div>', unsafe_allow_html=True)
#     language_counts = filtered_df["language"].value_counts()
#     st.bar_chart(language_counts, use_container_width=True)

# st.markdown('<div class="section-title">Trending Topics</div>', unsafe_allow_html=True)

# topics = get_topics(texts)

# if topics:
#     topic_cols = st.columns(3)
#     for index, topic in enumerate(topics):
#         with topic_cols[index % 3]:
#             st.markdown(f"""
#             <div class="topic-box">
#                 <div class="topic-title">Topic {index + 1}</div>
#                 <div class="topic-text">{topic}</div>
#             </div>
#             """, unsafe_allow_html=True)
# else:
#     st.info("Not enough processed articles to generate topics yet.")

# st.markdown('<div class="section-title">Top Frequent Words</div>', unsafe_allow_html=True)

# word_counts = get_word_frequency(texts)

# if word_counts:
#     word_df = pd.DataFrame(word_counts, columns=["Word", "Count"]).set_index("Word")
#     st.bar_chart(word_df, use_container_width=True)
# else:
#     st.info("No word frequency data available.")

# st.markdown('<div class="section-title">Latest Processed News</div>', unsafe_allow_html=True)

# display_columns = [
#     "source",
#     "language",
#     "title",
#     "cleaned_title",
#     "url",
#     "processed_at"
# ]

# available_columns = [col for col in display_columns if col in filtered_df.columns]

# st.dataframe(
#     filtered_df[available_columns].sort_values(
#         by="processed_at",
#         ascending=False,
#         na_position="last"
#     ) if "processed_at" in filtered_df.columns else filtered_df[available_columns],
#     use_container_width=True,
#     hide_index=True
# )

# with st.expander("View Raw Processed JSON"):
#     st.json(filtered_df.head(10).to_dict(orient="records"))

# st.markdown("""
# <div class="footer">
#     Nepal Pulse — Built with Kafka, Node.js, Python, Machine Learning, and Streamlit.
# </div>
# """, unsafe_allow_html=True)
import json
import re
from collections import Counter

import pandas as pd
import streamlit as st
from kafka import KafkaConsumer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

BOOTSTRAP_SERVERS = "kafka:29092"
TOPIC = "processed-news"

st.set_page_config(
    page_title="Nepal Pulse Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #fff7ed 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border-right: 1px solid #e5e7eb;
}

[data-testid="stSidebar"] h1 {
    color: #0f172a;
    font-size: 25px;
    font-weight: 850;
}

.sidebar-box {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 16px;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
}

.sidebar-title {
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 4px;
}

.sidebar-text {
    font-size: 13px;
    color: #64748b;
    line-height: 1.5;
}

.header-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 52%, #9a3412 100%);
    padding: 36px 38px;
    border-radius: 28px;
    border: 1px solid rgba(255,255,255,0.16);
    margin-bottom: 24px;
    box-shadow: 0 24px 60px rgba(15, 23, 42, 0.22);
}

.header-kicker {
    color: #fde68a;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    margin-bottom: 11px;
}

.header-title {
    font-size: 44px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 10px;
    line-height: 1.1;
}

.header-subtitle {
    font-size: 16px;
    color: #dbeafe;
    max-width: 940px;
    line-height: 1.65;
}

.header-authors {
    margin-top: 20px;
    display: inline-block;
    background: rgba(255,255,255,0.14);
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.20);
}

.card {
    background: rgba(255,255,255,0.96);
    padding: 22px;
    border-radius: 22px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
    min-height: 124px;
}

.card-accent-blue { border-top: 5px solid #2563eb; }
.card-accent-green { border-top: 5px solid #059669; }
.card-accent-orange { border-top: 5px solid #ea580c; }
.card-accent-purple { border-top: 5px solid #7c3aed; }

.metric-label {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 8px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.metric-value {
    font-size: 36px;
    font-weight: 900;
    color: #0f172a;
    line-height: 1.1;
}

.metric-note {
    color: #64748b;
    font-size: 13px;
    margin-top: 8px;
}

.panel {
    background: rgba(255,255,255,0.96);
    border-radius: 24px;
    border: 1px solid #e5e7eb;
    padding: 24px 26px;
    box-shadow: 0 14px 32px rgba(15, 23, 42, 0.07);
    margin-bottom: 24px;
}

.section-title {
    font-size: 24px;
    font-weight: 900;
    color: #0f172a;
    margin-bottom: 5px;
}

.section-subtitle {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 16px;
    line-height: 1.6;
}

.now-card {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e5e7eb;
    border-left: 5px solid #2563eb;
    padding: 15px 16px;
    border-radius: 16px;
    margin-bottom: 10px;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.05);
}

.now-title {
    font-size: 15px;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.45;
}

.now-meta {
    font-size: 12px;
    color: #64748b;
    margin-top: 7px;
}

.source-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 12px 14px;
    border-radius: 14px;
    margin-bottom: 8px;
}

.source-name {
    font-size: 14px;
    color: #0f172a;
    font-weight: 750;
}

.source-count {
    font-size: 13px;
    color: #1e3a8a;
    font-weight: 850;
    background: #dbeafe;
    padding: 5px 10px;
    border-radius: 999px;
}

.keyword-pill {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    padding: 7px 11px;
    border-radius: 999px;
    margin: 4px 5px 4px 0;
    font-size: 13px;
    font-weight: 750;
}

.topic-box {
    background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 20px;
    margin-bottom: 12px;
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.06);
    min-height: 124px;
}

.topic-box-one { border-top: 5px solid #2563eb; }
.topic-box-two { border-top: 5px solid #ea580c; }
.topic-box-three { border-top: 5px solid #059669; }

.topic-title {
    font-size: 14px;
    font-weight: 900;
    color: #111827;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.topic-text {
    font-size: 16px;
    color: #334155;
    line-height: 1.55;
    font-weight: 600;
}

.news-note {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1e3a8a;
    padding: 12px 14px;
    border-radius: 14px;
    font-size: 14px;
    margin-bottom: 14px;
}

.footer {
    color: #475569;
    font-size: 13px;
    text-align: center;
    padding: 24px 0 6px 0;
}

div[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}

.stTextInput > div > div > input {
    border-radius: 14px;
}

.stMultiSelect > div > div {
    border-radius: 14px;
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
        "were", "will", "new", "not", "about", "than", "their", "they",
        "them", "also", "more", "less", "can", "could"
    }

    filtered = [word for word in words if word not in stopwords and len(word) > 2]
    return Counter(filtered).most_common(15)


rows = load_messages()

st.markdown("""
<div class="header-box">
    <div class="header-kicker">Knowledge Discovery and Data Science Project</div>
    <div class="header-title">Nepal Pulse Dashboard</div>
    <div class="header-subtitle">
        A real-time news intelligence dashboard for monitoring what is happening in Nepal,
        discovering trending topics, and comparing news activity across multiple sources.
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
    st.title("Dashboard Controls")

    st.markdown("""
    <div class="sidebar-box">
        <div class="sidebar-title">Filter the News Feed</div>
        <div class="sidebar-text">
            Select sources, choose language, and search headlines to focus on the news records you want to analyze.
        </div>
    </div>
    """, unsafe_allow_html=True)

    sources = sorted(df["source"].dropna().unique().tolist())
    selected_sources = st.multiselect(
        "News sources",
        options=sources,
        default=sources,
        help="Choose one or more news websites to include in the dashboard."
    )

    languages = sorted(df["language"].dropna().unique().tolist())
    selected_languages = st.multiselect(
        "Languages",
        options=languages,
        default=languages,
        help="Filter articles by language."
    )

    search_query = st.text_input(
        "Search headlines",
        placeholder="Example: Nepal, minister, cricket",
        help="Search inside original and cleaned headlines."
    )

    st.markdown("---")

    st.markdown("""
    <div class="sidebar-box">
        <div class="sidebar-title">System Information</div>
        <div class="sidebar-text">
            Kafka topic: processed-news<br>
            Dashboard cache: 10 seconds<br>
            Run scraper again to load fresh records.
        </div>
    </div>
    """, unsafe_allow_html=True)

filtered_df = df[
    df["source"].isin(selected_sources) &
    df["language"].isin(selected_languages)
].copy()

if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].fillna("").str.contains(search_query, case=False, regex=False) |
        filtered_df["cleaned_title"].fillna("").str.contains(search_query, case=False, regex=False)
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
    <div class="card card-accent-blue">
        <div class="metric-label">Processed Articles</div>
        <div class="metric-value">{total_articles}</div>
        <div class="metric-note">Records after current filters</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="card card-accent-green">
        <div class="metric-label">Active Sources</div>
        <div class="metric-value">{total_sources}</div>
        <div class="metric-note">Unique news portals in view</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="card card-accent-orange">
        <div class="metric-label">Languages</div>
        <div class="metric-value">{total_languages}</div>
        <div class="metric-note">Language categories detected</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="card card-accent-purple">
        <div class="metric-label">Last Processed</div>
        <div style="font-size:16px;font-weight:850;color:#0f172a;line-height:1.4;">{latest_time}</div>
        <div class="metric-note">Most recent processed record</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# What's happening right now
st.markdown("""
<div class="panel">
    <div class="section-title">What Is Happening Right Now in Nepal</div>
    <div class="section-subtitle">
        A quick view of the latest headlines, active keywords, and most active sources across the processed news stream.
    </div>
</div>
""", unsafe_allow_html=True)

now_left, now_mid, now_right = st.columns([1.35, 1, 0.9])

with now_left:
    st.markdown("""
    <div class="panel">
        <div class="section-title">Latest Headlines</div>
        <div class="section-subtitle">Most recent processed articles from the selected sources.</div>
    """, unsafe_allow_html=True)

    if "processed_at" in filtered_df.columns:
        latest_news = filtered_df.sort_values(
            by="processed_at",
            ascending=False,
            na_position="last"
        ).head(6)
    else:
        latest_news = filtered_df.head(6)

    for _, row in latest_news.iterrows():
        processed_value = row.get("processed_at", "")
        processed_display = (
            processed_value.strftime("%Y-%m-%d %H:%M:%S")
            if pd.notna(processed_value) and hasattr(processed_value, "strftime")
            else str(processed_value)
        )

        st.markdown(f"""
        <div class="now-card">
            <div class="now-title">{row.get("title", "Untitled")}</div>
            <div class="now-meta">{row.get("source", "Unknown source")} | {processed_display}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with now_mid:
    st.markdown("""
    <div class="panel">
        <div class="section-title">Trending Keywords</div>
        <div class="section-subtitle">Common terms appearing in current headlines.</div>
    """, unsafe_allow_html=True)

    current_keywords = get_word_frequency(texts)[:10]

    if current_keywords:
        pills_html = ""
        for word, count in current_keywords:
            pills_html += f'<span class="keyword-pill">{word} ({count})</span>'
        st.markdown(pills_html, unsafe_allow_html=True)
    else:
        st.info("No keyword data available.")

    st.markdown("</div>", unsafe_allow_html=True)

with now_right:
    st.markdown("""
    <div class="panel">
        <div class="section-title">Most Active Sources</div>
        <div class="section-subtitle">Sources publishing the most records.</div>
    """, unsafe_allow_html=True)

    top_sources = filtered_df["source"].value_counts().head(5)

    if not top_sources.empty:
        for source, count in top_sources.items():
            st.markdown(f"""
            <div class="source-row">
                <span class="source-name">{source}</span>
                <span class="source-count">{count}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No source data available.")

    st.markdown("</div>", unsafe_allow_html=True)

left_col, right_col = st.columns([1.15, 1])

with left_col:
    st.markdown("""
    <div class="panel">
        <div class="section-title">Source Distribution</div>
        <div class="section-subtitle">Comparison of article volume by news portal.</div>
    """, unsafe_allow_html=True)

    source_counts = filtered_df["source"].value_counts()
    st.bar_chart(source_counts, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("""
    <div class="panel">
        <div class="section-title">Language Distribution</div>
        <div class="section-subtitle">Breakdown of processed records by language.</div>
    """, unsafe_allow_html=True)

    language_counts = filtered_df["language"].value_counts()
    st.bar_chart(language_counts, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="panel">
    <div class="section-title">Trending Topics</div>
    <div class="section-subtitle">
        Topic keywords are generated from cleaned headlines using LDA topic modeling.
    </div>
</div>
""", unsafe_allow_html=True)

topics = get_topics(texts)

if topics:
    topic_cols = st.columns(3)
    topic_classes = ["topic-box-one", "topic-box-two", "topic-box-three"]

    for index, topic in enumerate(topics):
        with topic_cols[index % 3]:
            st.markdown(f"""
            <div class="topic-box {topic_classes[index % 3]}">
                <div class="topic-title">Topic {index + 1}</div>
                <div class="topic-text">{topic}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Not enough processed articles to generate topics yet.")

st.markdown("""
<div class="panel">
    <div class="section-title">Top Frequent Words</div>
    <div class="section-subtitle">
        Most common meaningful English words found in the processed headlines.
    </div>
""", unsafe_allow_html=True)

word_counts = get_word_frequency(texts)

if word_counts:
    word_df = pd.DataFrame(word_counts, columns=["Word", "Count"]).set_index("Word")
    st.bar_chart(word_df, use_container_width=True)
else:
    st.info("No word frequency data available.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="panel">
    <div class="section-title">Latest Processed News</div>
    <div class="section-subtitle">
        Cleaned and structured news records from the real-time processing pipeline.
    </div>
    <div class="news-note">
        Use the sidebar controls to filter by source, language, or headline keyword.
    </div>
</div>
""", unsafe_allow_html=True)

display_columns = [
    "source",
    "language",
    "title",
    "cleaned_title",
    "url",
    "processed_at"
]

available_columns = [col for col in display_columns if col in filtered_df.columns]

table_df = filtered_df[available_columns].copy()

if "processed_at" in table_df.columns:
    table_df = table_df.sort_values(
        by="processed_at",
        ascending=False,
        na_position="last"
    )

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True
)

with st.expander("View raw processed JSON"):
    st.json(filtered_df.head(10).to_dict(orient="records"))

st.markdown("""
<div class="footer">
    Nepal Pulse Dashboard — Developed by Rabin Dhakal and Asis Shrestha.
    Built with Kafka, Node.js, Python, Machine Learning, and Streamlit.
</div>
""", unsafe_allow_html=True)