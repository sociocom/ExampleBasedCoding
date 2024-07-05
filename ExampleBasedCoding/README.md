# examplebasedcoding

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

    Flag Overwrite
        flag_overwrite: Whether to overwrite the flag column as "D". True or False.


Command example with arguments:

    python main.py <input_excel_path> <output_excel_path> <id_column> <source_column> <target_column> <flag_column> <source_flag_list> <target_flag_list> <flag_overwrite>


Example usage (with column names):

    python main.py data/DISEASE_test.xlsx data/output.xlsx ID 出現形 正規形 正規形_flag S,A,B,C D,nan False
