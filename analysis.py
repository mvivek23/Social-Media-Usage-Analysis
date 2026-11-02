
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
data = pd.read_csv("data/social_media_data.csv")

# Display basic information
print("\nSOCIAL MEDIA USAGE ANALYSIS")
print("-" * 40)

print("\nTotal Users:", len(data))

print(
    "Average Daily Usage:",
    round(data["Daily_Usage_Minutes"].mean(), 2),
    "minutes"
)

print(
    "Average Sleep:",
    round(data["Sleep_Hours"].mean(), 2),
    "hours"
)

print(
    "Average Productivity Score:",
    round(data["Productivity_Score"].mean(), 2)
)

# Platform-wise average usage
platform_usage = data.groupby("Platform")["Daily_Usage_Minutes"].mean()

print("\nAverage Usage by Platform:")
print(platform_usage.round(2))

# Set the graph style
sns.set_theme(style="whitegrid")

# Graph 1: Average usage by platform
plt.figure(figsize=(9, 5))

sns.barplot(
    x=platform_usage.index,
    y=platform_usage.values
)

plt.title("Average Daily Social Media Usage by Platform")
plt.xlabel("Social Media Platform")
plt.ylabel("Average Usage (Minutes)")
plt.tight_layout()
plt.savefig("platform_usage.png")
plt.show()

# Graph 2: Platform distribution
plt.figure(figsize=(7, 7))

data["Platform"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Social Media Platform Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig("platform_distribution.png")
plt.show()

# Graph 3: Usage and sleep relationship
plt.figure(figsize=(9, 5))

sns.scatterplot(
    data=data,
    x="Daily_Usage_Minutes",
    y="Sleep_Hours",
    hue="Platform",
    s=100
)

plt.title("Social Media Usage vs Sleep Duration")
plt.xlabel("Daily Usage (Minutes)")
plt.ylabel("Sleep Duration (Hours)")
plt.tight_layout()
plt.savefig("usage_vs_sleep.png")
plt.show()

print("\nAnalysis completed successfully!")
print("Three graphs have been saved in the project folder.")
