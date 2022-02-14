import pandas as pd
import os


mapping_df = pd.read_csv(os.path.join("data_mapping", "mappings", "uri_mappings.csv"))

data_dir = os.path.join("data_mapping", "synthetic_data")


# Define domain strings and file paths for the each domain.
domains = ["dm", "lb", "ur"]
input_paths = [os.path.join(data_dir, f"{domain}.csv") for domain in domains]
output_paths = [os.path.join(data_dir, f"{domain}_modified.csv") for domain in domains]




# Optional subsetting, input_paths[0] should be the path for the dm file.
subset = True
n = 100
usubjids_to_retain = pd.read_csv(input_paths[0])["usubjid"].unique().tolist()[:n]



# Loop through the two domains.
for domain, input_path, output_path in zip(domains, input_paths, output_paths):

    # Edit the dataset, adding the uri columms specified in the mapping file.
    mapping_df_subset = mapping_df.loc[mapping_df["domain"]==domain]
    df = pd.read_csv(input_path)
    df.drop(["domain"], axis=1, inplace=True, errors="ignore")
    df.insert(0, "row_id", range(1,1+len(df)))
    df.insert(0, "domain", domain)
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


    if subset:
        df = df[df["usubjid"].isin(usubjids_to_retain)]
    df.to_csv(output_path, index=False)






# # Subsetting.
# dm_df = pd.read_csv(os.path.join(data_dir, "dm_modified.csv"))
# lb_df = pd.read_csv(os.path.join(data_dir, "lb_modified.csv"))
# ur_df = pd.read_csv(os.path.join(data_dir, "ur_modified.csv"))

# n = 100
# usubjids_to_retain = dm_df["usubjid"].unique().tolist()[:n]


# dm_df[dm_df["usubjid"].isin(usubjids_to_retain)].to_csv(os.path.join(data_dir, "dm_modified.csv"), index=False)
# lb_df[lb_df["usubjid"].isin(usubjids_to_retain)].to_csv(os.path.join(data_dir, "dm_modified.csv"), index=False)
# ur_df[ur_df["usubjid"].isin(usubjids_to_retain)].to_csv(os.path.join(data_dir, "dm_modified.csv"), index=False)

# dm_df.to_csv()


# print(usubjids_to_retain)