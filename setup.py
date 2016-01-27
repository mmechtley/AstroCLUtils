from distutils.core import setup

setup(
    name='AstroCLUtils',
    version='1.0',
    packages=[''],
    url='',
    license='BSD',
    author='Matt Mechtley',
    author_email='',
    description='Command-line astronomy utilities',
    requires=['numpy', 'astropy', 'matplotlib', 'scipy'],
    scripts=['scripts/ds9_with_regions.py', 'scripts/exiraf.py',
             'scripts/strip_drizzle_keys.py', 'scripts/subtractbg.py',
             'scripts/plot_snr.py']
)
