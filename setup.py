from setuptools import setup

setup(
    install_requires=[
        "pendulum>=2.0.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        # @ToDo(jorrick) change this to be all pre-commit based.
        "dev": ["pre-commit", "flake8", "flake8-docstrings", "black", "isort", "pytype", "pytest"],
    },
)
