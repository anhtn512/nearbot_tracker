import json
from base64 import b64decode

def convert_deposit(amount):
    n = int(amount)/pow(10, 24)
    return str(n)

def handle_base64(str_b64):
    temp = b64decode(str_b64)
    try:
        temp = temp.decode('utf-8')
    except:
        print(temp)
    return temp


def markdown_parser(text):
    special_characters = ['\\','_','*','[',']','(',')','~','`','>','<','&','#','+','-','=','|','{','}','.','!']
    for i in special_characters:
        text = text.replace(i, '\\{}'.format(i))
    return text


def create_linkhash(hash):
    short_hash = '\.\.\.' + hash[-6:]
    link = 'https://testnet.nearblocks.io/txns/{}'.format(hash)
    message = '[{}]({})'.format(short_hash, link)
    return message


def extract_action(tx):
    return tx['actions']


def handle_transaction(tx):
    message = 'Hash: {}\n'.format(create_linkhash(tx['hash']))
    actions = extract_action(tx)
    for action in actions:
        message = message + '`---------------`\n'
        message = message + handle_action(tx, action)
    return message


def handle_action(tx, action):
    if type(action) == 'str' and action == 'CreateAccount':
        message_addon = handle_CreateAccount(tx, action)
        return message_addon
    action_type = list(action.keys())[0]
    action_detail = action[action_type]
    message_addon = ''
    if action_type == 'FunctionCall':
        message_addon = handle_FunctionCall(tx, action_detail)
    if action_type == 'Transfer':
        message_addon = handle_Transfer(tx, action_detail)
    if action_type == 'DeleteAccount':
        message_addon = handle_DeleteAccount(tx, action_detail)
    if action_type == 'AddKey':
        message_addon = handle_AddKey(tx, action_detail)
    if action_type == 'DeleteKey':
        message_addon = handle_DeleteKey(tx, action_detail)
    return message_addon


def handle_args(args):
    args_str = handle_base64(args)
    return json.loads(args_str)


def handle_FunctionCall(tx, action_detail):
    # Sample
    # {
    #     "actions": [{
    #         "FunctionCall": {
    #             "args": "eyJzaWduYXR1cmVfdmVyaWZpZWRfZGF0YSI6eyJvcGVyYXRvcl9hY3Rpb25fZGF0YSI6eyJQZXJwTWFya2V0SW5mbyI6eyJpbmZvIjp7IlBlcnBQcmljZSI6eyJtYXhfdGltZXN0YW1wIjoxNjg3NTQ0ODg3MDAwLCJwZXJwX3ByaWNlcyI6W3siaW5kZXhfcHJpY2UiOiIxOTExMzcwMDAwMDAiLCJtYXJrX3ByaWNlIjoiMTg1NDAzMDAwMDAwIiwic3ltYm9sIjoiUEVSUF9FVEhfVVNEQyIsInRpbWVzdGFtcCI6MTY4NzU0NDg4NzAwMH0seyJpbmRleF9wcmljZSI6IjEzOTcyMDAwMCIsIm1hcmtfcHJpY2UiOiIxMzk3MzAwMDAiLCJzeW1ib2wiOiJQRVJQX05FQVJfVVNEQyIsInRpbWVzdGFtcCI6MTY4NzU0NDg4NzAwMH0seyJpbmRleF9wcmljZSI6IjMxMDE2NTcwMDAwMDAiLCJtYXJrX3ByaWNlIjoiMzAwODYxMDAwMDAwMCIsInN5bWJvbCI6IlBFUlBfQlRDX1VTREMiLCJ0aW1lc3RhbXAiOjE2ODc1NDQ4ODcwMDB9XX19fX0sInNpZ25hdHVyZSI6ImQ0YmVkNTM3MjdjYzI4YzFlMGY5ZjhhNjQ2YmE5YTZiYTliNDBkZmM4NDkyOWE3MmNjNGM0NDQ0MmUxNDliNDczMDdkZjAyODM2M2FkODE5Y2QzMmVjODFjMGYxNTVhMmNjMmVmYzhkZmZhZjYwNWI2NjIzZTAxMzBiZmZjMjMyMDEifX0=",
    #             "deposit": "0",
    #             "gas": 300000000000000,
    #             "method_name": "operator_execute_action"
    #         }
    #     }],
    #     "hash": "DhBdk6qz37bz7espR5Sbmxoi9StwaebqkJEBnSsMV8GH",
    #     "nonce": 104241976440952,
    #     "public_key": "ed25519:76yqnWXyYSQqN8vbepVLmb5ojRE8ZqDpa4gw4BeTiFyL",
    #     "receiver_id": "asset-manager.orderly.testnet",
    #     "signature": "ed25519:3Y1RpkFk37U7sfn4QhWmYM8BgRYk5LUTzugoQ647tjm4NcHpVhD4ReyZ8mBRQXKquAtom2aq3vaK1oHWK6Nt9X9q",
    #     "signer_id": "operator_manager.orderly.testnet"
    # }
    signer_id = markdown_parser(tx['signer_id'])
    receiver_id = markdown_parser(tx['receiver_id'])
    method_name = markdown_parser(action_detail['method_name'])
    args = markdown_parser(json.dumps(handle_args(action_detail['args']), indent=2))
    message = '*{}* call method _{}_ in *{}*\n'.format(signer_id, method_name, receiver_id)
    message = message + 'Args:\n'
    message = message + '```\n{}\n```\n'.format(args)
    message = message + 'Gas: {}\n'.format(action_detail['gas'])
    return message


