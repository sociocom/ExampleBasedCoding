Command line tool by example based coding.

Command line arguments:
    Path
        input: Input Excel file path
        output: Output Excel file path
    
    Column names
        id: ID column in Excel file
        source: Source column in Excel file
        target: Target column in Excel file
        flag_col: Flag column in Excel file
    
    Flag list
        source_flag: Source flag list for training data. If the flags are more than one, split by comma without space.
        target_flag: Target flag list for test data. If the flags are more than one, Split by comma without space.

Example usage (with column names):
    python main.py data/DISEASE_test.xlsx data/output.xlsx ID 出現形 正規形 正規形_flag S,A,B,C D,nan
