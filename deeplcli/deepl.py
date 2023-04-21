import argparse
import requests
import json


def command_translate(args):
    url = 'https://api-free.deepl.com/v2/translate'

    params = {'auth_key': args.auth_key, 'text': args.text, 'target_lang': args.target_lang}

    response = requests.post(url, data=params)

    if response.ok:
        result = json.loads(response.content.decode('utf-8'))
        print(result['translations'][0]['text'])
        # print(result['translations'])
    else:
        print("Error: ", response.status_code, response.text)


def main():
    parser = argparse.ArgumentParser(prog='deepl')
    subparsers = parser.add_subparsers()

    parser_translate = subparsers.add_parser('translate', help='translate texts')
    parser_translate.add_argument('-k', '--key', dest='auth_key', metavar='AUTH_KEY', type=str, default=None, help='auth key for DeepL')
    parser_translate.add_argument('--target', dest='target_lang', metavar='LANGUAGE', type=str, default='JA', help='target language')
    parser_translate.add_argument('--text', dest='text', metavar='TEXT', type=str, required=True, help='text')
    parser_translate.set_defaults(handler=command_translate)

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
