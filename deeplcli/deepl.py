'''A wrapper of DeepL APIs'''

import os
import sys
import configparser
import json
import csv
from typing import List, Optional
import requests

DEFAULT_TIMEOUT = 30.0


def retrieve_default_key():
    '''Retrieve Default Key'''

    config = configparser.ConfigParser()
    ini_file_path = os.path.join(os.environ['HOME'], '.deepl', 'credentials')
    config.read(ini_file_path)
    return config['default'].get('auth_key')


def translate(source_lang: str, target_lang: str, text: str, glossary_id: Optional[str] = None, auth_key: Optional[str] = None) -> Optional[str]:
    '''Request Translation'''

    url = 'https://api-free.deepl.com/v2/translate'

    auth_key = auth_key or retrieve_default_key()
    if auth_key is None:
        return None

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    params = {'source_lang': source_lang, 'target_lang': target_lang, 'text': text}
    if glossary_id is not None:
        params['glossary_id'] = glossary_id

    response = requests.post(url, headers=headers, data=params, timeout=DEFAULT_TIMEOUT)

    if not response.ok:
        print("Error: ", response.status_code, response.text, file=sys.stderr)
        return None

    result: dict = json.loads(response.content.decode('utf-8'))
    return result['translations'][0]['text']


def glossary_language_pairs(auth_key: Optional[str] = None) -> Optional[str]:
    '''List Language Pairs Supported by Glossaries'''

    url = 'https://api-free.deepl.com/v2/glossary-language-pairs'

    auth_key = auth_key or retrieve_default_key()
    if auth_key is None:
        return None

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

    if not response.ok:
        print("Error: ", response.status_code, response.text, file=sys.stderr)
        return None

    result = response.content.decode('utf-8')
    return result


def read_glossaries(glossary_files: List[str]) -> str:
    '''Read Glossaries'''

    glossary_pairs = []
    for pairs_file in glossary_files:
        with open(pairs_file, encoding='utf-8', newline='') as fin:
            for row in csv.reader(fin, delimiter='\t'):
                for from_ in row[:-1]:
                    if from_.startswith('#'):
                        continue
                    glossary_pairs.append(f'{from_},{row[-1]}')
    return '\n'.join(glossary_pairs)


def create_glossary(
    source_lang: str,
    target_lang: str,
    name: str,
    entries: Optional[str] = None,
    glossary_files: Optional[List[str]] = None,
    entries_format: str = 'csv',
    auth_key: Optional[str] = None,
) -> Optional[str]:
    '''Create a Glossary'''

    url = 'https://api-free.deepl.com/v2/glossaries'

    if entries is None and not glossary_files:
        return None

    auth_key = auth_key or retrieve_default_key()
    if auth_key is None:
        return None

    if glossary_files is not None:
        entries = read_glossaries(glossary_files)
        if not entries:
            return None

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    params = {
        'source_lang': source_lang,
        'target_lang': target_lang,
        'name': name,
        'entries': entries,
        'entries_format': entries_format,
    }

    response = requests.post(url, headers=headers, data=params, timeout=DEFAULT_TIMEOUT)

    if not response.ok:
        print("Error: ", response.status_code, response.text, file=sys.stderr)
        return None

    result = response.content.decode('utf-8')
    return result


def list_glossaries(auth_key: Optional[str] = None) -> Optional[str]:
    '''List all Glossaries'''

    url = 'https://api-free.deepl.com/v2/glossaries'

    auth_key = auth_key or retrieve_default_key()
    if auth_key is None:
        return None

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

    if not response.ok:
        print("Error: ", response.status_code, response.text)
        return None

    result = response.content.decode('utf-8')
    return result


def retrieve_glossary(glossary_id: str, auth_key: Optional[str] = None):
    '''Retrieve Glossary Details'''

    url = f'https://api-free.deepl.com/v2/glossaries/{glossary_id}'

    auth_key = auth_key or retrieve_default_key()
    if auth_key is None:
        return None

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

    if not response.ok:
        print("Error: ", response.status_code, response.text, file=sys.stderr)
        return None

    result = response.content.decode('utf-8')
    return result


def delete_glossary(glossary_id: str, auth_key: Optional[str] = None) -> Optional[str]:
    '''Delete a Glossary'''

    url = f'https://api-free.deepl.com/v2/glossaries/{glossary_id}'

    auth_key = auth_key or retrieve_default_key()
    if auth_key is None:
        return None

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    response = requests.delete(url, headers=headers, timeout=DEFAULT_TIMEOUT)

    if not response.ok:
        print("Error: ", response.status_code, response.text, file=sys.stderr)
        return None

    result = response.content.decode('utf-8')
    return result


def retrieve_glossary_entries(glossary_id: str, auth_key: Optional[str] = None) -> Optional[str]:
    '''Retrieve Glossary Entries'''

    url = f'https://api-free.deepl.com/v2/glossaries/{glossary_id}/entries'

    auth_key = auth_key or retrieve_default_key()
    if auth_key is None:
        return None

    headers = {'Authorization': 'DeepL-Auth-Key ' + auth_key, 'Accept': 'text/tab-separated-values'}

    response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

    if not response.ok:
        print("Error: ", response.status_code, response.text, file=sys.stderr)
        return None

    result = response.content.decode('utf-8')
    return result
