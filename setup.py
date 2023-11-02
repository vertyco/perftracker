from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="perftracker",
    version="1.0.3",
    url="https://github.com/vertyco/perftracker",
    author="Alex Goble",
    author_email="alex.c.goble@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A Python performance tracking package",
    packages=find_packages(),
    install_requires=["pydantic"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
