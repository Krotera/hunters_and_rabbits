import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="hunters_and_rabbits",
    version="1.0.0",
    author="Krotera",
    author_email="01101011@tuta.io",
    description="A Dash implementation of the Hunters and Rabbits graph game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        "networkx>=2.4",
        "flask>=1.1.1",
        "plotly>=4.4.1",
        "dash>=1.7.0",
        "dash-core-components>=1.6.0",
        "dash-html-components>=1.0.2",
        "numpy>=1.18.0",
    ],
    classifiers=[ # https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
