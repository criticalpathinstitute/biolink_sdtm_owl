import pandas as pd
import os

# TODO Rewrite to edit arbitrary number of files instead of copying the code for one.


mapping_df = pd.read_csv(os.path.join("data_mapping", "mappings", "uri_mappings.csv"))

data_dir = os.path.join("data_mapping", "sample_data")

input_lb_path = os.path.join(data_dir, "lb_original.csv")
output_lb_path = os.path.join(data_dir, "lb.csv")

input_ur_path = os.path.join(data_dir, "ur_original.csv")
output_ur_path = os.path.join(data_dir, "ur.csv")



# Edit the LB dataset, adding the uri columms specified in the mapping file.
mapping_df_subset = mapping_df.loc[mapping_df["domain"]=="lb"]
df = pd.read_csv(input_lb_path)
for _,source_col,target_col in mapping_df_subset[["source_col","target_col"]].drop_duplicates().itertuples():
    cols_to_keep = df.columns.to_list()
    df = df.merge(
        right=mapping_df_subset, 
        how="left", 
        left_on=["domain",source_col],
        right_on=["domain","source_value"],
        )
    df[target_col] = df.apply(lambda row: f"{row.target_prefix}{row.target_curie}", axis=1)
    df = df[cols_to_keep+[target_col]]
df.to_csv(output_lb_path, index=False)



# Edit the UR dataset, adding the URI columns specified in the mapping file.
mapping_df_subset = mapping_df.loc[mapping_df["domain"]=="ur"]
df = pd.read_csv(input_ur_path)
for _,source_col,target_col in mapping_df_subset[["source_col","target_col"]].drop_duplicates().itertuples():
    cols_to_keep = df.columns.to_list()
    df = df.merge(
        right=mapping_df_subset, 
        how="left", 
        left_on=["domain",source_col],
        right_on=["domain","source_value"],
        )
    df[target_col] = df.apply(lambda row: f"{row.target_prefix}{row.target_curie}", axis=1)
    df = df[cols_to_keep+[target_col]]
df.to_csv(output_ur_path, index=False)