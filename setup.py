from distutils.core import setup
from Cython.Build import cythonize
import numpy as np
from os.path import join, exists
from os import mkdir
from shutil import move
import tarfile
from urllib.request import Request, urlopen
from glob import glob

# make dependency directory
if not exists('deps'):
    mkdir('deps')

# download Eigen if we don't have it in deps
eigenurl = 'https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.gz'
eigentarpath = join('deps', 'Eigen.tar.gz')
eigenpath = join('deps', 'Eigen')
if not exists(eigenpath):
    print('Downloading Eigen...')
    req = Request(eigenurl, headers={'User-Agent': 'XYZ/3.0'})
    tar_data = webpage = urlopen(req, timeout=10).read()
    with open(eigentarpath, 'wb') as f:
        f.write(tar_data)

    with tarfile.open(eigentarpath, 'r') as tar:
        tar.extractall('deps')
    thedir = glob(join('deps', 'eigen-*'))[0]
    move(join(thedir, 'Eigen'), eigenpath)
    print('...done!')

setup(
    name='autoregressive',
    version='0.1.2',
    description='Extension for switching vector autoregressive models with pyhsmm',
    author='Matthew James Johnson',
    author_email='mattjj@csail.mit.edu',
    url='https://github.com/mattjj/pyhsmm-autoregressive',
    license='GPL',
    packages=['autoregressive'],
    keywords=[
        'bayesian', 'inference', 'mcmc', 'time-series',
        'autoregressive', 'var', 'svar'],
    install_requires=[
        'Cython >= 0.20.1',
        'numpy', 'scipy', 'matplotlib', 'pybasicbayes >= 0.2.1', 'pyhsmm'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: C++'],
    ext_modules=cythonize('**/*.pyx'),
    include_dirs=[np.get_include(), 'deps']
)
