import scipy.cluster
import sklearn.cluster
import numpy
from PIL import Image
import binascii

def dominant_colors(filename):
    image = Image.open(filename)
    num_clusters = 10
    image = image.resize((150, 150))
    ar = numpy.asarray(image)
    shape = ar.shape
    if len(shape) < 3:
        return None
    print(filename, shape)
    ar = ar.reshape(numpy.product(shape[:2]), shape[2]).astype(float)
    kmeans = sklearn.cluster.KMeans(
        n_clusters=num_clusters,
        init="k-means++",
        max_iter=20,
        random_state=1000
    ).fit(ar)
    codes = kmeans.cluster_centers_
    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = numpy.histogram(vecs, len(codes))    # count occurrences
    colors = []
    for index in numpy.argsort(counts)[::-1]:
        colors.append(tuple([int(code) for code in codes[index]]))
    return colors

def hexcolor(color):
    return binascii.hexlify(bytearray(int(c) for c in color)).decode('ascii')
