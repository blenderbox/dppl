class Pixelate(object):
    """ This is used by Imagekit as a processor which will pixelate the image.
    """
    def process(self, image):
        RESIZE_CO = 0.035

        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        psize = tuple([int(RESIZE_CO * x) for x in image.size])
        pixelated = image.resize(psize)
        pixelated = pixelated.resize(image.size)

        return pixelated
