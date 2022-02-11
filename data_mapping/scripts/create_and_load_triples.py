import subprocess
import os


# Note that the relative paths for source data have to be hardcoded within the YARRRML mapping template.
# So to use a different folder than /sample_data, the source values in that yaml file have to be changed.

# Paths are relative to the working dir, so run this script from biolink_sdtm_owl main dir.
working_dir = os.getcwd()

# Input paths and files.
yarrrml_template_path = os.path.join("data_mapping", "mappings", "mapping_template.yml")
ontology_ttl_path = os.path.join("data_mapping", "turtle", "biolink_sdtm_owl.ttl")


# Output paths and files.
output_dir = "output"
rml_template_output_path = os.path.join("data_mapping", "turtle", "rml_template.ttl")
instance_data_output_path = os.path.join("data_mapping", "turtle", "instance_data_triples.ttl")
output_ttl_path = os.path.join("data_mapping", "turtle", "biolink_sdtm_owl_with_data.ttl")
output_ttl_path_reasoned = os.path.join("data_mapping", "turtle", "biolink_sdtm_owl_with_data_reasoned.ttl")


convert_paths_for_docker = lambda path: path.replace("\\","/")


# 1. Convert the YARRRML mapping template to a RML mapping template.
subprocess.run(["docker", "run", "--rm", "-it", 
                "-v", f"{working_dir}:/data", 
                "rmlio/yarrrml-parser:latest", 
                "-i", f"/data/{convert_paths_for_docker(yarrrml_template_path)}", 
                "-o", f"/data/{convert_paths_for_docker(rml_template_output_path)}"
                ])



# 2. Use the RML mapping template to process the csv's and output the data triples as a ttl file.
subprocess.run(["docker", "run", "--rm", 
                "-v", f"{working_dir}:/data", 
                "rmlio/rmlmapper-java", 
                "-m", f"{convert_paths_for_docker(rml_template_output_path)}",  
                "-o", f"{convert_paths_for_docker(instance_data_output_path)}"
                ])




# 3. Create a combined ttl file for the ontology and the instance data.
with open(instance_data_output_path, "r") as f:
    data_triples = f.read()

with open(ontology_ttl_path, "r") as f:
    ontology_content = f.read()

with open(output_ttl_path, "w") as f:
    f.write(f"{ontology_content}\n\n\n{data_triples}")




# 4. Reason over the combined ontology and data triples and save the output ttl file.
subprocess.run(["docker", "run", 
                "-v", f"{working_dir}:/work",
                "--rm", "-ti",
                "obolibrary/robot", "robot", "reason",
                "--reasoner", "hermit",
                "--axiom-generators", '"SubClass EquivalentClass ClassAssertion PropertyAssertion"',
                "--input", f"/work/{convert_paths_for_docker(output_ttl_path)}",
                "--include-indirect", "true",
                "reduce",
                "--output", f"/work/{convert_paths_for_docker(output_ttl_path_reasoned)}"
                ])
