PY ?= python3
PAPERS = P1_Provenance_Dispatch P2_Fallback_Engines P3_NextCamera_Prediction \
         P4_Decoder_Admission P5_CrossModal_Fusion P6_Platform_Architecture

.PHONY: check fetch plan $(PAPERS)

## Verify every refs.bib: duplicate keys, missing fields, malformed DOIs. No network.
check:
	@for p in $(PAPERS); do $(PY) _tools/check_bib.py $$p || true; done

## Download open-access PDFs for every paper into <paper>/literature/pdf/.
## Needs network. Paywalled works are listed for manual pickup, never scraped.
fetch:
	@for p in $(PAPERS); do echo "== $$p"; $(PY) _tools/fetch_pdfs.py $$p; done

## Fetch one paper's PDFs, e.g. make P3_NextCamera_Prediction
$(PAPERS):
	$(PY) _tools/fetch_pdfs.py $@

## Show how many references each paper has and how many have a fetchable PDF URL.
plan:
	@$(PY) _tools/plan.py
