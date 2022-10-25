from setuptools import setup

setup(
    name="instalingapi",
    version="1.2.5-dev7",
    description="Instaling API written in Python.",
    license="Unlicense",
    author="Oreeeee",
    packages=["instalingapi"],
    install_requires=["requests", "beautifulsoup4", "lxml"]
)