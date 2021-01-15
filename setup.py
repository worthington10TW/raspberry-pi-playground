from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='monitor',
    version='0.1.0',
    description='Build monitor GPIO',
    long_description=readme,
    author='Matthew Z Worthington',
    author_email='worthingtown@gmail.com',
    url='https://github.com/worthington10TW/raspberry-pi-playground',
    include_package_data=True,
    license=license,
    packages=find_packages(include=('monitor', 'monitor.*')),
    entry_points={
        'console_scripts': ['monitor=monitor.app:main'],
    },
    package_data={'': ['monitor/integrations.json']},
)
