
import mysql.connector
from config import db_config
from mcp.server.fastmcp import FastMCP

def test_db_connection():
    """Test the MySQL database connection. Returns True if successful, else False."""
    try:
        conn = mysql.connector.connect(**db_config)
        conn.close()
        print("[INFO] Database connection successful.")
        return True
    except Exception as e:
        print(f"[FATAL] Could not connect to the database: {e}")
        return False

if not test_db_connection():
    import sys
    sys.exit(1)


# Add title and description for better discoverability
mcp = FastMCP(
    "naturalquery",
)


# Use structured output and add tool metadata
@mcp.tool(title="List MySQL Tables", description="Read all tables in the current MySQL schema to find the relevant table based on human input.")
def mysql_list_tables() -> list[str]:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tables
    except Exception as e:
        return [f"Error: {e}"]


# 2. Get Table Sample Rows
@mcp.tool(title="Get Table Sample Rows", description="Fetch a few sample rows from a table for context.")
def mysql_get_table_sample_rows(table_name: str, limit: int = 5) -> list:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM `{table_name}` LIMIT %s", (limit,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        return [f"Error: {e}"]


# 3. Get Table Column Names
@mcp.tool(title="Get Table Column Names", description="List the column names of a table.")
def mysql_get_table_column_names(table_name: str) -> list[str]:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        columns = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return columns
    except Exception as e:
        return [f"Error: {e}"]


# 4. Search Table by Keyword
@mcp.tool(title="Search Table by Keyword", description="Search for a keyword in all columns of a table.")
def mysql_search_table_by_keyword(table_name: str, keyword: str, limit: int = 5) -> list:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Get column names
        cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
        columns = [row[0] for row in cursor.fetchall()]
        # Build WHERE clause
        like_clauses = [f"`{col}` LIKE %s" for col in columns]
        where_clause = " OR ".join(like_clauses)
        sql = f"SELECT * FROM `{table_name}` WHERE {where_clause} LIMIT %s"
        params = tuple([f"%{keyword}%"] * len(columns)) + (limit,)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        return [f"Error: {e}"]


# 5. Get Foreign Key Relationships
@mcp.tool(title="Get Foreign Key Relationships", description="Describe foreign key relationships for a table.")
def mysql_get_foreign_keys(table_name: str) -> list:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL
            """,
            (table_name,)
        )
        fks = cursor.fetchall()
        cursor.close()
        conn.close()
        return fks
    except Exception as e:
        return [f"Error: {e}"]


@mcp.tool(title="Describe Table", description="Describes the structure of a given table in the current MySQL schema.")
def mysql_describe_table(table_name: str) -> list[tuple]:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE `{table_name}`")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return [f"Error: {e}"]


@mcp.tool(title="Execute MySQL Query", description="Executes a MySQL query and returns the result as a list of rows or affected row count.")
def mysql_execute_query(query: str) -> list:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.description:
            result = cursor.fetchall()
        else:
            result = [f"{cursor.rowcount} rows affected."]
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        return [f"Error: {e}"]


# For production, use streamable-http transport for better scalability
if __name__ == "__main__":
    mcp.run()
