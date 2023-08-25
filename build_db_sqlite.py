import sqlite3

def build_sqlite_db():
    # Connect to or create the database
    db_path = "policy.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # drop_table_statement = "DROP TABLE policy" 
    # cursor.execute(drop_table_statement)

    # Create a table with columns
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS policy (
            policy_number TEXT PRIMARY KEY,
            customer_id TEXT DEFAULT NULL,
            registration_number TEXT,
            sum_insured INTEGER,
            period_of_insured TEXT,
            mobile_number INTEGER
        )
    '''
    cursor.execute(create_table_query)
    connection.commit()

    # Insert values into the table
    insert_data_query = '''
        INSERT INTO policy
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    values_to_insert = [        
        ("3362/02405675/000/00","Mr. Rishabh Sood", "KA53MC5013", 4714, "From 15/10/2022 00:00 to 14/10/2023 23:59",9582394818),    
        ("1704003123P104849149","MR UMAPATHI K", "TN - 37 - AW - 9914", 784,"From 00:00 Hrs of 04/08/2023 To Midnight of 03/08/2024",9994322446)
    ]
    cursor.executemany(insert_data_query, values_to_insert)
    connection.commit()


    # Close the connection
    connection.close()

if __name__=='__main__':
    build_sqlite_db()