from setuptools import setup

setup(
    install_requires=[
        "pendulum>=2.0.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": ["pre-commit", "flake8", "flake8-docstrings", "black", "isort", "pytype"],
    },
)
