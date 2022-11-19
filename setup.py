from setuptools import find_namespace_packages, setup


setup(
    name='bartender',
    version='0.1.0',
    license='MIT',
    description='Annotated barplots in a nice grid',
    author='Heinz Eckert',
    author_email='heinzeckert6@gmail.com',
    packages=find_namespace_packages(),
    install_requires=[
        'matplotlib',
        'pandas'
    ]
)