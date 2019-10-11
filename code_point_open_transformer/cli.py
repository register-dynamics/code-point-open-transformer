from os import listdir
from os.path import join, isfile
import re
from collections import OrderedDict
import csv

import click
import openpyxl
import xlrd
from tqdm import tqdm # progress bar

DATA_HEADER_PATH = 'Doc/Code-Point_Open_Column_Headers.csv'
REGIONS_PATH = 'Doc/Codelist.xlsx'
NHS_REGIONS_FULL_PATH = 'Doc/NHS_Codelist.xls'
DATA_DIR_PATH = 'Data/CSV'
MERGED_DATA_FILE_NAME = 'code-point-open.csv'
COUNTRY_CODES_REGISTER_NAME = 'uk-country'
COUNTRY_CODES = {
  'E92000001': 'England',
  'S92000003': 'Scotland',
  'W92000004': 'Wales',
  'N92000002': 'N Ireland',
}

@click.command()
@click.argument('package_dir', type=click.Path(exists=True,
                dir_okay=True, file_okay=False))
@click.argument('output_dir', type=click.Path(exists=True,
                dir_okay=True, file_okay=False))
def main(package_dir, output_dir):
  """Improve usability of Code-Point Open data and link to lookup files"""

  regions_full_path = join(package_dir, REGIONS_PATH)

  # Parse table of contents from regions workbook
  regions_workbook = openpyxl.load_workbook(regions_full_path)
  regions_workbook_toc = {row[0]: slugify(row[1])
                          for row in regions_workbook['AREA_CODES'].values}

  # For each region sheet, write a register-ready CSV file
  # and build a map of region codes to sheet slugs for curies.
  region_to_sheet = {}
  region_header = ['code', 'name']
  for sheet_code, sheet_slug in regions_workbook_toc.items():
    sheet_file_path = join(output_dir, sheet_slug + '.csv')
    tqdm.write('Writing region file: ' + sheet_file_path)

    with open(sheet_file_path, 'w', newline='') as sheet_file:
      region_writer = csv.writer(sheet_file)
      region_writer.writerow(region_header)

      for region_name, region_code in regions_workbook[sheet_code].values:
        region_writer.writerow([region_code, region_name])
        region_to_sheet[region_code] = sheet_slug

  # Do the same for NHS region workbook, using older library
  nhs_regions_full_path = join(package_dir, NHS_REGIONS_FULL_PATH)
  nhs_regions_workbook = xlrd.open_workbook(nhs_regions_full_path)
  for sheet in nhs_regions_workbook.sheets():
    sheet_slug = slugify(sheet.name)
    sheet_file_path = join(output_dir, sheet_slug + '.csv')
    tqdm.write('Writing NHS region file: ' + sheet_file_path)

    with open(sheet_file_path, 'w', newline='') as sheet_file:
      region_writer = csv.writer(sheet_file)
      region_writer.writerow(region_header)

      for region_code, region_name in sheet.get_rows():
        region_writer.writerow([region_code.value, region_name.value])
        region_to_sheet[region_code.value] = sheet_slug

  # Write country codes to a register-ready CSV and append to code map
  country_codes_full_path = join(output_dir, COUNTRY_CODES_REGISTER_NAME + '.csv')
  with open(country_codes_full_path, 'w', newline='') as country_codes_file:
    country_codes_writer = csv.writer(country_codes_file)
    country_codes_writer.writerow(['code', 'name'])

    for country_code, country_name in COUNTRY_CODES.items():
      country_codes_writer.writerow([country_code, country_name])
      region_to_sheet[country_code] = COUNTRY_CODES_REGISTER_NAME

  # Load headers to prepend to data from header file
  data_header_full_path = join(package_dir, DATA_HEADER_PATH)
  with open(data_header_full_path, newline='') as data_header_file:
    raw_header = list(csv.reader(data_header_file))[1]
    data_header = [slugify(header) for header in raw_header]
    data_header.append('geometry')

  # For each data file
  data_dir_full_path = join(package_dir, DATA_DIR_PATH)
  data_file_paths = [join(data_dir_full_path, filename)
                     for filename in listdir(data_dir_full_path)
                     if isfile(join(data_dir_full_path, filename))]

  merged_data_full_path = join(output_dir, MERGED_DATA_FILE_NAME)
  with open(merged_data_full_path, 'w', newline='') as merged_data_file:
    merged_data_writer = csv.DictWriter(merged_data_file, fieldnames=data_header)
    merged_data_writer.writeheader()

    for data_file_path in tqdm(data_file_paths):
      tqdm.write('Processing data file: ' + data_file_path)
      with open(data_file_path, newline='') as data_file:
        data_reader = csv.DictReader(data_file, fieldnames=data_header)
        for row in data_reader:
          new_row = {}
          for key, value in row.items():
            if key.endswith('_code') and value in region_to_sheet:
              new_row[key] = region_to_sheet[value] + ':' + value
            else:
              new_row[key] = value
            
          new_row['postcode'] = format_postcode(new_row['postcode'])
          new_row['geometry'] = format_geometry(new_row['eastings'], new_row['northings'])

          merged_data_writer.writerow(new_row)

def slugify(input):
  return input.replace(' ', '-').lower()

def format_postcode(postcode):
  outward = postcode[:-3].strip()
  inward = postcode[-3:].strip()
  return '{} {}'.format(outward, inward)

def format_geometry(eastings, northings):
  return '{} {}'.format(eastings, northings)

if __name__ == '__main__':
  main()
