from StringIO import StringIO
import code5
import sys
import random

def pattern_png(code='0-0-0-0-0'):
    c5 = code5.Code5()
    image_factory = None
    c5.add_data(code)
    img = c5.make_image(image_factory=image_factory)

    code_buffer = StringIO()
    img.save(code_buffer)
    code_buffer.seek(0)
    code_file = '%s.png'%code
    with open(code_file, "wb") as file_png:
        file_png.write(code_buffer.getvalue())
    code_buffer.close()

def random_draw():
    pattern = code5.Pattern()
    code = ''
    code = '%d-'%random.randint(0, 255)
    code += '%d-'%random.randint(0, 255)
    code += '%d-'%random.randint(0, 255)
    code += '%d-'%random.randint(0, 255)
    code += '%d'%random.randint(0, 255)
    print "The drawn code5 is %s."%code
    print "We should check that this code is available."
    print "If available then we update the user account model instance with this code."
    print "Now let's generate the png pattern"
    pattern_png(code)



if __name__ == '__main__':
    random_draw()


