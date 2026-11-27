
from setuptools import setup

setup(
    name='pix-scan',
    packages=['pix_scan'],
    #version=__version__,
    entry_points={
        'gui_scripts': ['pixscan=pix_scan.main:main'],
    },
    data_files=[
        ('share/applications', ['data/pix-scan.desktop']),
        ('share/icons/hicolor/scalable/apps', ['data/pix-scan.png'])
    ],
    include_package_data=True,
    zip_safe=False
)
