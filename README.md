# Code-Point Open Data Transformer

[Code-Point Open][cpo] is a dataset of UK postcodes. This script makes the dataset
easier to use by denormalising it, concatenating the files, adding headers, and
standardising some of the formatting.

## Installation
Ensure you have Python 3.7+ installed on your machine.

```
pip3 install --user "git+https://github.com/timwis/code-point-open-transformer#egg=code-point-open-transformer"
```

## Usage
```
Usage: codepointopen [OPTIONS] PACKAGE_DIR OUTPUT_DIR

  Improve usability of Code-Point Open data and link to lookup files
```

This script does the following:

- For each set of regions in the "code list" files, outputs a `.csv` file to create a register from
- Merges all the data files into `code-point-open.csv`
- Converts all the linked values in the data files to [CURIE][curie] format
- Formats the `postcode` column with a single space between outward and inward parts
- Adds a `geometry` column that is a space-separated combination of `eastings` and `northings`

[cpo]: https://www.ordnancesurvey.co.uk/business-government/products/code-point-open
[pipenv]: https://pipenv.readthedocs.io/en/latest/
[curie]: https://spec.openregister.org/v2/datatypes/curie
