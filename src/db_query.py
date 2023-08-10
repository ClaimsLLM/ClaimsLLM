import json, sqlite3


def extract_data_to_json(query):
    try:
        # Connect to the database
        connection = sqlite3.connect('./policy.db')
        cursor = connection.cursor()

        # Execute a SELECT query
        select_query = f"SELECT * FROM policy WHERE mobile_number={query}"
        cursor.execute(select_query)

        # Fetch the results
        results = cursor.fetchall()

        # Create a list of dictionaries to store the results
        data = []
        for row in results:
            data.append({
                "Policy Number": row[0],
                "Name": row[1],
                "Registration Number":row[2],
                "Sum Insured": row[3],
                "Period of Insurance": row[4],
                "Mobile Number": row[5]
            })

        # Write the data to a JSON file
        # with open("./data/policy.json", "w") as json_file:
        #     json.dump(data, json_file, indent=4)
        return data
        print("Data extracted and saved to JSON file successfully.")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        # Close the connection
        if connection:
            connection.close()

