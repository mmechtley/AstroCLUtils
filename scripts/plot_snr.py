#!/usr/bin/env python
"""
Plot signal-to-noise ratio image, given a set of science images and noise maps.
First half of command-line-arguments should be science images, second half noise
maps. Noise map names should contain 'ivm' or 'wht' to indicate inverse variance
maps, or 'rms' to indicate rms maps. Can also specify extesions, with ERR
extension interpreted as RMS error. Float arguments will be marked as contour
levels (in sigma)
With 'linearity' argument, Make a plot of SNR vs. signal, to assess where
linearity or poisson approximation ceases to apply.

Examples:
plot_snr.py sci*.fits ivm*.fits
plot_snr.py sci*.fits rms*.fits -1.5 1.5
plot_snr.py *flt.fits[SCI] *flt.fits[ERR]
plot_snr.py linearity sci*.fits ivm*.fits
"""
import numpy as np
from astropy.stats import biweight_location
from matplotlib import pyplot as pp
import sys
from astropy.io import fits
from matplotlib.colors import SymLogNorm


def parse_ext(imgstring):
    ext = 0
    if '[' in imgstring:
        imgstring, ext = imgstring[:-1].split('[')
        ext = ext.split(',')
        if len(ext) > 1:
            ext[1] = int(ext[1])
        else:
            ext += [1]
        ext = tuple(ext)
    return imgstring, ext


def plot_snr_image(img, ivm, levels=(-1.5, 1.5,)):
    img, imgext = parse_ext(img)
    ivm, ivmext = parse_ext(ivm)
    data = fits.getdata(img, ext=imgext)

    np.seterr(all='ignore')

    if 'ivm' in ivm or 'wh' in ivm or 'WHT' == ivmext:
        inv_noise = np.sqrt(fits.getdata(ivm, ext=ivmext))
    elif 'rms' in ivm or 'sig' in ivm or 'ERR' == ivmext:
        inv_noise = 1.0 / fits.getdata(ivm, ext=ivmext)
    else:
        print('Unknown weight map format {}'.format(ivm))
        return

    pp.figure()
    # Use linthresh=1 to go linear when we reach the sky noise
    norm = SymLogNorm(linthresh=1)
    pp.imshow(data * inv_noise, interpolation='nearest',
              origin='lower', norm=norm)
    cbar = pp.colorbar()
    ticks = norm.inverse(np.linspace(0, 1, 10))
    cbar.set_ticks(ticks)
    cbar.set_label('S/N')
    if len(levels) > 0:
        pp.contour(data * inv_noise, levels=levels, colors='black')
    pp.title(img)
    pp.show()


def plot_linearity(scifile, ivmfile):
    """
    Assumes sky-subtracted images in counts/sec and corresponding IVM
    :param scifile: science image file (cts/sec)
    :param ivmfile: inverse variance map
    """
    scih = fits.open(scifile)
    ivmh = fits.open(ivmfile)
    exptime = scih[0].header['EXPTIME']
    scidata = scih[0].data
    vardata = 1/ivmh[0].data
    skyvar = biweight_location(vardata)
    snr_cps = scidata / np.sqrt(vardata - skyvar)
    # Only plot pixels that are at least 2 sigma above sky
    mask = scidata > 2*np.sqrt(skyvar)
    pp.scatter(scidata[mask].flat, snr_cps[mask].flat,
               label='Predicted (Data*sqrt(Weight))')
    # Idealized (poisson) SNR model is SNR(cts) = sqrt(cts)
    x_ideal = np.linspace(0, scidata[mask].max(), 200)
    y_ideal = np.sqrt(x_ideal*exptime)
    pp.plot(x_ideal, y_ideal,
            label='Ideal (sqrt(Counts))')
    pp.xlabel('Signal (counts/sec)')
    pp.ylabel('SNR (sky variance subtracted)')
    pp.axis([x_ideal.min(), x_ideal.max(), y_ideal.min(), y_ideal.max()])
    pp.legend(loc='lower right')
    pp.show()
    scih.close()
    ivmh.close()
    return


if __name__ == '__main__':
    if 'help' in sys.argv or len(sys.argv) < 2:
        print(__doc__)
        exit(0)
    levels = []
    linearity = False
    for arg in sys.argv[::-1]:
        try:
            levels += [float(arg)]
            sys.argv.remove(arg)
            continue
        except ValueError:
            pass
        if arg == 'linearity':
            linearity = True
            sys.argv.remove(arg)
    levels = sorted(levels)

    files = sys.argv[1:]
    scis, ivms = files[0:len(files)//2], files[len(files)//2:]

    for sci, ivm in zip(scis, ivms):
        if linearity:
            plot_linearity(sci, ivm)
        else:
            plot_snr_image(sci, ivm, levels=levels)


