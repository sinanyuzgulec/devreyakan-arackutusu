from setuptools import setup, find_packages

setup(
    name="devreyakan-arackutusu",
    version="0.0.4",
    author="Sinan Yüzgüleç",
    description="Elektronik mühendisleri ve gömülü sistem geliştiricileri için araç kutusu",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sinanyuzgulec/devreyakan-arackutusu",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt6>=6.4.0",
        "numpy>=1.20.0",
        "pyserial>=3.5"
    ],
    entry_points={
        "console_scripts": [
            "devreyakan-arackutusu=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
