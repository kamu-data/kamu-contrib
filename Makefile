.PHONY: docs
docs:
	kamu inspect lineage --output-format dot | dot -Tpng > doc/depgraph.png


.PHONY: strip-notebooks
strip-notebooks:
	find . -name '.ipynb_checkpoints' -type d -prune -exec rm -rf {} \;
	find . -name '*.ipynb' -type f -exec nbstripout {} \;
