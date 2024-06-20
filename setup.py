from setuptools import setup, find_packages

setup(
    name='snake',
    version='0.1',
    packages=find_packages(where='.', include=['snake*',]),
    package_dir={'': '.'},
)
