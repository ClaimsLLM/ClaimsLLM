import sqlite3

def build_sqlite_db():
    # Connect to or create the database
    db_path = "policy.db"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

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
        ("0177899357 01 00", "MS SANCHAREE DAS","KA 03 MW 5618" , 8426,"From 03/09/2022 to. Midnight of 02/09/2023",9739000376),
        ("2311 1002 2924 3401 000","MS SANCHAREE DAS","KA-03-MW-5618" , 14352, "From 03 Sep, 2018 00:01 hrs To 02 Sep, 2019 Midnight",9739000376),
        ("3362/02405675/000/00","Mr. Rishabh Sood", "KA53MC5013", 4714, "From 15/10/2022 00:00 to 14/10/2023 23:59",9582394818),
        ("920222223122786188","MR.PANCHANAN BHAUMIK", "WB30L4485", 981, "From 00:00 Hrs on 28-Oct-2022 to Midnight of 27-Oct-2023",9739000376),
        ("OG-23-9906-1802-00514595","AMIT KUMAR BHAUMIK", "KA01EQ0723", 1693, "From: 03-Feb-2023, 00:00 To: 02-Feb-2024 Midnight",9739000376),
        ("1704003123P104849149","MR UMAPATHI K", "TN - 37 - AW - 9914", 784,"From 00:00 Hrs of 04/08/2023 To Midnight of 03/08/2024",9994322446)
    ]
    cursor.executemany(insert_data_query, values_to_insert)
    connection.commit()


    # Close the connection
    connection.close()

if __name__=='__main__':
    build_sqlite_db()