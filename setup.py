import os

from setuptools import (
    find_packages,
    setup
)


with open(os.path.join('requirements.txt'), 'r') as f:
    REQUIRED_PACKAGES = f.readlines()


packages = find_packages()


setup(
    name='peertax',
    version='0.0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=packages,
    include_package_data=True,
    description='Data Science project looking into the Peer Review Taxonomy'
)
