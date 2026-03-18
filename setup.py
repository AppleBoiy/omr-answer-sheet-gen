"""
Setup script for OMR Generator package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="omr-generator-thai",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Thai OMR Answer Sheet Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/omr-generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "reportlab>=3.6.0",
        "qrcode>=7.3.0",
        "pillow>=9.0.0",
    ],
    include_package_data=True,
    package_data={
        "": ["fonts/THSarabunNew/*.ttf"],
    },
)
