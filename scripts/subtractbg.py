#!/usr/bin/env python
import matplotlib.pyplot as pp
import numpy as np
from astropy.io import fits
import scipy.stats


def estimate_bg(img_data, mask, clip_sig=3, n_clip=10, min_pix=50):
    # make a copy of the mask since we will modify it
    mask = mask.copy()
    pixels = img_data[~mask]
    clip_iter = 0
    mode, sig = 0, 1
    mask = np.ones(pixels.shape, dtype=bool)
    while True:
        # approximation of mode
        mu, med = np.mean(pixels[mask]), np.median(pixels[mask])
        mode = 3*med - 2*mu
        sig = np.std(pixels[mask])
        mask &= np.abs(pixels - med) < clip_sig * sig
        clip_iter += 1
        if np.sum(mask) < min_pix or clip_iter >= n_clip:
            break
    return mode, sig


def showhist(pixels, mode, sig):
    pp.hist(pixels, bins=np.linspace(mode-3*sig, mode+3*sig, 20), log=True)
    pp.axvline(mode)
    print(mode)
    pp.show()


def subtractbg(filename):
    f = fits.open(filename, mode='update')
    badval, counts = scipy.stats.mode(f[0].data, axis=None)
    badval = badval[0]
    if badval != 0:
        print('Warning: non-zero mode value found: {:0.3g}'.format(badval))
    badpx = f[0].data == badval

    mode, sig = estimate_bg(f[0].data, badpx)

    showhist(f[0].data[~badpx].flat, mode, sig)

    bg = float(input('BG level: '))

    f[0].data[~badpx] -= bg

    showhist(f[0].data[~badpx].flat, 0, sig)

    if 'y' in input('Save? '):
        f.flush()
    f.close()

if __name__ == '__main__':
    import sys
    import glob
    try:
        fs = sys.argv[1:]
    except IndexError:
        fs = glob.glob('sci_psf*.fits')
    for f in fs:
        subtractbg(f)
