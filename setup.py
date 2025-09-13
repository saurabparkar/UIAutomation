from setuptools import setup, find_packages

setup(
    name="UIFramework",
    version="0.1.0",
    description="A Unified UI Automation Framework with Selenium and Playwright support",
    author="Saurab Parkar",
    packages=find_packages(include=["UIFramework", "UIFramework.*"]),
    install_requires=[
        "pytest",
        "selenium",
        "playwright",
    ],
    include_package_data=True,  # <-- important for MANIFEST.in
    python_requires=">=3.8",
)