def handle_CreateAccount(tx, action_detail):
    # Sample
    # {
    #     "actions": ["CreateAccount", {
    #         "Transfer": {
    #             "deposit": "200000001000000000000000000"
    #         }
    #     }, {
    #                     "AddKey": {
    #                         "access_key": {
    #                             "nonce": 0,
    #                             "permission": "FullAccess"
    #                         },
    #                         "public_key": "ed25519:3bbC12RxzwmZvBAc8K3AnWXuBDSENAcoindG3eUJsHx1"
    #                     }
    #                 }],
    #     "hash": "HwhgwRnEPp48Y3KWwBnZcUXH1WsRbvf7bpBu78CsYde5",
    #     "nonce": 51910588196210,
    #     "public_key": "ed25519:4XhhXfW316DeAYBTxQe7Z15WostJptFpnXdv57KtXVNC",
    #     "receiver_id": "temp-1687544893400.testnet",
    #     "signature": "ed25519:5Vx5dWMFWnJKWC4pD424tscDYEkPgeiRLA3fEz2383utXEt8a9FzTGdgMGmuKyRFdVweU9a7bsv855qq4CPRr9ff",
    #     "signer_id": "testnet"
    # }
    receiver_id = markdown_parser(tx['receiver_id'])
    message = 'New account - _{}_ created\n'.format(receiver_id)
    return message


def handle_Transfer(tx, action_detail):
    # Sample
    # {
    #     "actions": [{
    #         "Transfer": {
    #             "deposit": "199000000000000000000000000"
    #         }
    #     }],
    #     "hash": "GhjHNkVPeDtbkRvrawUe5mtidHXLfvdUXdw98gYYCW4S",
    #     "nonce": 129884549000001,
    #     "public_key": "ed25519:HMjdMV1kmc53KPP4GdyfFFd1J9TvBW9DetmFhjHy57Mk",
    #     "receiver_id": "tqsang.testnet",
    #     "signature": "ed25519:2FD5Nnbac2eQsHCzC7SR7NALG3NVgrgCuGP4ARuuAmiPPgK8NMwdCCih9vcrn4sZvnYtvBc4tUPinn5D1PMvMn6W",
    #     "signer_id": "acaftwmdvjnk7s9wzrbz5daym.testnet"
    # }
    signer_id = markdown_parser(tx['signer_id'])
    receiver_id = markdown_parser(tx['receiver_id'])
    deposit = markdown_parser(convert_deposit(action_detail['deposit']))
    message = '*{}* transfer _{}N_ to *{}*\n'.format(signer_id, deposit, receiver_id)
    return message


