import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sous",
    version="0.0.1",
    author="Hunter Thompson",
    author_email="thompson.grey.hunter@gmail.com",
    description="Sous programming language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sudo-Sous/Sous",
    packages=setuptools.find_packages(),
    scripts=['bin/sous'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
