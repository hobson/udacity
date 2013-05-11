from __future__ import unicode_literals

import io
import os.path
import re
import subprocess
import urllib2

# This downloads, builds, and installs NumPy against the MKL in the
# currently active virtualenv

file_name = 'numpy-1.6.2.tar.gz'
url = ('http://sourceforge.net/projects/numpy/files/NumPy/1.6.2/'
       'numpy-1.6.2.tar.gz/download')

def main():

    # download NumPy and unpack it
    file_data = urllib2.urlopen(url).read()
    with io.open(file_name, 'wb') as fobj:
        fobj.write(file_data)
    subprocess.check_call('tar -xvf {0}'.format(file_name), shell=True)
    base_name = re.search(r'(.*)\.tar\.gz$', file_name).group(1)
    os.chdir(base_name)

    # write out a site.cfg file in the build directory
    site_cfg = (
        '[mkl]\n'
        'library_dirs = /opt/intel/composer_xe_2013.1.117/mkl/lib/intel64\n'
        'include_dirs = /opt/intel/composer_xe_2013.1.117/mkl/include\n'
        'mkl_libs = mkl_rt\n'
        'lapack_libs =\n')
    with io.open('site.cfg', 'wt', encoding='UTF-8') as fobj:
        fobj.write(site_cfg)

    # build and install NumPy
    subprocess.check_call('python setup.py build', shell=True)
    subprocess.check_call('python setup.py install', shell=True)


if __name__ == '__main__':
    main()
