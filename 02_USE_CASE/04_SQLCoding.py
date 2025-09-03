from openai import OpenAI
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()
my_key = os.environ.get("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=my_key)

# Create a SQL database connection (SQLite for this example)
engine = create_engine("sqlite:///example.db")
connection = engine.connect()


def setup_database():
    """Set up the database with sample data"""
    try:
        # Create employees table
        connection.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                position TEXT,
                salary INTEGER,
                hire_date TEXT,
                department TEXT
            );
        """
            )
        )

        # Create departments table
        connection.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                budget INTEGER,
                location TEXT
            );
        """
            )
        )

        # Insert sample data
        connection.execute(
            text(
                """
            INSERT OR REPLACE INTO employees (id, name, position, salary, hire_date, department) VALUES
            (1, 'Alice Johnson', 'Data Scientist', 120000, '2022-03-15', 'Engineering'),
            (2, 'Bob Smith', 'Software Engineer', 100000, '2021-06-01', 'Engineering'),
            (3, 'Charlie Brown', 'Product Manager', 95000, '2023-01-20', 'Product'),
            (4, 'Diana Prince', 'UX Designer', 85000, '2022-08-10', 'Design'),
            (5, 'Eve Wilson', 'Data Engineer', 110000, '2021-12-05', 'Engineering'),
            (6, 'Frank Miller', 'Marketing Manager', 90000, '2023-02-14', 'Marketing');
        """
            )
        )

        connection.execute(
            text(
                """
            INSERT OR REPLACE INTO departments (id, name, budget, location) VALUES
            (1, 'Engineering', 500000, 'Floor 3'),
            (2, 'Product', 300000, 'Floor 2'),
            (3, 'Design', 200000, 'Floor 1'),
            (4, 'Marketing', 250000, 'Floor 4');
        """
            )
        )

        connection.commit()
        print("Database setup completed successfully!")

    except Exception as e:
        print(f" Error setting up database: {e}")


def get_database_schema():
    """Get database schema information for context"""
    try:
        # Get table names
        tables_query = text("SELECT name FROM sqlite_master WHERE type='table';")
        tables = connection.execute(tables_query).fetchall()

        schema_info = {}
        for table in tables:
            table_name = table[0]
            # Get column information
            columns_query = text(f"PRAGMA table_info({table_name});")
            columns = connection.execute(columns_query).fetchall()
            schema_info[table_name] = [col[1] for col in columns]

        return schema_info
    except Exception as e:
        print(f" Error getting schema: {e}")
        return {}


def query_sql_analysis(sql_query, query_results):
    """
    Analyze SQL query results using OpenAI
    """
    try:
        # Convert results to readable format
        if isinstance(query_results, pd.DataFrame):
            data_summary = query_results.to_string(index=False)
        else:
            data_summary = str(query_results)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a data analyst expert. Analyze SQL query results and provide insights, patterns, and recommendations.",
                },
                {
                    "role": "user",
                    "content": f"""
SQL Query: {sql_query}

Query Results:
{data_summary}

Please provide:
1. Summary of the data
2. Key insights and patterns
3. Recommendations based on the findings
4. Any potential data quality issues
""",
                },
            ],
            max_tokens=300,
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f" Error analyzing query results: {e}"


def text_to_sql_conversion(natural_language_query):
    """
    Convert natural language to SQL using OpenAI with tool calling
    """
    try:
        # Get database schema for context
        schema = get_database_schema()
        schema_context = "\n".join(
            [
                f"Table '{table}': {', '.join(columns)}"
                for table, columns in schema.items()
            ]
        )

        # Define tools for SQL generation
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "generate_sql_query",
                    "description": "Generate SQL query from natural language",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_query": {
                                "type": "string",
                                "description": "The generated SQL query using SQLite syntax",
                            },
                            "explanation": {
                                "type": "string",
                                "description": "Brief explanation of what the query does",
                            },
                            "confidence": {
                                "type": "number",
                                "description": "Confidence level in the generated query (0-1)",
                            },
                        },
                        "required": ["sql_query", "explanation", "confidence"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "validate_sql_query",
                    "description": "Validate if a SQL query is syntactically correct",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_query": {
                                "type": "string",
                                "description": "The SQL query to validate",
                            },
                            "is_valid": {
                                "type": "boolean",
                                "description": "Whether the query is syntactically valid",
                            },
                            "error_message": {
                                "type": "string",
                                "description": "Error message if query is invalid",
                            },
                        },
                        "required": ["sql_query", "is_valid"],
                    },
                },
            },
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a SQL expert. Convert natural language queries to SQL using the provided tools.

