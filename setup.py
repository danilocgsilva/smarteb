from setuptools import setup

VERSION = "1.0.1"

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="smart_eb",
    version=VERSION,
    description="Makes web stack based on AWS Elasticbeanstalk really easy",
    long_description_content_type="text/markdown",
    long_description=readme(),
    keywords="easy AWS Elasticbeanstalk command-line-utility",
    url="https://github.com/danilocgsilva/smarteb",
    author="Danilo Silva",
    author_email="contact@danilocgsilva.me",
    packages=["smart_eb"],
    entry_points={"console_scripts": ["smeb=smart_eb.__main__:main"],},
    include_package_data=True
)

