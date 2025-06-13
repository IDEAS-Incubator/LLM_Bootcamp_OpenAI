from openai import OpenAI
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=my_key)

# Create a SQL database connection (SQLite for this example)
engine = create_engine("sqlite:///example.db")
connection = engine.connect()


# Example SQL table creation and data insertion (run once to set up)
def setup_database():
    connection.execute(
        text(
            """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            position TEXT,
            salary INTEGER,
            hire_date TEXT
        );
    """
        )
    )
    connection.execute(
        text(
            """
        INSERT INTO employees (name, position, salary, hire_date) VALUES
        ('Alice', 'Data Scientist', 120000, '2022-03-15'),
        ('Bob', 'Software Engineer', 100000, '2021-06-01'),
        ('Charlie', 'Product Manager', 95000, '2023-01-20');
    """
        )
    )


if __name__ == "__main__":
    # Uncomment to set up the database
    setup_database()

    # Query the SQL database
    query = "SELECT * FROM employees WHERE salary > 100000;"
    result = pd.read_sql_query(query, connection)

    # Convert query results to a readable format
    data_summary = result.to_string(index=False)

    # Use OpenAI API to analyze the query results
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes SQL query results.",
            },
            {
                "role": "user",
                "content": f"""
    The following is a table of employees earning more than $100,000:
    {data_summary}

    Provide a brief summary of the data, highlighting key insights.
    """,
            },
        ],
        max_tokens=100,
        temperature=0.7,
    )

    # Print results
    print("SQL Query Results:")
    print(result)
    print("\nOpenAI Summary:")
    print(response.choices[0].message.content.strip())

    # Close the database connection
    connection.close()
