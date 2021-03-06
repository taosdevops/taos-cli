from setuptools import find_packages, setup

setup(
    author="TAOS DevopsNow",
    name="taos",
    author_email="devopsnow@taos.com",
    description="Taos Command Line",
    # license=open("LICENSE").read(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    version="1.1.0",
    url="https://github.com/taosdevops/taos",
    install_requires=[
        "beautifulsoup4~=4.8",
        "Click~=7.0",
        "sendgrid~=6.1",
        "slackclient~=2.2",
        "taosdevopsutils~=1.3",
    ],
    entry_points="""
        [console_scripts]
        taos=taos.cli:main
        """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Your supported Python ranges
)
