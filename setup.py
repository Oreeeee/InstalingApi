from setuptools import setup

setup(
    name="instalingapi",
    version="1.2.7",
    description="Instaling API written in Python.",
    license="Unlicense",
    author="Oreeeee",
    packages=["instalingapi"],
    install_requires=["requests", "beautifulsoup4", "lxml", "latest-user-agents"]
)