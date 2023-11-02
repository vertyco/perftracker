from setuptools import find_packages, setup

setup(
    name="perftracker",
    version="0.1.0",
    url="https://github.com/vertyco/perftracker",
    author="Your Name",
    author_email="alex.c.goble@gmail.com",
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
