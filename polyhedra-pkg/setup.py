from setuptools import setup, find_packages

setup(name='polyhedra',
        version='0.2',
        author='Franklin Pezzuti Dyer',
        author_email='franklin+polyhedra@dyer.me',
        packages=find_packages(exclude=['deprecated']),
        zip_safe=False)
