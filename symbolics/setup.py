from setuptools import setup, find_packages  # Always prefer setuptools over distutils

setup(
    name='symbolics',  # Required
    version='0.0.1',  # Required
    description='',  # Required
    package_dir={'symbolic calculation': 'src'},
    packages=find_packages(where='src'),  # Required
)
