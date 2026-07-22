PYTHON       = python3
VENV         = .venv
ACTIVATE     = . $(VENV)/bin/activate
MAIN         = a_maze_ing.py
CONFIG       = config.txt
PKG_VERSION  = 1.0.0

MYPY_FLAGS = \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

.PHONY: install run debug clean lint lint-strict build

install:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install -r requirements.txt

run:
	$(ACTIVATE) && python3 $(MAIN) $(CONFIG)

debug:
	$(ACTIVATE) && python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} \;
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} \;
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf $(VENV)

lint:
	$(ACTIVATE)  && flake8 . --exclude $(VENV)
	$(ACTIVATE) && mypy . $(MYPY_FLAGS)

lint-strict:
	$(ACTIVATE) && flake8 . --exclude $(VENV) 
	$(ACTIVATE) && mypy . --strict

build:
	$(ACTIVATE) && python3 -m build
	cp dist/mazegen-$(PKG_VERSION).tar.gz .
	cp dist/mazegen-$(PKG_VERSION)-py3-none-any.whl .
	rm -rf dist/ mazegen.egg-info/
