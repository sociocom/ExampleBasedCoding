
import argparse
import pandas as pd
from ExampleBasedCoding import EntityDictionary, normalize
import numpy as np

"""
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
        
"""

"""
python main.py data/BODY_SIP-3_v20240508.xlsx data/output.xlsx ID 出現形 正規形 正規形_flag S,A,B,C D,nan
python main.py data/output.xlsx data/output_2.xlsx ID 出現形 TREE TREE_flag S,A,B,C D,nan
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Example usage (with column names):
    python main.py data/DISEASE_test.xlsx data/output.xlsx ID 出現形 正規形 正規形_flag S,A,B,C D,nan""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("input", type=str, help="Input Excel file path")
    parser.add_argument("output", type=str, help="Output Excel file path")

    parser.add_argument("id", type=str, help="ID column in Excel file")
    parser.add_argument("source", type=str, help="Source column in Excel file")
    parser.add_argument("target", type=str, help="Target column in Excel file")
    parser.add_argument("flag_col", type=str, help="Flag column in Excel file")
    
    parser.add_argument("source_flag", type=str,\
        help="Source flag list for training data. If the flags are more than one, split by comma without space.")
    parser.add_argument("target_flag", type=str,\
        help="Target flag list for test data. If the flags are more than one, Split by comma without space.")
    
    args = parser.parse_args()
    
    args.source_flag = args.source_flag.strip("[]").split(",")
    args.target_flag = args.target_flag.strip("[]").split(",")
        
    # コマンドライン引数から値のリストを取得
    args.source_flag = [str(i) if i.lower() != "nan" else np.nan 
                        for i in args.source_flag]
    args.target_flag = [str(i) if i.lower() != "nan" else np.nan 
                        for i in args.target_flag]

    print(f"-Input Information----------------")
    print(f"Target Column: {args.target}")
    print(f"Flag Column: {args.flag_col}")    
    print(f"Source Flag: {args.source_flag}")
    print(f"Target Flag: {args.target_flag}")
    print(f"----------------------------------")
    
    print("data loading...")
    df_original = pd.read_excel(args.input, index_col=0)
    print("data loading done.")
    
    df = df_original[[args.id, args.source, args.target, args.flag_col]]
    
    train_data = df[df[args.flag_col].isin(args.source_flag)]
    train_data = train_data[train_data[args.target]!="-1"]
    train_data = train_data[train_data[args.target]!="[ERR]"]

    train_data[[args.id, args.source, args.target, args.flag_col]].to_csv("train_data.csv")
    
    id_words = list(df[df[args.flag_col].isin(args.target_flag)].index)
    words = df[df[args.flag_col].isin(args.target_flag)][args.source].tolist()
    words = [str(i) for i in words]

    ## Normalize entities
    print("normalizing...")
    normalization_dictionary  = EntityDictionary(\
    'train_data.csv',  args.source,  args.target)
    
    normalized, scores  = normalize(words,  normalization_dictionary,  matching_threshold=0)
    print("normalizing done.")

    df_results = pd.DataFrame([id_words, words, normalized, scores]).T
    
    # カラム名設定
    df_results.columns = [args.id, args.source, args.target, "score"]
    df_results.set_index(args.id, inplace=True)
    df_original.update(df_results)

    ## Write output file
    print("saving...")
    df_original.to_excel(args.output)
    print("saving done.")