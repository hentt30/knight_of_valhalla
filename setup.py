"""
Configuration setup for python project
"""
import setuptools


setuptools.setup(
    name="advancing_hero",
    version="1.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    description=
    "A game for a college project",
    license="MIT",
    install_requires=[
        "pygame"
    ],
)
