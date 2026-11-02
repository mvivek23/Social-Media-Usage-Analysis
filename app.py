
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Social Media Usage Analysis",
    page_icon="📱",
    layout="wide"
)

# -------------------------------
# LOAD DATASET
# -------------------------------

DATA_PATH = Path(__file__).parent / "data" / "social_media_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

try:
    data = load_data()
except FileNotFoundError:
    st.error("Dataset not found. Check the data folder.")
    st.stop()

# Basic data cleaning
data = data.drop_duplicates()
data = data.dropna()

# -------------------------------
# DASHBOARD TITLE
# -------------------------------

st.title("📱 Social Media Usage Analysis System")

st.markdown(
    "### An interactive Python-based data analysis dashboard"
)

st.write(
    "Analyze social media usage patterns, platform preferences, "
    "sleep duration and productivity."
)

st.divider()

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------

st.sidebar.title("Dashboard Filters")

platforms = sorted(data["Platform"].unique())

selected_platforms = st.sidebar.multiselect(
    "Select Social Media Platforms",
    platforms,
    default=platforms
)

filtered_data = data[
    data["Platform"].isin(selected_platforms)
]

if filtered_data.empty:
    st.warning("Please select at least one platform.")
    st.stop()

# -------------------------------
# SUMMARY STATISTICS
# -------------------------------

st.subheader("📊 Overall Usage Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Users",
    len(filtered_data)
)

col2.metric(
    "Average Daily Usage",
    f"{filtered_data['Daily_Usage_Minutes'].mean():.1f} min"
)

col3.metric(
    "Average Sleep",
    f"{filtered_data['Sleep_Hours'].mean():.1f} hrs"
)

col4.metric(
    "Average Productivity",
    f"{filtered_data['Productivity_Score'].mean():.1f}/10"
)

st.divider()

# -------------------------------
# PLATFORM USAGE BAR CHART
# -------------------------------

st.subheader("📈 Average Usage by Platform")

platform_usage = (
    filtered_data.groupby("Platform")["Daily_Usage_Minutes"]
    .mean()
    .sort_values(ascending=False)
)

fig1, ax1 = plt.subplots(figsize=(9, 5))

sns.barplot(
    x=platform_usage.index,
    y=platform_usage.values,
    ax=ax1
)

ax1.set_title("Average Daily Usage by Platform")
ax1.set_xlabel("Social Media Platform")
ax1.set_ylabel("Usage in Minutes")

plt.xticks(rotation=15)
plt.tight_layout()

st.pyplot(fig1)
plt.close(fig1)

st.divider()

# -------------------------------
# PLATFORM DISTRIBUTION
# -------------------------------

st.subheader("🥧 Platform Distribution")

col5, col6 = st.columns(2)

with col5:
    platform_count = filtered_data["Platform"].value_counts()

    fig2, ax2 = plt.subplots(figsize=(7, 6))

    ax2.pie(
        platform_count.values,
        labels=platform_count.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax2.set_title("Platform Distribution")

    st.pyplot(fig2)
    plt.close(fig2)

with col6:
    st.write("**Platform-wise User Records**")

    st.dataframe(
        platform_count.rename("Number of Users"),
        use_container_width=True
    )

# -------------------------------
# USAGE VS SLEEP ANALYSIS
# -------------------------------

st.divider()

st.subheader("😴 Social Media Usage vs Sleep")

fig3, ax3 = plt.subplots(figsize=(9, 5))

sns.scatterplot(
    data=filtered_data,
    x="Daily_Usage_Minutes",
    y="Sleep_Hours",
    hue="Platform",
    s=100,
    ax=ax3
)

ax3.set_title("Daily Usage and Sleep Duration")
ax3.set_xlabel("Daily Usage (Minutes)")
ax3.set_ylabel("Sleep Duration (Hours)")

plt.tight_layout()

st.pyplot(fig3)
plt.close(fig3)

# -------------------------------
# PRODUCTIVITY ANALYSIS
# -------------------------------

st.divider()

st.subheader("💻 Productivity Analysis")

productivity = (
    filtered_data.groupby("Platform")["Productivity_Score"]
    .mean()
    .sort_values(ascending=False)
)

fig4, ax4 = plt.subplots(figsize=(9, 5))

sns.barplot(
    x=productivity.index,
    y=productivity.values,
    ax=ax4
)

ax4.set_title("Average Productivity by Platform")
ax4.set_xlabel("Platform")
ax4.set_ylabel("Productivity Score")

plt.tight_layout()

st.pyplot(fig4)
plt.close(fig4)

# -------------------------------
# AUTOMATED INSIGHTS
# -------------------------------

st.divider()

st.subheader("💡 Automated Insights")

highest_usage_platform = platform_usage.idxmax()
lowest_usage_platform = platform_usage.idxmin()

highest_usage = platform_usage.max()
lowest_usage = platform_usage.min()

st.write(
    f"1. **{highest_usage_platform}** has the highest "
    f"average daily usage at {highest_usage:.2f} minutes."
)

st.write(
    f"2. **{lowest_usage_platform}** has the lowest "
    f"average daily usage at {lowest_usage:.2f} minutes."
)

correlation = filtered_data[
    ["Daily_Usage_Minutes", "Sleep_Hours"]
].corr().iloc[0, 1]

st.write(
    f"3. Correlation between daily usage and sleep: "
    f"**{correlation:.2f}**."
)

st.caption(
    "Correlation describes an association in this sample; "
    "it does not establish cause and effect."
)

# -------------------------------
# DATASET TABLE
# -------------------------------

st.divider()

st.subheader("📋 Dataset Records")

st.dataframe(
    filtered_data,
    use_container_width=True
)

# -------------------------------
# DOWNLOAD DATASET
# -------------------------------

csv_data = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="social_media_analysis.csv",
    mime="text/csv"
)

# -------------------------------
# FOOTER
# -------------------------------

st.divider()

st.markdown(
    "### Social Media Usage Analysis System"
)

st.caption(
    "Developed using Python, Pandas, Matplotlib, "
    "Seaborn and Streamlit | BCA Minor Project"
)
