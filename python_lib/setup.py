import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="excalibur",
    version="0.0.1",
    author="Ceacar",
    author_email="alex.yonder@yahoo.com",
    description="A python utility package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ceacar/utility",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
