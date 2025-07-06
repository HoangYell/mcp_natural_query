
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
