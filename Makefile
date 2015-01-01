PYTHON = python3
FLAKE8 = flake8
DISTFM = egg_info bdist_egg bdist_wheel --python-tag=py32 sdist --format=bztar,gztar,zip

dist:
	$(PYTHON) setup.py $(DISTFM)

all: dist

clean:
	rm -rfv build/ */__pycache__/ */*.py[cdo]

distclean: clean
	rm -rfv dist/ mitorrent.egg-info/

install:
	$(PYTHON) setup.py install

test:
	$(PYTHON) setup.py check
	$(PYTHON) -m unittest --buffer --catch
	$(FLAKE8) --count

upload:
	$(PYTHON) setup.py $(DISTFM) upload -r https://testpypi.python.org/pypi
