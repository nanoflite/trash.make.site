from PIL import Image
import hitherdither

def dither(src, dst, image_size=(640,640)):
    dither_palette = [(25,25,25), (75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250)] # 6 tone palette
    threshold = [96, 96, 96]
    img = Image.open(src).convert('RGB')
    img.thumbnail(image_size, Image.LANCZOS)
    palette = hitherdither.palette.Palette(dither_palette)
    dithered = hitherdither.ordered.bayer.bayer_dithering(img, palette, threshold, order=8)
    dithered.save(dst)