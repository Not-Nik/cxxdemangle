# cxxdemangle (c) Nikolas Wipper 2022

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cxxdemangle",
    version="0.0.1b",
    author="Nikolas Wipper",
    #author_email="author@example.com",
    description="Demangling C++ names from the Itanium ABI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Not-Nik/cxxdemangle",
    packages=setuptools.find_packages(),
    license="MPL",
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Disassemblers'

        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.5',
)