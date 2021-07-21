# Python tools for ProteoGenomics Analysis Toolkit


![Python application](https://github.com/bigbio/py-pgatk/workflows/Python%20application/badge.svg)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/pypgatk/README.html)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f6d030fd7d69413987f7265a01193324)](https://www.codacy.com/gh/bigbio/py-pgatk/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=bigbio/py-pgatk&amp;utm_campaign=Badge_Grade)
[![PyPI version](https://badge.fury.io/py/pypgatk.svg)](https://badge.fury.io/py/pypgatk)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pypgatk)

**pypgatk** is a Python library part of the [ProteoGenomics Analysis Toolkit](https://pgatk.readthedocs.io/en/latest). It provides different bioinformatics tools for proteogenomics data analysis.

**This is a private fork for the purposes of our project**

# Requirements:

This package requirements vary depending on the way that you want to install it (all three are independent, you don't need all these requirements):

- pip: if installation goes through pip, you will require Python3 and pip3 installed.
- Bioconda: if installation goes through Bioconda, you will require that [conda is installed and configured to use bioconda channels](https://bioconda.github.io/user/index.html).
- Docker container: to use pypgatk from its docker container you will need [Docker](https://docs.docker.com/install/) installed.
- Source code: to use and install from the source code directly, you will need to have git, Python3 and pip.

# Installation

## Use latest source code

Alternatively, for the latest version, clone this repo and go into its directory, then execute `pip3 install .` :

```
git clone https://github.com/ProGenNo/py-pgatk.git
cd py-pgatk
# you might want to create a virtualenv for pypgatk before installing
pip3 install .
```

# Usage

The pypgatk design combines multiple modules and tools into one framework. All the possible commands are accessible using the commandline tool `pypgatk_cli.py`.

```
$: pypgatk_cli.py -h
Usage: pypgatk_cli.py [OPTIONS] COMMAND [ARGS]...

  This is the main tool that give access to all commands and options
  provided by the pypgatk

Options:
  -h, --help  Show this message and exit.

Commands:
  cbioportal-downloader     Command to download the the cbioportal studies
  cbioportal-to-proteindb  Command to translate cbioportal mutation data into
                           proteindb
  cosmic-downloader        Command to download the cosmic mutation database
  cosmic-to-proteindb      Command to translate Cosmic mutation data into
                           proteindb
  dnaseq-to-proteindb      Generate peptides based on DNA sequences
  ensembl-downloader       Command to download the ensembl information
  generate-decoy           Create decoy protein sequences. Each protein is
                           reversed and the cleavage sites switched with
                           preceding amino acid. Peptides are checked for
                           existence in target sequences if foundthe tool will
                           attempt to shuffle them. James.Wright@sanger.ac.uk
                           2015
  threeframe-translation   Command to perform 3frame translation
  vcf-to-proteindb         Generate peptides based on DNA variants from
                           ENSEMBL VEP VCF files

```

The library provides multiple commands to download, translate and generate protein sequence databases from reference and mutation genome databases.

# Full Documentation

[https://pgatk.readthedocs.io/en/latest/pypgatk.html](https://pgatk.readthedocs.io/en/latest/pypgatk.html)

## Cite as
Yasset Perez-Riverol, & Husen M. Umer. (2021, February 3). bigbio/pypgatk: Pre-release v0.0.9 (Version v0.0.9). Zenodo. [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4499011.svg)](https://doi.org/10.5281/zenodo.4499011)

