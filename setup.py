from setuptools import setup

setup(
    name="talonlib",
    version="1.3.beta",
    author="Morozoff_",
    description="УНППТ™ - Уникальная Необратимая Публичная Подпись Талона",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    py_modules=["talonlib"],
    install_requires=["psutil"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
)
