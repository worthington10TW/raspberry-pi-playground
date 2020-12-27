from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='raspberry pi playground',
    version='0.1.0',
    description='Raspberry zero toy, maybe a build centre or something cool',
    long_description=readme,
    author='Matthew Z Worthington',
    author_email='worthingtown@gmail.com',
    url='https://github.com/worthington10TW/raspberry-pi-playground',
    license=license,
    packages=find_packages(exclude=('test', 'docs'))
)
