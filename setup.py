from distutils.core import setup

with open("README.md") as f:
	read_description = f.read()


setup(
	name = 'SearchAPI',
	version = '0.1',
	packages = ['API',],
	long_description = read_description
	)
