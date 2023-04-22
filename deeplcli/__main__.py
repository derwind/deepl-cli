'''A CLI for DeepL APIs'''

import argparse
from .deepl import translate, glossary_language_pairs, create_glossary, list_glossaries, retrieve_glossary, delete_glossary, retrieve_glossary_entries


def command_translate(args):
    '''Request Translation'''

    result = translate(args.source_lang, args.target_lang, args.text, args.glossary_id, args.auth_key)
    if result is not None:
        print(result)


def command_glossary_language_pairs(args):
    '''List Language Pairs Supported by Glossaries'''

    result = glossary_language_pairs(args.auth_key)
    if result is not None:
        print(result)


def command_create_glossary(args):
    '''Create a Glossary'''

    result = create_glossary(args.source_lang, args.target_lang, args.name, args.entries, args.glossary_files, args.entries_format, args.auth_key)
    if result is not None:
        print(result)


def command_list_glossaries(args):
    '''List all Glossaries'''

    result = list_glossaries(args.auth_key)
    if result is not None:
        print(result)


def command_retrieve_glossary(args):
    '''Retrieve Glossary Details'''

    result = retrieve_glossary(args.glossary_id, args.auth_key)
    if result is not None:
        print(result)


def command_delete_glossary(args):
    '''Delete a Glossary'''

    result = delete_glossary(args.glossary_id, args.auth_key)
    if result is not None:
        print(result)


def command_retrieve_glossary_entries(args):
    '''Retrieve Glossary Entries'''

    result = retrieve_glossary_entries(args.glossary_id, args.auth_key)
    if result is not None:
        print(result)


def main():
    '''Entrypoint'''

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
        '--glossary_files', dest='glossary_files', metavar='GLOSSARIES', action='append', type=str, default=[], help='TSV glossary files'
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
        args.handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
