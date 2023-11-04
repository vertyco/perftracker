from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="perftracker",
    version="1.2.0",
    url="https://github.com/vertyco/perftracker",
    author="vertyco",
    author_email="alex.c.goble@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="PerfTracker is a lightweight function performance monitoring framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Pydantic :: 1",
        "Framework :: Pydantic :: 2",
        "Framework :: Pytest",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Typing :: Typed",
        "Natural Language :: English",
    ],
    python_requires=">=3.10",
)