Database Schema:
{schema_context}

Rules:
- Use SQLite syntax
- Only use tables and columns that exist in the schema
- Use proper SQL formatting
- Always use the generate_sql_query function to create the SQL
- Validate the query using validate_sql_query function if needed""",
                },
                {
                    "role": "user",
                    "content": f"Convert this to SQL: {natural_language_query}",
                },
            ],
            tools=tools,
            tool_choice={
                "type": "function",
                "function": {"name": "generate_sql_query"},
            },
            max_tokens=500,
            temperature=0.1,
        )

        # Handle tool calls
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]

            if tool_call.function.name == "generate_sql_query":
                args = json.loads(tool_call.function.arguments)
                sql_query = args.get("sql_query", "")
                explanation = args.get("explanation", "")
                confidence = args.get("confidence", 0.0)

                # Clean up the SQL query
                sql_query = sql_query.strip()
                if sql_query.startswith("```sql"):
                    sql_query = sql_query[6:]
                if sql_query.endswith("```"):
                    sql_query = sql_query[:-3]

                # Validate the query
                validation_result = validate_generated_sql(sql_query)

                if validation_result["is_valid"]:
                    return {
                        "sql_query": sql_query.strip(),
                        "explanation": explanation,
                        "confidence": confidence,
                        "validation": validation_result,
                    }
                else:
                    # Try to fix the query
                    fixed_query = fix_sql_query(
                        sql_query, validation_result["error_message"]
                    )
                    return {
                        "sql_query": fixed_query,
                        "explanation": f"Fixed query: {explanation}",
                        "confidence": confidence * 0.8,
                        "validation": {"is_valid": True, "error_message": "Fixed"},
                    }

        return f" Error: No SQL query generated"

    except Exception as e:
        return f" Error converting to SQL: {e}"


def validate_generated_sql(sql_query):
    """
    Validate SQL query syntax
    """
    try:
        if not sql_query.strip():
            return {"is_valid": False, "error_message": "Empty query"}

        required_keywords = ["SELECT", "FROM"]
        query_upper = sql_query.upper()

        for keyword in required_keywords:
            if keyword not in query_upper:
                return {
                    "is_valid": False,
                    "error_message": f"Missing required keyword: {keyword}",
                }

        if sql_query.count("(") != sql_query.count(")"):
            return {"is_valid": False, "error_message": "Unbalanced parentheses"}

        if sql_query.count("'") % 2 != 0:
            return {"is_valid": False, "error_message": "Unbalanced quotes"}

        return {"is_valid": True, "error_message": None}

    except Exception as e:
        return {"is_valid": False, "error_message": str(e)}


def fix_sql_query(sql_query, error_message):
    """
    Attempt to fix common SQL errors
    """
    try:
        schema = get_database_schema()
        fixed_query = sql_query

        if "missing required keyword" in error_message.lower():
            if "SELECT" not in fixed_query.upper():
                fixed_query = f"SELECT * {fixed_query}"

        if fixed_query.endswith(";"):
            fixed_query = fixed_query[:-1]

        if not fixed_query.endswith(";"):
            fixed_query += ";"

        return fixed_query

    except Exception as e:
        return sql_query


def execute_sql_query(sql_query):
    """
    Execute SQL query and return results
    """
    try:
        result = pd.read_sql_query(sql_query, connection)
        return result
    except Exception as e:
        return f" Error executing SQL: {e}"


def interactive_sql_demo():
    """
    Interactive demo for both QuerySQL and CodingSQL
    """
    print("=" * 60)
    print("SQL Programming with OpenAI Demo")
    print("=" * 60)
    print("1. QuerySQL - Analyze existing SQL query results")
    print("2. CodingSQL - Convert natural language to SQL")
    print("3. Exit")
    print("=" * 60)

    while True:
        try:
            choice = input("\nChoose an option (1-3): ").strip()

            if choice == "1":
                # QuerySQL Demo
                print("\nQuerySQL Demo - Analyzing SQL Results")
                print("-" * 40)

                example_queries = [
                    "SELECT * FROM employees WHERE salary > 100000;",
                    "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department;",
                    "SELECT name, position, salary FROM employees ORDER BY salary DESC LIMIT 3;",
                ]

                for i, query in enumerate(example_queries, 1):
                    print(f"\nQuery {i}: {query}")
                    result = execute_sql_query(query)

                    if isinstance(result, pd.DataFrame):
                        print("\nResults:")
                        print(result)

                        analysis = query_sql_analysis(query, result)
                        print("\nAI Analysis:")
                        print(analysis)
                    else:
                        print(f"Error: {result}")

                    input("\nPress Enter to continue...")

            elif choice == "2":
                # CodingSQL Demo
                print("\nCodingSQL Demo - Natural Language to SQL")
                print("-" * 40)

                example_queries = [
                    "Show me all employees in the Engineering department",
                    "Find the average salary by department",
                    "List the top 3 highest paid employees",
                    "Count how many employees were hired in 2022",
                ]

                for i, nl_query in enumerate(example_queries, 1):
                    print(f"\nNatural Language Query {i}: {nl_query}")

                    sql_result = text_to_sql_conversion(nl_query)

                    if isinstance(sql_result, dict):
                        sql_query = sql_result["sql_query"]
                        explanation = sql_result["explanation"]
                        confidence = sql_result["confidence"]
                        validation = sql_result["validation"]

                        print(f"Generated SQL: {sql_query}")
                        print(f"Explanation: {explanation}")
                        print(f"Confidence: {confidence:.2f}")
                        print(
                            f"Validation: {'Valid' if validation['is_valid'] else 'Invalid'}"
                        )

                        if not validation["is_valid"]:
                            print(f"Error: {validation['error_message']}")
                    else:
                        print(f"Error: {sql_result}")
                        continue

                    result = execute_sql_query(sql_query)
                    if isinstance(result, pd.DataFrame):
                        print("\nResults:")
                        print(result)
                    else:
                        print(f"Error: {result}")

                    input("\nPress Enter to continue...")

                print("\nInteractive Mode - Try your own queries!")
                while True:
                    user_query = input(
                        "\nEnter your natural language query (or 'back' to return): "
                    ).strip()

                    if user_query.lower() == "back":
                        break

                    if user_query:
                        sql_result = text_to_sql_conversion(user_query)

                        if isinstance(sql_result, dict):
                            sql_query = sql_result["sql_query"]
                            explanation = sql_result["explanation"]
                            confidence = sql_result["confidence"]
                            validation = sql_result["validation"]

                            print(f"\nGenerated SQL: {sql_query}")
                            print(f"Explanation: {explanation}")
                            print(f"Confidence: {confidence:.2f}")
                            print(
                                f"Validation: {'Valid' if validation['is_valid'] else 'Invalid'}"
                            )

                            if not validation["is_valid"]:
                                print(f"Error: {validation['error_message']}")
                        else:
                            print(f"Error: {sql_result}")
                            continue

                        result = execute_sql_query(sql_query)
                        if isinstance(result, pd.DataFrame):
                            print("\nResults:")
                            print(result)
                        else:
                            print(f"Error: {result}")

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print(" Invalid choice. Please enter 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n Unexpected error: {e}")


if __name__ == "__main__":
    setup_database()
    interactive_sql_demo()
    connection.close()
