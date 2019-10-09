# Code-Point Open Data Transformer

[Code-Point Open][cpo] is a dataset of UK postcodes. This script makes the dataset
easier to use by denormalising it, concatenating the files, adding headers, and
standardising some of the formatting.

## Usage
With Python 3 and [Pipenv][pipenv] installed:

1. Clone this repository and run `pipenv install` within it.
2. Download the [Code-Point Open][cpo] dataset and unzip it.
3. Activate a local environment using `pipenv shell`.
4. Run the script using `python bin/cli.py /path/to/unzipped_data/ /path/to/output_dir/`

The script will write a `.csv` file for every set of regions included in the code-point
open "code list" files. It will also merge all the data files, converting linked values
to [CURIE][curie] format. Finally, it modifies the `Postcode` column to format it with a
single space

This script does the following:

- For each set of regions in the "code list" files, outputs a `.csv` file to create a register from
- Merges all the data files into `code-point-open.csv`
- Converts all the linked values in the data files to [CURIE][curie] format
- Formats the `postcode` column with a single space between outward and inward parts
- Adds a `geometry` column that is a space-separated combination of `eastings` and `northings`

[cpo]: https://www.ordnancesurvey.co.uk/business-government/products/code-point-open
[pipenv]: https://pipenv.readthedocs.io/en/latest/
[curie]: https://spec.openregister.org/v2/datatypes/curie
