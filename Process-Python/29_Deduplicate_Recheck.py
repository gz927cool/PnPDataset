import pandas as pd
import os

# Define paths
base_dir = r"c:\Users\001\Desktop\Github-Project\PnPDataset"
input_dir = os.path.join(base_dir, "08-Data-Remerge")
input_file = os.path.join(input_dir, "01-Merged_Recheck.csv")
output_file = os.path.join(input_dir, "02-Merged_Recheck_Deduplicated.csv")

def deduplicate_data():
    print(f"Loading data from {input_file}...")
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    except:
        df = pd.read_csv(input_file, encoding='gbk')

    print(f"Original row count: {len(df)}")

    # Define aggregation logic
    def join_unique(series):
        # Filter out NaNs and empty strings, then get unique values
        values = [str(x).strip() for x in series if pd.notna(x) and str(x).strip() != '']
        unique_values = sorted(list(set(values)))
        return ' | '.join(unique_values)

    def get_first_mode(series):
        # Return the most frequent value, or the first one if all unique
        mode = series.mode()
        if not mode.empty:
            return mode[0]
        return series.iloc[0] if not series.empty else None

    # Group by Refined_Formal_Name
    # We need to handle rows where Refined_Formal_Name is NaN. 
    # Usually we don't want to merge all NaNs together.
    # So we split the dataframe.
    
    df_valid = df[df['Refined_Formal_Name'].notna() & (df['Refined_Formal_Name'] != '')]
    df_nan = df[df['Refined_Formal_Name'].isna() | (df['Refined_Formal_Name'] == '')]

    print(f"Rows with valid Refined_Formal_Name: {len(df_valid)}")
    print(f"Rows with empty Refined_Formal_Name: {len(df_nan)}")

    # Perform aggregation on valid rows
    # Columns: Original_Entry, Refined_Formal_Name, Refined_Category, Status/Notes
    
    agg_funcs = {
        'Original_Entry': join_unique,
        'Refined_Category': get_first_mode, # Assuming category should be consistent
        'Status/Notes': join_unique
    }

    df_deduped = df_valid.groupby('Refined_Formal_Name', as_index=False).agg(agg_funcs)
    
    # Combine back with NaN rows (which are not deduplicated)
    final_df = pd.concat([df_deduped, df_nan], ignore_index=True)
    
    # Sort for better readability
    final_df = final_df.sort_values(by='Refined_Formal_Name', na_position='last')

    print(f"Deduplicated row count: {len(final_df)}")
    print(f"Removed {len(df) - len(final_df)} duplicate rows.")

    # Save
    final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved deduplicated data to {output_file}")

if __name__ == "__main__":
    deduplicate_data()
