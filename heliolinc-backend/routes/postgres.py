import psycopg2
import csv
import os
import pandas as pd
import io

# credentials to access db
hluser = "hluser"
hlpass="qXScJfdH1zW76sw9dFDj8w"
hlhost="127.0.0.1"
hlport="5432"
hldb="hldata"

db_params = {
    'dbname': hldb,
    'user': hluser,
    'password': hlpass,
    'host': hlhost,
    'port': hlport
}

desired_columns = ['object_id', 'ra', 'dec', 'mjd', 'obscode', 'username', 'band', 'mag']

def read_psv_ades(fn):
    """Read PSV ADES file
    
    Args:
        fn (str): Filename
        
    Returns:
        tuple: loaded dataframe, header
    """
    header = []
    with open(fn) as fp:
        # consume and store the header
        while True:
            line = fp.readline()
            if line[0] in ['#', '!']:
                header.append(line.rstrip())
                continue
            # the line is the header
            names = [ s.strip() for s in line.split('|') ]
            break
        df = pd.read_csv(fp, sep='|', header=None, names=names)
    return df, header

async def preprocess_csv(file_path):
    # Check if the file exists
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Determine file format
    file_extension = os.path.splitext(file_path)[1]
    header = None
    # Read the file based on its format
    if file_extension.lower() == '.psv':
        df, header = read_psv_ades(file_path)
    elif file_extension.lower() == '.csv':
        df = pd.read_csv(file_path)
    else:
        raise Exception("Unsupported file format")

    # Find the first case-insensitive match for each desired column
    matched_columns = {col: None for col in desired_columns}
    for col in df.columns:
        for desired_col in desired_columns:
            if desired_col in col.lower() and matched_columns[desired_col] is None:
                matched_columns[desired_col] = col

    # Remove None values from matched_columns
    matched_columns = {k: v for k, v in matched_columns.items() if v is not None}

    # Reorder and rename columns according to the matched columns
    df = df[matched_columns.values()]

    # Rename the columns to the desired names
    df.columns = [k for k, v in matched_columns.items()]

    # if obscode not present
    print(df.columns)
    if 'user_name' not in df.columns:
        df['user_name'] = 'vera'

    if "obscode" not in df.columns:
        for comment in header:
            if "obscode" in comment.lower() or "mpccode" in comment.lower():
                df["obscode"] = comment.split()[-1]
    print(df.columns)
    # check if all required columns are present
    required_columns = [col for col in desired_columns if col not in ['band', 'mag']]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' is missing in the data.")
    
    # Handle special columns
    if 'band' not in df.columns:
        df['band'] = None

    if 'mag' not in df.columns:
        df['mag'] = 99

    # Reorder DataFrame to desired column order
    df = df[desired_columns]

    insert_to_postgres(df, db_params, 'heliolinc', desired_columns)

def insert_to_postgres(df, connection_params, table_name, target_columns):
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Save DataFrame to an in-memory buffer
        buffer = io.StringIO()
        df.to_csv(buffer, sep='\t', index=False, header=False)
        buffer.seek(0)

        # Copy data from the buffer to the database
        cursor.copy_expert(f"COPY {table_name}({','.join(target_columns)}) FROM STDIN WITH CSV DELIMITER '\t'", buffer)
        connection.commit()
    except psycopg2.DatabaseError as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

def cleanup():
    # files generated during the process
    generated_files = [
        # './true_raw_input.csv',
        # './output.csv',
        'LSST_pairs_01.csv',
        'LSST_hl_all.csv',
        'LSST_hl_summary.csv',
        'LSST_lflist01'
    ]
    
    # delete the generated files
    for file in generated_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Deleted {file}")

