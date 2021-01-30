from setuptools import find_packages, setup


def read_requirements():
    """
    Looping through requirements.txt
    installing requirements
    """
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split("\n")

    return requirements


setup(
    name="coupons",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    entry_points="""
        [console_scripts]
    """,
)
