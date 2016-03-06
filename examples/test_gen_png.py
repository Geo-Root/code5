from StringIO import StringIO
import code5
import sys

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


if __name__ == '__main__':
	if len(sys.argv) > 1:
		code = sys.argv[1]
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
				pattern_png(code)
	else:
		print "Error: Prove code as python test_gen_png.py x-x-x-x-x"


