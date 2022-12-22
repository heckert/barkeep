import pathlib
from setuptools import find_namespace_packages, setup


with pathlib.Path("./requirements.txt").open() as f:
    install_requires = [
        str(requirement) for requirement in f
    ]

setup(
    name='barkeep',
    version='0.1.0',
    license='MIT',
    description='Annotated barplots in a nice grid',
    author='Heinz Eckert',
    author_email='heinzeckert6@gmail.com',
    packages=find_namespace_packages(include=['barkeep', 'barkeep.*']),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=install_requires
)