def handle_DeleteAccount(tx, action_detail):
    # Sample
    # {
    #     "actions": [{
    #         "DeleteAccount": {
    #             "beneficiary_id": "comicdeer.testnet"
    #         }
    #     }],
    #     "hash": "AonKKcjdNriRPN8fY8g8PWhKGhi4UragjKQNebRjJ17z",
    #     "nonce": 129884575000001,
    #     "public_key": "ed25519:3bbC12RxzwmZvBAc8K3AnWXuBDSENAcoindG3eUJsHx1",
    #     "receiver_id": "temp-1687544893400.testnet",
    #     "signature": "ed25519:2xkFmykhBTp5ab52fi3ayVkzjvpvFyWx4nvoxf1MaQP3QErvLsq3bUpw4DY7DKKSgMvgE5MZBGmn6tMFkmtHyVqM",
    #     "signer_id": "temp-1687544893400.testnet"
    # }
    signer_id = markdown_parser(tx['signer_id'])
    receiver_id = markdown_parser(tx['receiver_id'])
    beneficiary_id = markdown_parser(action_detail['beneficiary_id'])
    message = '*{}* delete account _{}_ and transfer remaining funds to *{}*\n'.format(signer_id, receiver_id, beneficiary_id)
    return message


def handle_AddKey(tx, action_detail):
    # Sample
    # {
    #     "actions": [{
    #         "AddKey": {
    #             "access_key": {
    #                 "nonce": 0,
    #                 "permission": "FullAccess"
    #             },
    #             "public_key": "ed25519:8x8nVen34Jxbgdnz5uwJk6X3WDdzcnsgKWdEkgVF1pxy"
    #         }
    #     }],
    #     "hash": "AKFFaLTJLSecR6UCY9dmttZrHyMgtqcttkmGBz4X6Qwk",
    #     "nonce": 129885132000001,
    #     "public_key": "ed25519:ChZpNefiimjWhdhBw3kx3uBXNFNuzV9M2S4TXVK6VYkf",
    #     "receiver_id": "a0gs9a2hfa27ue8xbwsbgn1pd.testnet",
    #     "signature": "ed25519:45D57iCjUKxdUB1BZoTfDmD5HdCvtZ4pqgATtquUKXyvr4eCTN9ChkygkL4vapkJ6SJWLXYnWyrYpRoNgtatdyS",
    #     "signer_id": "a0gs9a2hfa27ue8xbwsbgn1pd.testnet"
    # }
    receiver_id = markdown_parser(tx['receiver_id'])
    permission = markdown_parser(action_detail['access_key']['permission'])
    public_key = markdown_parser(action_detail['public_key'])
    message = 'New key added for *{}* with _{}_\n'.format(receiver_id, permission)
    message = message + 'Public key: {}\n'.format(public_key)
    return message


def handle_DeleteKey(tx, action_detail):
    # Sample
    # {
    #     "actions": [{
    #         "DeleteKey": {
    #             "public_key": "ed25519:5mMypYnvPGUV7i1vij385Qgb3cMyC18sHUvgLeQ39iDq"
    #         }
    #     }],
    #     "hash": "9FPj4NYDimoMiDcv52iN9D7pJJccRoz5Lh85sPiYcGgB",
    #     "nonce": 127748008000017,
    #     "public_key": "ed25519:7SpHsJAVDWFu8X6XE5d4cMvi4yM2d51a7CZftqYKCNe3",
    #     "receiver_id": "prenku4.testnet",
    #     "signature": "ed25519:34NiNvEiqAQThLRJipW5b5c3p6pDRhxP9FM3N5CVMG8B1f5ZH5DH9KxqdGW4w1XHEiaBQZJHc8YjPabNajiQN5hF",
    #     "signer_id": "prenku4.testnet"
    # }
    signer_id = markdown_parser(tx['signer_id'])
    public_key = markdown_parser(action_detail['public_key'])
    message = '*{}* has deleted a key\n'.format(signer_id)
    message = message + 'Public key: {}\n'.format(public_key)
    return message