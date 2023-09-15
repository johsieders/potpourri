from setuptools import setup, find_packages  # Always prefer setuptools over distutils

setup(
    name='numbers',  # Required
    version='0.0.1',  # Required
    description='',  # Required
    package_dir={'modular arithmetic, polynomials and the like': 'src_'},
    packages=find_packages(where='src_'),  # Required
)
