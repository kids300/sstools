#!/usr/bin/env python

from __future__ import print_function

import errno
import base64
import json
import sys
import os
import qrcode
from qrcode.image.pure import PymagingImage
import argparse
savepath = "/home/yan/Downloads/ssqr"


def make_sure_path_exists(p):
    #    p = os.path.dirname(path)
    try:
        os.makedirs(p)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def generate_qr(method, password, server, port): #result, append):
    result = '{}:{}@{}:{}'.format(method, password, server, port)
    old_result = result
    append = '{}'.format(port)
    localsavepath = os.path.join(savepath,port)
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
    )
    make_sure_path_exists(localsavepath)

    result = base64.b64encode(result.encode('ascii')).decode('ascii')
    result = "ss://" + result  
    qr.add_data(result)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(os.path.join(localsavepath, 'qr.png'))
    with open(os.path.join(localsavepath, 'url.txt'),'w') as f:
        f.write(old_result+'\n')
        f.write(result+'\n')
    return img, old_result, result

def main(opts):
    args = json.load(open(opts.input, 'r'))
    if 'port_password' in args:
        for port, password in args['port_password'].items():
            generate_qr(args['method'], password, args['server'], port)
    else:
        generate_qr((args['method'], args['password'], args['server'], args['port']))
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input', default='/etc/shadowsocks.json')
    args = parser.parse_args(sys.argv[1:])
    main(args)
