from setuptools import setup


with open("requirements.txt", "r") as req:
    install_required = req.read()


tests_required = (
    "pytest",
    "pytest-black",
    "pytest-cov",
    "pytest-tornado",
    "pytest-flake8",
)


setup(
    name="microsentry",
    version="0.0.0",
    setup_requires=["pytest-runner"],
    install_required=install_required,
    tests_require=tests_required,
)
