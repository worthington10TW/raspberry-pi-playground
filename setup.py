from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    install_requires=[
        "aiohttp==3.7.3",
        "aioresponses==0.7.1",
        "async-timeout==3.0.1; python_full_version >= '3.5.3'",
        "attrs==20.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "certifi==2020.12.5",
        "chardet==3.0.4",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "mock==4.0.3",
        "mock.gpio==0.1.7",
        "multidict==5.1.0; python_version >= '3.6'",
        "pyyaml==5.3.1",
        "requests==2.25.1",
        "typing-extensions==3.7.4.3",
        "urllib3==1.26.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "yarl==1.6.3; python_version >= '3.6'",
    ],
    name="monitor",
    version="0.1.0",
    description="Build monitor GPIO",
    long_description=readme,
    author="Matthew Z Worthington",
    author_email="worthingtown@gmail.com",
    url="https://github.com/worthington10TW/raspberry-pi-playground",
    include_package_data=True,
    license=license,
    packages=find_packages(include=("monitor", "monitor.*")),
    entry_points={"console_scripts": ["monitor=monitor.app:main"],},
    package_data={"": ["monitor/integrations.json"]},
)
