#!/usr/bin/env python
"""
code5 - Convert stdin (or the first argument) to a Code5 Code.

When stdout is a tty the Code5 Code is printed to the terminal and when stdout is
a pipe to a file an image is written. The default image format is PNG.
"""
import sys
import optparse
import os
import code5


def main(args=sys.argv[1:]):
    parser = optparse.OptionParser(usage=__doc__.strip())
    opts, args = parser.parse_args(args)

    c5 = code5.Code5()

    image_factory = None

    decode = False
    alphabet = False

    if args:
        data = ''
        if args[0] == 'alphabet':
            alphabet = True
        else:
            if '.png' in args[0]:
                decode = True
                data = args[0]
            else:
                try:
                    with open(args[0], 'r') as data_file:
                        data = data_file.read()
                    data = data.replace('\n',',')
                except:
                    data = args[0]
    else:
        stdin_buffer = getattr(sys.stdin, 'buffer', sys.stdin)
        data = stdin_buffer.read()
        if args[0] == 'alphabet':
            alphabet = True
        else:
            if '.png' in args[0]:
                decode = True
                data = args[0]
            else:
                try:
                    with open(args[0], 'r') as data_file:
                        data = data_file.read()
                    data = data.replace('\n',',')
                except:
                    data = args[0]

    if alphabet:
        c5.dump_alphabet(image_factory=image_factory)
    else:
        if not decode:
            blocks = data.split(',')

            for block in blocks:
                c5.add_data(block)
                img = c5.make_image(image_factory=image_factory)

                with open('debug.txt', 'w') as debug_file:
                    debug_file.write(c5.UR+'\n')
                    debug_file.write(c5.C+'\n')
                    debug_file.write(c5.DL+'\n')
                    debug_file.write(c5.DR+'\n')

                try:
                    img.save_to_path('%s.png'%block, format=None)
                except:
                    img.save('%s.png'%block)
        else:
            result = c5.revert(image_factory=image_factory, image_path=data)
            with open('debug.txt', 'w') as debug_file:
                    debug_file.write(c5.log)
            with open('result.txt', 'w') as result_file:
                result_file.write(result)


if __name__ == "__main__":
    main()
