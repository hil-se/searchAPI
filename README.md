# searchAPI

You can directly use `SearchAPI` to save the record of the journals based on the keywords or catergories entered. SearchAPI obtains abstract for the search keywords and saves it in a csv file.

SearchAPI currently runs as per the instructions provided in arxiv API user manual: https://arxiv.org/help/api/user-manual. 

The search results can be filtered based on Title, Author, Abstract, Comment, Journal Reference, Subject Category, Report Number and Id. 

## Examples

### Without filtering
It can be entered on the command line as
	```
	python SearchAPI.py --search electron --start 0 --max 10000 --sort relevance
	```

Where `search` is a mandatory field and to filter search results based on categories use `cat:` and select the categories listen on the user manual. For the default field, the prefix is not mandatory and title will be used as default.   

`start`, `max` and `sort` are non-mandatory fields and the defaults are mentioned as above.


## References
<a id="1">[1]</a> 
Mahdi Sadjadi (2017). arxivscraper: Zenodo. http://doi.org/10.5281/zenodo.889853
