import os

from setuptools import setup


def package_files(directory):
    paths = []
    for path, directories, file_names in os.walk(directory):
        for filename in file_names:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('elo')

setup(
    name = 'elo',
    version = '1.0',
    packages = ['elo'],
    package_data = {'': extra_files},
)
