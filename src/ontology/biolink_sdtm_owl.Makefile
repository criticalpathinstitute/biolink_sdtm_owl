## Customize Makefile settings for biolink_sdtm_owl
## 
## If you need to customize your Makefile, make
## changes here rather than in the main Makefile

# ----------------------------------------
# Robot Modules (non-dosdp, not imports)
# ----------------------------------------

MODULES = core_terms sdtm_dm sdtm_lb #sdtm_ur
MODULEDIR = ../modules
ALL_MODS_OWL = $(patsubst %, modules/%.owl, $(MODULES))
ALL_MODS_CSV = $(patsubst %, modules/%.csv, $(MODULES))

all_modules:: all_modules_owl #all_modules_obo
all_modules_owl:: $(ALL_MODS_OWL)
#all_modules_obo: $(patsubst %, modules/%.obo, $(MODS))

#Targets for ROBOT template modules
modules/%.owl:: $(MODULEDIR)/%.csv
	$(ROBOT) template --template $< --input biolink_sdtm_owl.owl --prefix "biolink_sdtm_owl: $(URIBASE)/biolink_sdtm_owl/" --prefix "biolink: https://w3id.org/biolink/vocab/" --ontology-iri $(ONTBASE)/$@ -o $@.tmp.owl && mv $@.tmp.owl $@

