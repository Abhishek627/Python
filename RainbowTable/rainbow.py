import os
import time
import argparse
import hashlib
import sqlite3
from pathlib import Path


# Globals

# TABLE[last] = first
TABLE = {}
ALGORITHM = 'md5'
CHAIN_LENGTH = 4
REDUCTION_LENGTH = 8


def _reduce(i, h):
    # hint = (int(h, 16) + i) % (2 ** REDUCTION_LENGTH)
    # return hex(hint)[2:]
    return h[: REDUCTION_LENGTH]


def _hash(t, algo):
    if algo == 'sha1':
        hasher = hashlib.sha1(t.encode())
    elif algo == 'sha256':
        hasher = hashlib.sha256(t.encode())
    elif algo == 'sha512':
        hasher = hashlib.sha512(t.encode())
    else:
        hasher = hashlib.md5(t.encode())

    return hasher.hexdigest()


def create_chain(word):
    chain = [word]
    for i in range(CHAIN_LENGTH):
        h = _hash(word, ALGORITHM)
        chain.append(h)
        word = _reduce(i, h)
        chain.append(word)

    TABLE[chain[-1]] = chain[0]


def create_table(words):
    for word in words:
        create_chain(word)


def store_table():

    if not os.path.exists('./database/'):
        os.mkdir('database')

    conn = sqlite3.connect('./database/rainbow_table.db')
    conn.execute(
        "CREATE TABLE IF NOT EXISTS HashTable(first TEXT, last TEXT);")

    for k, v in TABLE.items():
        conn.execute("INSERT INTO HashTable VALUES (?,?)", (v, k))

    # Store Chain length and Reduction length used to create Rainbow table
    conn.execute(
        "CREATE TABLE IF NOT EXISTS MetaHashTable(reduction INTEGER, chain INTEGER, algo TEXT);")
    conn.execute("INSERT INTO MetaHashTable VALUES (?,?,?)",
                 (REDUCTION_LENGTH, CHAIN_LENGTH, ALGORITHM))

    conn.commit()
    conn.close()
    print('Created Rainbow table with the following configurations:')
    print('Chain length:      ', CHAIN_LENGTH)
    print('Reduction length:  ', REDUCTION_LENGTH)
    print('Algorithm:         ', ALGORITHM)
    print()


def crack_hash(h):

    if not os.path.exists('./database/'):
        os.mkdir('database')

    conn = sqlite3.connect('./database/rainbow_table.db')
    c = conn.cursor()

    try:
        c.execute("SELECT first, last from HashTable;")
    except Exception as e:
        print(e)
        return

    TABLE.clear()
    for first, last in c:
        TABLE[last] = first

    try:
        c.execute("SELECT reduction, chain, algo from MetaHashTable;")
    except Exception as e:
        print(e)
        return

    for r, _c, a in c:
        global REDUCTION_LENGTH, CHAIN_LENGTH, ALGORITHM
        REDUCTION_LENGTH = r
        CHAIN_LENGTH = _c
        ALGORITHM = a

    c.close()
    conn.commit()
    conn.close()

    flag = False
    plain_text, hash_to_be_cracked = None, h
    for i in range(CHAIN_LENGTH):
        r = _reduce(i, h)
        if r in TABLE:
            flag = True
            plain_text = r
            break
        h = _hash(r, ALGORITHM)

    if flag:
        text = TABLE[plain_text]
        for i in range(CHAIN_LENGTH):
            h = _hash(text, ALGORITHM)
            if hash_to_be_cracked == h:
                print('[200] Password found:', text)
                return
            text = _reduce(i, h)

    print('[404] Password not found')


def get_hash(word):
    print('MD5:\t', _hash(word, 'md5'))
    print('SHA1:\t', _hash(word, 'sha1'))
    print('SHA256:\t', _hash(word, 'sha256'))
    print('SHA512:\t', _hash(word, 'sha512'))
    print()


terminal_banner = '''
 ____       _       _                      ____                _    
|  _ \ __ _(_)_ __ | |__   _____      __  / ___|_ __ __ _  ___| | __
| |_) / _` | | '_ \| '_ \ / _ \ \ /\ / / | |   | '__/ _` |/ __| |/ /
|  _ < (_| | | | | | |_) | (_) \ V  V /  | |___| | | (_| | (__|   < 
|_| \_\__,_|_|_| |_|_.__/ \___/ \_/\_/    \____|_|  \__,_|\___|_|\_\
                                                                    
'''
print(terminal_banner)

parser = argparse.ArgumentParser(
    description='A tool to crack md5, sha1, sha256, sha512 hashes by using the Rainbow table approach.')
parser.add_argument('-f', '--file', type=str,
                    help='File containing words to be hashed')
parser.add_argument('-a', '--algo', type=str,
                    help='Enter algorithm (md5, sha1, sha256, sha512)')
parser.add_argument('-cl', '--chainLength', type=int,
                    help='Enter chain length while reduction')
parser.add_argument('-rl', '--reductionLength', type=int,
                    help='Enter reduction length')
parser.add_argument('-w', '--word', type=str,
                    help='Get hash value for input word')
parser.add_argument('-c', '--crack', type=str,
                    help='Enter hash to be cracked')
group = parser.add_mutually_exclusive_group()
group.add_argument('-i', '--info', action='store_true',
                   help='Get configuration of created Rainbow table or current configuration')

args = parser.parse_args()


def main():
    # If no parameters are passed
    if all([v == None for _, v in args._get_kwargs()]):
        print('Oops, Nothing to do :(')
        print('Try -h, --help flag')
        return

    if args.chainLength:
        global CHAIN_LENGTH
        CHAIN_LENGTH = args.chainLength

    if args.reductionLength:
        global REDUCTION_LENGTH
        REDUCTION_LENGTH = args.reductionLength

    if args.algo:
        global ALGORITHM
        ALGORITHM = args.algo

    if args.info:
        if Path('./database/rainbow_table.db').is_file():
            conn = sqlite3.connect('./database/rainbow_table.db')
            c = conn.cursor()
            c.execute("SELECT reduction, chain, algo from MetaHashTable;")

            for r, _c, a in c:
                REDUCTION_LENGTH = r
                CHAIN_LENGTH = _c
                ALGORITHM = a

        print('Current configuration:')
        print('Chain length:      ', CHAIN_LENGTH)
        print('Reduction length:  ', REDUCTION_LENGTH)
        print('Algorithm:         ', ALGORITHM)
        print()

    if args.file:
        file = Path(args.file)
        if file.is_file():
            words = open(args.file).readlines()
            words = [word.strip().lower()
                     for word in words if len(word.strip()) > 0]

            create_table(words)
            tic = time.time()
            store_table()
            tac = time.time()
            print('Took', tac - tic, 'seconds to create Rainbow table.')
        else:
            print('[404] File not found')

    if args.crack:
        crack_hash(args.crack)

    if args.word:
        get_hash(args.word)


if __name__ == '__main__':
    main()
