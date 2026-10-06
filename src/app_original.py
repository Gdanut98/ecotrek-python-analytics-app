
# Import neccessary Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from wordcloud import WordCloud

# Page Configuration

st.set_page_config(page_title="EcoTrek Solutions Analysis", layout="wide")

# Title
st.markdown(
    "<h1 style='text-align: center;'>EcoTrek Solutions Analysis</h1>",
    unsafe_allow_html=True,
)

# Dictionary for temperature in °F

Temperature = {
    "January": 40, "February": 45, "March": 55, "April": 65, "May": 75,
    "June": 85, "July": 90, "August": 88, "September": 86, "October": 80,
    "November": 70, "December": 60
}

# Dictionary for GreenTote sales

GreenTote_Sales = {
    "January": 87500, "February": 100625, "March": 115725, "April": 132075,
    "May": 148875, "June": 164500, "July": 172725, "August": 185800,
    "September": 180900, "October": 170000, "November": 165000, "December": 160000
}

## Combine dictionaries into DataFrame

df = pd.DataFrame({"Sales": GreenTote_Sales, "Temperature": Temperature})

## Bring in charts from assigment 4

# Scatter plot
scatter = px.scatter(
    df,
    x="Sales",
    y="Temperature",
    color="Temperature",                 # gradient coloring by temperature
    size="Sales",                        # bubble size based on sales
    hover_data=df.columns,               # show all columns on hover
    trendline="ols",                     # add regression line
    color_continuous_scale="Viridis",    
    title="Sales vs Temperature"
)

# Update layout for better readability
scatter.update_layout(
    title=dict(x=0.5, font=dict(size=22)),    # center & enlarge title
    xaxis_title="Sales",
    yaxis_title="Temperature (°F)",
    plot_bgcolor="white",                     # clean background
    xaxis=dict(showgrid=True, gridcolor="lightgray"),
    yaxis=dict(showgrid=True, gridcolor="lightgray"),
)

# Improve marker styling
scatter.update_traces(
    marker=dict(line=dict(width=1, color="DarkSlateGrey")),
    opacity=0.8
)

# Read in customer review data from Assignment 3

df = pd.read_csv("Danut_George_sentiment.csv")

# Bar Chart
# Group by sentiment and count reviews
sentiment_counts = (df.groupby("sentiment")["Review"].count().reset_index().rename(columns={"Review": "Count"}))

# Add percentage column
total = sentiment_counts["Count"].sum()
sentiment_counts["Percent"] = (sentiment_counts["Count"] / total * 100).round(1)

# Create a combined text column for display
sentiment_counts["Label"] = sentiment_counts["Count"].astype(str) + " (" + sentiment_counts["Percent"].astype(str) + "%)"

# Plot horizontal bars
bar = px.bar(
    sentiment_counts,
    title = "Setiment Type Breakdown",
    x="Count",
    y="sentiment",
    orientation="h",
    color="sentiment",
    text="Label",
    color_discrete_map={"positive": "green", "neutral": "gray", "negative": "red"}
)

bar.update_traces(textposition="auto", textfont=dict(size=12))
bar.update_layout(width=750, height=320, margin=dict(l=140, r=120, t=70, b=50))
bar.update_layout(xaxis_title="Number of Reviews", yaxis_title="Sentiment")
bar.update_layout(title=dict(x=0.5, font=dict(size=22)))

# Word Cloud
# Combine all reviews into one string
text = " ".join(review for review in df["Review"].astype(str))


# Generate word cloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="viridis",   # nice color map
    max_words=100,        # top 100 words
    contour_color="steelblue",
    contour_width=2
).generate(text)

# Display
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Customer Reviews", fontsize=16)

# Description
st.markdown("""
    <p style='text-align: center; font-size:16px;'>
    Below is a summary analysis of GreenTote bag sales.<br>
    <strong>Figure 1</strong> shows correlation between Temperature and Sales.<br>
    <strong>Figure 2</strong> shows the breakdown of customer reviews.<br>
    <strong>Figure 3</strong> displays the most common words in reviews.
    </p>
""", unsafe_allow_html=True
)

# Layout
# --------------------------
st.subheader("Figure 1: Scatter Plot")
st.plotly_chart(scatter)

st.subheader("Figure 2: Bar Chart")
st.plotly_chart(bar)

st.subheader("Figure 3: Word Cloud")
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)
