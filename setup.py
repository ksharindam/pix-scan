
from setuptools import setup
from pix_scan import __version__

setup(
    name='pix-scan',
    packages=['pix_scan'],
    version=__version__,
    description='Simple scanimage frontend for HP Scanners',
    keywords='pyqt pyqt4 scan',
    url='http://github.com/ksharindam/pix-scan',
    author='Arindam Chaudhuri',
    author_email='ksharindam@gmail.com',
    license='GNU GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': ['pixscan=pix_scan.main:main'],
    },
    data_files=[
        ('share/applications', ['files/pix-scan.desktop']),
        ('share/icons', ['files/pix-scan.png'])
    ],
    include_package_data=True,
    zip_safe=False
)
