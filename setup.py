from setuptools import setup
from setuptools import find_packages

with open("README.md") as f:
	read_description = f.read()


setup(
	name = "searchscraper",
	version = "0.2",
	author = "Adarsh Balakrishnan, Zhe Yu",
	author_email = "adarshbalakrishnan88@gmail.com",
	description = ("A scholar search API that can be used to scrape data from Arxiv."),
	long_description = read_description,
	long_description_content_type="text/markdown",
	url = 'https://github.com/hil-se/searchAPI',
	packages=find_packages(),
	classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Markup :: LaTeX",
        ]
	)        

