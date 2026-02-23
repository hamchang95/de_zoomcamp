import duckdb

# Connect to the DuckDB file
con = duckdb.connect('taxi_pipeline.duckdb')

# Calculate total tips
total_tips = con.execute('SELECT SUM(tip_amt) FROM nyc_taxi_data_20260223012003.nyc_taxi_trips').fetchone()[0]

# Print the result
print(f'Total amount of money generated in tips: ${total_tips:.2f}')

# Close the connection
con.close()
