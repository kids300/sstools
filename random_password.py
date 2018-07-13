import string
import sys
import json
import os
import argparse
import datetime
from datetime import date
import random

def id_generator(size=64, chars=string.ascii_uppercase + string.digits+ string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def generate_config(in_f, out):
    old = json.load(open(in_f,'r'))
    for port in old['port_password']:
        password = id_generator()
        old['port_password'][port] = password

    json.dump(old, open(out,'w+'), indent=2)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input', default=os.path.expanduser(
        '~/.shadowsocks/shadowsocks.json'))
    today = date.today()
    parser.add_argument('-o', dest='output', default="{:02d}{:02d}".format(today.month, today.day))

    opts = parser.parse_args(sys.argv[1:])
    opts.output = os.path.expanduser(os.path.join('~/.shadowsocks/'+opts.output+".json"))

    generate_config(opts.input, opts.output)

