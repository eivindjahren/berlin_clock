from pathlib import Path

from setuptools import find_packages, setup


def get_long_description() -> str:
    return Path("README.md").read_text(encoding="utf8")


setup(
    name="Berlin Clock",
    author="Eivind Jahren",
    author_email="eivind.jahren@webstep.no",
    description="Displays a berlin clock in the terminal.",
    use_scm_version=True,
    url="https://github.com/eivindjahren/berlin_clock",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "berlin_clock=berlin_clock.__main__:main",
        ],
    },
    platforms="any",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    setup_requires=["setuptools_scm"],
    include_package_data=True,
)
