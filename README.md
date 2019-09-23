# Code-Point Open Data Transformer

[Code-Point Open][cpo] is a dataset of UK postcodes. This script makes the dataset
easier to use by denormalising it, concatenating the files, adding headers, and
standardising some of the formatting.

## Usage
With Python 3 and [Pipenv][pipenv] installed:

1. Clone this repository and run `pipenv install` within it.
2. Download the [Code-Point Open][cpo] dataset and unzip it.
3. Run the script using `python bin/cli.py /path/to/unzipped_directory/ > output.csv`

The script adds columns for lookup fields and a WKT-formatted version of the coordinates.
The only column it modifies is `Postcode`, formatting it with a single space between the
outward and inward parts. To remove some of the columns after processing, use a tool like
csvcut from [csvkit][csvkit].

[cpo]: https://www.ordnancesurvey.co.uk/business-government/products/code-point-open
[pipenv]: https://pipenv.readthedocs.io/en/latest/
[csvkit]: https://pipenv.readthedocs.io/en/latest/
