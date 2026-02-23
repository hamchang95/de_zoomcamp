import marimo

__generated_with = "0.20.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    mo.md("# Open Library Data Analysis\n\nThis notebook analyzes Harry Potter books from the Open Library pipeline.\n\nBased on: [dlt marimo docs](https://dlthub.com/docs/general-usage/dataset-access/marimo)")
    return (mo,)


@app.cell
def _():
    import dlt
    import ibis
    import plotly.express as px

    return dlt, ibis, px


@app.cell
def _(dlt):
    pipeline = dlt.pipeline("open_library_pipeline")
    dataset = pipeline.dataset()
    ibis_conn = dataset.ibis()
    return (ibis_conn,)


@app.cell
def _(mo):
    mo.md("""
    ## 1. Bar Chart: Number of Books per Author
    """)
    return


@app.cell
def _(ibis, ibis_conn, mo):
    # Bar Chart: Number of Books per Author
    author_table = ibis_conn.table("books__author_name")
    author_counts = (
        author_table
        .group_by("value")
        .aggregate(count=author_table.count())
        .order_by(ibis.desc("count"))
        .limit(20)
    )
    author_counts_df = author_counts.to_pandas()
    author_counts_df = author_counts_df.rename(columns={"value": "author_name"})
    mo.md(f"### Top 20 Authors by Book Count\n\nFound {len(author_counts_df)} authors")
    return (author_counts_df,)


@app.cell
def _(author_counts_df, px):
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
    fig_bar
    return


@app.cell
def _(mo):
    mo.md("""
    ## 2. Line Chart: Books Over Time
    """)
    return


@app.cell
def _(ibis_conn, mo):
    books_table = ibis_conn.table("books")
    books_over_time = (
        books_table
        .filter(books_table.first_publish_year.isnull() == False)
        .group_by("first_publish_year")
        .aggregate(count=books_table.count())
        .order_by("first_publish_year")
    )
    books_over_time_df = books_over_time.to_pandas()
    books_over_time_df = books_over_time_df.rename(columns={"first_publish_year": "year"})
    mo.md(f"### Books Published Over Time\n\nFound {len(books_over_time_df)} years with publication data")
    return (books_over_time_df,)


@app.cell
def _(books_over_time_df, px):
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
    fig_line
    return


@app.cell
def _(author_counts_df, books_over_time_df, mo):
    # Summary Statistics
    mo.md(f"""
    ### Summary

    - **Total Authors**: {len(author_counts_df)} (showing top 20)
    - **Total Years**: {len(books_over_time_df)}
    - **Year Range**: {int(books_over_time_df['year'].min())} - {int(books_over_time_df['year'].max())}
    - **Peak Year**: {int(books_over_time_df.loc[books_over_time_df['count'].idxmax(), 'year'])} ({int(books_over_time_df['count'].max())} books)
    """)
    return


if __name__ == "__main__":
    app.run()
