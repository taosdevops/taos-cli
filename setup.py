from setuptools import find_packages, setup

setup(
    author="TAOS DevopsNow",
    name="taos",
    email="devopsnow@taos.com",
    description="Taos Command Line",
    #license=open("LICENSE").read(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    version="1.0.0",
    url="https://github.com/taosdevops/taos",
    install_requires=[
        "Click==7.0",
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
    python_requires='>=3.6',  # Your supported Python ranges
)
