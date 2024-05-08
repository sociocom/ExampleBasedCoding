
import argparse
import pandas as pd
from ExampleBasedCoding import EntityDictionary, normalize

"""
Command line tool by example based coding.

Command line arguments:
    input: Input Excel file path
    output: Output Excel file path
    id: ID column in Excel file
    source: Source column in Excel file
    target: Target column in Excel file

Example usage (with column names):
    python main.py data/DISEASE_test.xlsx data/output.xlsx ID 出現形 正規形 正規形_flag '["S", "A", "B", "C"]' '["D"]'
        
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Example usage (with column names):
    python main.py data/DISEASE_test.xlsx data/output.xlsx ID 出現形 正規形 正規形_flag ["S", "A", "B", "C"] ["D"]""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("input", type=str, help="Input Excel file path")
    parser.add_argument("output", type=str, help="Output Excel file path")

    parser.add_argument("id", type=str, help="ID column in Excel file")
    parser.add_argument("source", type=str, help="Source column in Excel file")
    parser.add_argument("target", type=str, help="Target column in Excel file")
    parser.add_argument("flag_col", type=str, help="Flag column in Excel file")
    
    parser.add_argument("source_flag", type=list, help="source flag list for training data")
    parser.add_argument("target_flag", type=list, help="target flag list for test data")
    
    args = parser.parse_args()

    df_original = pd.read_excel(args.input, index_col=0)
    df = df_original[[args.id, args.source, args.target, args.flag_col]]
    


    # %%
    train_data = df[df[args.flag_col].isin(args.source_flag)]
    train_data = train_data[train_data[args.target]!="-1"]
    train_data = train_data[train_data[args.target]!="[ERR]"]

    train_data[[args.id, args.source, args.target, args.flag_col]].to_csv("train_data.csv")
    
    id_words = list(df[df[args.flag_col].isin(args.target_flag)].index)
    words = df[df[args.flag_col].isin(args.target_flag)][args.source].tolist()
    words = [str(i) for i in words]

    ## Normalize entities
    normalization_dictionary  = EntityDictionary(\
    'train_data.csv',  args.source,  args.target)
    normalized, scores  = normalize(words,  normalization_dictionary,  matching_threshold=0)

    df_results = pd.DataFrame([id_words, words, normalized, scores]).T
    
    # カラム名設定
    df_results.columns = [args.id, args.source, args.target, "score"]
    df_results.set_index(args.id, inplace=True)
    df_original.update(df_results)

    ## Write output file
    df_original.to_excel(args.output)
