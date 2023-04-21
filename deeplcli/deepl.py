import os
import argparse
import configparser
import requests
import json
import csv
from typing import List


def retrieve_default_key():
    config = configparser.ConfigParser()
    ini_file_path = os.path.join(os.environ['HOME'], '.deepl', 'credentials')
    config.read(ini_file_path)
    return config['default'].get('auth_key')


def command_translate(args):
    url = 'https://api-free.deepl.com/v2/translate'

    auth_key = args.auth_key or retrieve_default_key()
    if auth_key is None:
        raise

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    params = {'source_lang': args.source_lang, 'target_lang': args.target_lang, 'text': args.text}
    if args.glossary_id is not None:
        params['glossary_id'] = args.glossary_id

    response = requests.post(url, headers=headers, data=params)

    if response.ok:
        result = json.loads(response.content.decode('utf-8'))
        print(result['translations'][0]['text'])
        # print(result['translations'])
    else:
        print("Error: ", response.status_code, response.text)


def command_glossary_language_pairs(args):
    url = 'https://api-free.deepl.com/v2/glossary-language-pairs'

    auth_key = args.auth_key or retrieve_default_key()
    if auth_key is None:
        raise

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        result = json.loads(response.content.decode('utf-8'))
        print(json.dumps(result))
    else:
        print("Error: ", response.status_code, response.text)


def read_glossaries(glossary_files: List[str]) -> str:
    glossary_pairs = []
    for pairs_file in glossary_files:
        with open(pairs_file, encoding='utf-8', newline='') as fin:
            for row in csv.reader(fin, delimiter='\t'):
                for from_ in row[:-1]:
                    if from_.startswith('#'):
                        continue
                    glossary_pairs.append(f'{from_},{row[-1]}')
    return '\n'.join(glossary_pairs)


def command_create_glossary(args):
    url = 'https://api-free.deepl.com/v2/glossaries'

    if args.entries is None and args.glossary_files is None:
        raise

    auth_key = args.auth_key or retrieve_default_key()
    if auth_key is None:
        raise

    if args.entries is not None:
        entries = args.entries
    else:
        entries = read_glossaries(args.glossary_files)
        if not entries:
            raise

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    params = {
        'source_lang': args.source_lang,
        'target_lang': args.target_lang,
        'name': args.name,
        'entries': entries,
        'entries_format': args.entries_format,
    }

    response = requests.post(url, headers=headers, data=params)

    if response.ok:
        result = json.loads(response.content.decode('utf-8'))
        print(json.dumps(result))
    else:
        print("Error: ", response.status_code, response.text)


def command_list_glossaries(args):
    url = 'https://api-free.deepl.com/v2/glossaries'

    auth_key = args.auth_key or retrieve_default_key()
    if auth_key is None:
        raise

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        result = json.loads(response.content.decode('utf-8'))
        print(json.dumps(result))
    else:
        print("Error: ", response.status_code, response.text)


def command_retrieve_glossary(args):
    url = f'https://api-free.deepl.com/v2/glossaries/{args.glossary_id}'

    auth_key = args.auth_key or retrieve_default_key()
    if auth_key is None:
        raise

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        result = json.loads(response.content.decode('utf-8'))
        print(json.dumps(result))
    else:
        print("Error: ", response.status_code, response.text)


def command_delete_glossary(args):
    url = f'https://api-free.deepl.com/v2/glossaries/{args.glossary_id}'

    auth_key = args.auth_key or retrieve_default_key()
    if auth_key is None:
        raise

    headers = {
        'Authorization': 'DeepL-Auth-Key ' + auth_key,
    }

    response = requests.delete(url, headers=headers)

    if response.ok:
        result = response.content.decode('utf-8')
        print(result)
    else:
        print("Error: ", response.status_code, response.text)


def command_retrieve_glossary_entries(args):
    url = f'https://api-free.deepl.com/v2/glossaries/{args.glossary_id}/entries'

    auth_key = args.auth_key or retrieve_default_key()
    if auth_key is None:
        raise

    headers = {'Authorization': 'DeepL-Auth-Key ' + auth_key, 'Accept': 'text/tab-separated-values'}

    response = requests.get(url, headers=headers)

    if response.ok:
        result = response.content.decode('utf-8')
        print(result)
    else:
        print("Error: ", response.status_code, response.text)


