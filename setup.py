#!/usr/bin/env python3
"""
Setup script untuk Location Tracker
"""

from setuptools import setup, find_packages
import os

# Read long description from README
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="location-tracker",
    version="1.0.0",
    author="Location Tracker Team",
    author_email="info@locationtracker.com",
    description="Sistem Deep Learning untuk melacak lokasi menggunakan gambar dan face recognition",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/location-tracker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "gpu": [
            "tensorflow-gpu>=2.14.0",
            "torch-gpu>=2.1.0",
        ],
        "web": [
            "flask>=3.0.0",
            "werkzeug>=3.0.1",
        ]
    },
    entry_points={
        "console_scripts": [
            "location-tracker=main:main",
            "location-tracker-web=web_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.pkl", "*.html", "*.md"],
    },
    zip_safe=False,
    keywords=[
        "computer-vision",
        "deep-learning",
        "face-recognition", 
        "location-tracking",
        "gps",
        "image-recognition",
        "tensorflow",
        "opencv",
        "geolocation"
    ],
    project_urls={
        "Bug Reports": "https://github.com/your-username/location-tracker/issues",
        "Source": "https://github.com/your-username/location-tracker",
        "Documentation": "https://location-tracker.readthedocs.io/",
    },
)