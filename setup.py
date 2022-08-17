import os

from setuptools import setup, find_packages

version = (os.getenv("VERSION") or "0.0.0").lstrip("v")

this_script_dir = os.path.split(os.path.abspath(__file__))[0]
with open(f"{this_script_dir}/requirements.txt", "r") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="hasura-postgres-schema-sync",
    version=version,
    url="https://github.com/ftpsolutions/hasura-postgres-schema-sync",
    author="Edward Beech",
    author_email="edward.beech@ftpsolutions.com.au",
    description="A service to keep a Hasura instance in sync with a Postgres database",
    packages=find_packages(),
    install_requires=install_requires,
)