def main():
    parser = argparse.ArgumentParser(prog='deepl', description='Call DeepL Free APIs.')
    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('translate', help='Request Translation')
    subparser.add_argument('-k', '--key', dest='auth_key', metavar='AUTH_KEY', type=str, default=None, help='auth key for DeepL')
    subparser.add_argument('--source', dest='source_lang', metavar='LANGUAGE', type=str, default='en', help='source language')
    subparser.add_argument('--target', dest='target_lang', metavar='LANGUAGE', type=str, default='ja', help='target language')
    subparser.add_argument('--glossary_id', dest='glossary_id', metavar='GLOSSARY', type=str, default=None, help='glossary id')
    subparser.add_argument('--text', dest='text', metavar='TEXT', type=str, required=True, help='text')
    subparser.set_defaults(handler=command_translate)

    subparser = subparsers.add_parser('glossary-language-pairs', help='List Language Pairs Supported by Glossaries')
    subparser.add_argument('-k', '--key', dest='auth_key', metavar='AUTH_KEY', type=str, default=None, help='auth key for DeepL')
    subparser.set_defaults(handler=command_glossary_language_pairs)

    subparser = subparsers.add_parser('create-glossary', help='Create a Glossary')
    subparser.add_argument('-k', '--key', dest='auth_key', metavar='AUTH_KEY', type=str, default=None, help='auth key for DeepL')
    subparser.add_argument('--source', dest='source_lang', metavar='LANGUAGE', type=str, default='en', help='source language')
    subparser.add_argument('--target', dest='target_lang', metavar='LANGUAGE', type=str, default='ja', help='target language')
    subparser.add_argument('--name', dest='name', metavar='NAME', type=str, required=True, help='glossaries name')
    group = subparser.add_mutually_exclusive_group(required=True)
    group.add_argument('--entries', dest='entries', metavar='ENTRIES', type=str, default=None, help='entries')
    group.add_argument(
        '--glossary_files', dest='glossary_files', metavar='GLOSSARIES', action='append', type=str, default=None, help='TSV glossary files'
    )
    subparser.add_argument('--entries_format', dest='entries_format', metavar='FORMAT', type=str, default='csv', help='entriesformat')
    subparser.set_defaults(handler=command_create_glossary)

    subparser = subparsers.add_parser('list-glossaries', help='List all Glossaries')
    subparser.add_argument('-k', '--key', dest='auth_key', metavar='AUTH_KEY', type=str, default=None, help='auth key for DeepL')
    subparser.set_defaults(handler=command_list_glossaries)

    subparser = subparsers.add_parser('retrieve-glossary', help='Retrieve Glossary Details')
    subparser.add_argument('-k', '--key', dest='auth_key', metavar='AUTH_KEY', type=str, default=None, help='auth key for DeepL')
    subparser.add_argument('--glossary_id', dest='glossary_id', metavar='GLOSSARY', type=str, required=True, help='glossary id')
    subparser.set_defaults(handler=command_retrieve_glossary)

    subparser = subparsers.add_parser('delete-glossary', help='Delete a Glossary')
    subparser.add_argument('-k', '--key', dest='auth_key', metavar='AUTH_KEY', type=str, default=None, help='auth key for DeepL')
    subparser.add_argument('--glossary_id', dest='glossary_id', metavar='GLOSSARY', type=str, required=True, help='glossary id')
    subparser.set_defaults(handler=command_delete_glossary)

    subparser = subparsers.add_parser('retrieve-glossary-entries', help='Retrieve Glossary Entries')
    subparser.add_argument('-k', '--key', dest='auth_key', metavar='AUTH_KEY', type=str, default=None, help='auth key for DeepL')
    subparser.add_argument('--glossary_id', dest='glossary_id', metavar='GLOSSARY', type=str, required=True, help='glossary id')
    subparser.set_defaults(handler=command_retrieve_glossary_entries)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        try:
            args.handler(args)
        except:
            parser.print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
