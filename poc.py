import os
from pathlib import Path

import requests as re
import logging

from pestuary.versioned_uploads import VersionedUploads

# datasets to url mapping
datasets = [
    {
        'name': '2022_primary_election_results.xlsx',
        'url': 'https://vote.phila.gov/files/raw-data/2022_Primary_Results_Major_Office.xlsx'
    },
    {
        'name': 'city_payments_fy2017.csv',
        'url': 'https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+city_payments_fy2017&filename=city_payments_fy2017&format=csv&skipfields=cartodb_id,the_geom,the_geom_webmercator'
    },
    {
        'name': 'business_licenses.csv',
        'url': 'https://phl.carto.com/api/v2/sql?q=SELECT+*,+ST_Y(the_geom)+AS+lat,+ST_X(the_geom)+AS+lng+FROM+business_licenses&filename=business_licenses&format=csv&skipfields=cartodb_id'
    },
    {
        'name': 'business_licenses.geojson',
        'url': 'https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+business_licenses&filename=business_licenses&format=geojson&skipfields=cartodb_id'
    },
    {
        'name': 'instore_forgivable_loan_program.csv',
        'url': 'https://phl.carto.com/api/v2/sql?q=SELECT+*+FROM+instore_forgivable_loan_program&filename=instore_forgivable_loan_program&format=csv&skipfields=cartodb_id,the_geom,the_geom_webmercator'
    }
]


def get_dataset_details(data):
    return data['name'], data['url']


def download_dataset(data, directory='data'):
    data_name, data_url = get_dataset_details(data)
    resp = re.get(data_url)
    open(os.path.join('.', directory, data_name), 'wb').write(resp.content)


def onboard_dataset_to_estuary(data, estuary_versioned_uploads, directory='data'):
    dataset_name, url = get_dataset_details(data)
    download_dataset(data, directory)
    logging.info('Downloaded dataset %s from url %s.', dataset_name, url)

    estuary_versioned_uploads.add_with_version(data=os.path.join(directory, dataset_name), filename=name)
    logging.info('Uploaded dataset %s to estuary.', dataset_name)


if __name__ == '__main__':
    versioned_uploads = VersionedUploads()
    data_dir = 'data'
    Path(data_dir).mkdir(exist_ok=True)
    for dataset in datasets:
        onboard_dataset_to_estuary(dataset, versioned_uploads, data_dir)
