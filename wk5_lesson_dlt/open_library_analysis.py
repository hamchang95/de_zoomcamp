# %% [markdown]
# # Open Library Data Analysis
# 
# This notebook analyzes Harry Potter books from the Open Library pipeline.
# 
# Based on: https://dlthub.com/docs/general-usage/dataset-access/marimo

# %% [markdown]
# ## Setup
# Import required libraries and connect to the dlt dataset

# %%
import marimo as mo
import dlt
import ibis
import pandas as pd
import plotly.express as px

# %%
# Connect to the dlt pipeline dataset
pipeline = dlt.pipeline("open_library_pipeline")
dataset = pipeline.dataset()

# Get ibis connection for querying
ibis_conn = dataset.ibis_connection()

# %% [markdown]
# ## 1. Bar Chart: Number of Books per Author

# %%
# Query to count books per author
# Authors are stored in the books__author_name child table
author_table = ibis_conn.table("books__author_name")

# Group by author name and count
author_counts = (
    author_table
    .group_by("value")
    .aggregate(count=author_table.count())
    .order_by(ibis.desc("count"))
    .limit(20)
)

# Execute and convert to pandas
author_counts_df = author_counts.to_pandas()
author_counts_df = author_counts_df.rename(columns={"value": "author_name"})

mo.md(f"### Top 20 Authors by Book Count\n\nFound {len(author_counts_df)} authors")

# %%
# Create bar chart
fig_bar = px.bar(
    author_counts_df,
    x="author_name",
    y="count",
    title="Number of Books per Author (Top 20)",
    labels={"author_name": "Author Name", "count": "Number of Books"},
    color="count",
    color_continuous_scale="Blues"
)
fig_bar.update_layout(
    xaxis_tickangle=-45,
    height=600,
    showlegend=False
)
fig_bar.update_xaxes(title_text="Author")
fig_bar.update_yaxes(title_text="Number of Books")

mo.output(fig_bar)

# %% [markdown]
# ## 2. Line Chart: Books Over Time

# %%
# Query books by publication year
# Use first_publish_year from the main books table
books_table = ibis_conn.table("books")

# Filter out null years and group by year
books_over_time = (
    books_table
    .filter(books_table.first_publish_year.isnull() == False)
    .group_by("first_publish_year")
    .aggregate(count=books_table.count())
    .order_by("first_publish_year")
)

# Execute and convert to pandas
books_over_time_df = books_over_time.to_pandas()
books_over_time_df = books_over_time_df.rename(columns={"first_publish_year": "year"})

mo.md(f"### Books Published Over Time\n\nFound {len(books_over_time_df)} years with publication data")

# %%
# Create line chart
fig_line = px.line(
    books_over_time_df,
    x="year",
    y="count",
    title="Number of Books Published Over Time",
    labels={"year": "Year", "count": "Number of Books"},
    markers=True
)
fig_line.update_layout(
    height=600,
    xaxis_title="Publication Year",
    yaxis_title="Number of Books"
)
fig_line.update_traces(line=dict(width=3), marker=dict(size=6))

mo.output(fig_line)

# %% [markdown]
# ## Summary Statistics

# %%
mo.md(f"""
### Summary

- **Total Authors**: {len(author_counts_df)} (showing top 20)
- **Total Years**: {len(books_over_time_df)}
- **Year Range**: {int(books_over_time_df['year'].min())} - {int(books_over_time_df['year'].max())}
- **Peak Year**: {int(books_over_time_df.loc[books_over_time_df['count'].idxmax(), 'year'])} ({int(books_over_time_df['count'].max())} books)
""")
