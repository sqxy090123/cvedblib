from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cvedblib",
    version="0.0.1b1",
    author="sqxy090123",
    author_email="sqx20150423@gmail.com",
    description="A library for querying and exploiting CVEs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sqxy090123/cvedblib",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "cvedblib": ["o.json", "extra/*.dll", "extra/*.c"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=open("requirements.txt").read().splitlines()
)