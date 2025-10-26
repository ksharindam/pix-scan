
from setuptools import setup

setup(
    name='pix-scan',
    packages=['pix_scan'],
    #version=__version__,
    entry_points={
        'console_scripts': ['pixscan=pix_scan.main:main'],
    },
    data_files=[
        ('share/applications', ['files/pix-scan.desktop']),
        ('share/icons/hicolor/scalable/apps', ['files/pix-scan.png'])
    ],
    include_package_data=True,
    zip_safe=False
)
