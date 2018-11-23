"""Setup file for handling packaging and distribution."""
from __future__ import absolute_import

import os
from setuptools import setup, find_packages

__version__ = "0.1.0"

DIR = os.path.dirname(__file__)
with open(os.path.join(DIR, "README.md")) as f:
    long_description = f.read()

requirements = [
]

setup(
    name='network-simulator',
    version=__version__,
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    license="MIT",
    author="shefer",
    author_email="elran777@gmail.com",
    url="https://github.com/IamShobe/network_simulator",
    keywords="patch",
    install_requires=requirements,
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
    entry_points={},
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={'': ['*.xls', '*.xsd', '*.json', '*.css', '*.xml', '*.rst']},
    extras_require={
        'dev': [
            'attrdict',

        ],
    },
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
)
