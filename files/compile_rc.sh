#!/bin/bash
cd ..
pyrcc5 -o pix_scan/resources_rc.py files/resources.qrc
sed -i -e "s/PyQt5/PyQt4/g" pix_scan/resources_rc.py
