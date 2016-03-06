from code5.main import Code5
from code5.main import Pattern

from code5 import image  # noqa


def tag(data=""):
    c5 = code5.Code5()

    image_factory = None

    c5.add_data(data)
    img = c5.make_image(image_factory=image_factory)

    return img

def run_example(data="9-167-38-71-178", *args, **kwargs):
    """
    Build an example Code5 Code and display it.

    There's an even easier way than the code here though: just use the ``make``
    shortcut.
    """
    cr = Code5(*args, **kwargs)
    cr.add_data(data)

    im = cr.make_image()
    im.show()


if __name__ == '__main__':
    import sys
    run_example(*sys.argv[1:])
