import subprocess
import os
import glob

# Paths are relative to the working dir, so run this script from biolink_sdtm_owl main dir.
working_dir = os.getcwd()
output_ttl_path_reasoned = os.path.join("data_mapping", "turtle", "biolink_sdtm_owl_with_data_reasoned.ttl")

query_path = os.path.join("data_mapping", "queries", "*.sparql")


query_paths = [path for path in glob.glob(query_path)]
results_paths = [os.path.join("data_mapping", "query_results", os.path.basename(path).replace('.sparql','.csv')) for path in query_paths]


convert_paths_for_docker = lambda path: path.replace("\\","/")

for input_path, output_path in zip(query_paths, results_paths):
    subprocess.run(["docker", "run", 
                    "-v", f"{working_dir}:/work",
                    "--rm", "-ti",
                    "obolibrary/robot", "robot", "query",
                    "--input", f"/work/{convert_paths_for_docker(output_ttl_path_reasoned)}",
                    "--query", f"/work/{convert_paths_for_docker(input_path)}",
                    f"/work/{convert_paths_for_docker(output_path)}"
                    ])