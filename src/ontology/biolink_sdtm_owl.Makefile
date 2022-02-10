## Customize Makefile settings for biolink_sdtm_owl
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# ----------------------------------------
# Robot Modules (non-dosdp, not imports)
# ----------------------------------------

MODULES = core_terms sdtm_dm sdtm_lb sdtm_ur
MODULEDIR = ../modules
ALL_MODS_OWL = $(patsubst %, modules/%.owl, $(MODULES))
ALL_MODS_CSV = $(patsubst %, modules/%.csv, $(MODULES))

all_modules:: all_modules_owl #all_modules_obo
all_modules_owl:: $(ALL_MODS_OWL)
#all_modules_obo: $(patsubst %, modules/%.obo, $(MODS))

#Targets for ROBOT template modules
modules/%.owl:: $(MODULEDIR)/%.csv
	$(ROBOT) template --template $< --input biolink_sdtm_owl.owl --prefix "biolink_sdtm_owl: $(URIBASE)/biolink_sdtm_owl/" --prefix "biolink: https://w3id.org/biolink/vocab/" --ontology-iri $(ONTBASE)/$@ -o $@.tmp.owl && mv $@.tmp.owl $@

#Commands for ncit import
#robot extract --catalog catalog.xml --input mirror/ncit.owl --term-file imports/ncit_terms.txt --method BOT --output imports/ncit_import.owl --individuals minimal --output imports/ncit_import.owl


#first run export ROBOT_JAVA_ARGS=-Xmx4G

#robot --catalog catalog-v001.xml extract -i mirror/ncit.owl -T imports/ncit_terms_combined.txt --force true --individuals exclude --method BOT \
	annotate --ontology-iri https://w3id.org/c-path/biolink_sdtm_owl/imports/ncit_import.owl annotate -V https://w3id.org/c-path/biolink_sdtm_owl/releases/2022-02-10/imports/ncit_import.owl --annotation owl:versionInfo 2022-02-10 --output imports/ncit_import.owl

#command to make all main products
#need to get rid of the 'relax' command specified by default, because equivalency axioms are important for us
#Also need to get rid of the 'reduce' command, because it does really wonky things to the ontology.

#robot --catalog catalog-v001.xml merge --input biolink_sdtm_owl-edit.owl \
	reason --reasoner ELK --equivalent-classes-allowed all --exclude-tautologies structural \
	 annotate --ontology-iri https://w3id.org/c-path/biolink_sdtm_owl/biolink_sdtm_owl-full.owl annotate -V https://w3id.org/c-path/biolink_sdtm_owl/releases/2022-02-08/biolink_sdtm_owl-full.owl --annotation owl:versionInfo 2022-02-08 --output biolink_sdtm_owl-full.owl.tmp.owl && mv biolink_sdtm_owl-full.owl.tmp.owl biolink_sdtm_owl-full.owl


