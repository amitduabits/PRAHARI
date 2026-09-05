PY ?= python3

.PHONY: all test experiments figures clean p1 p2 p3 p4 p5 p6

all: test experiments

test:
	$(PY) -m pytest tests -q

experiments:
	$(PY) run_all.py

figures:
	$(PY) make_figures.py

p1 p2 p3 p4 p5 p6:
	$(PY) run_all.py $@

clean:
	rm -f results/*.json figures/*.png
