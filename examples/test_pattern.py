# -*- coding: utf-8 -*-
from StringIO import StringIO
import code5
import sys
import random
import json

def encode(code=''):
    pattern = code5.Pattern()
    if '-' in code:
        # multi encode
        if len(code.split('-')) != 5:
            print "Error: Format should be x-x-x-x-x"
        else:
            part_code = code.split('-')
            c1 = int(part_code[0])
            c2 = int(part_code[1])
            c3 = int(part_code[2])
            c4 = int(part_code[3])
            c5 = int(part_code[4])
            if (c1 < 0 or c1 > 255) or (c2 < 0 or c2 > 255) or (c3 < 0 or c3 > 255) or (c4 < 0 or c4 > 255) or (c5 < 0 or c5 > 255):
                print "Error: Each block should be betweeb 0-255."
            else:
                lines = pattern.encode([c1,c2,c3,c4,c5])
                print "Result -----"
                for line in lines:
                    print line
                print "----- Result"

    else:
        # single encode
        lines = pattern.encode_single(int(code))
        print "Result -----"
        for line in lines:
            print line
        print "----- Result"

def decode(lines=[]):
    pattern = code5.Pattern()
    print str(lines)
    if len(lines) == 3:
        # single decode
        code = pattern.decode_single(lines)
        print "Result -----"
        print code
        print "----- Result"
    elif len(lines) == 9:
        # multi decode
        code = pattern.decode_2(lines)
        print "Result -----"
        print code
        print "----- Result"
    else:
        print "Unknown pattern size: 3 lines for single decode and 9 lines for full code."


def alphabet():
    pattern = code5.Pattern()
    print "Result -----"
    pattern.possibilities(True)
    print "----- Result"



if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--alp': # alphabet
            alphabet()
        elif sys.argv[1] == '--help': # encode
            print "--enc: encoding a code into a pattern"
            print "--dec: decoding a pattern into a code"
            print "--alp: printing the code5 alphabet"
        else:
            if len(sys.argv) > 2:
                if sys.argv[1] == '--enc': # encode
                    encode(sys.argv[2])
                elif sys.argv[1] == '--dec': # decode
                    try:
                        content = ""
                        with open(sys.argv[2], 'r') as pattern_file:
                            content = pattern_file.read()
                        print str(content)
                        decode(content.decode('UTF-8').split("\n"))
                    except:
                        print "Error: Commands dec required a json content file as second argument."
                else:
                    print "Error: Command not supported [--help, --alp, --dec, --enc]"
            else:
                print "Error: Commands enc and dec required a second argument."



