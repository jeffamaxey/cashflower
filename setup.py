from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    author="Zuzanna Chmielewska",
    description="Framework for actuarial cash flow models",
    include_package_data=True,
    install_requires=[
        'pandas',
        'networkx',
        'numpy'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="cashflower",
    packages=find_packages(include=["cashflower", "cashflower.*"]),
    project_urls={
        'Source': 'https://github.com/acturtle/cashflower',
        'Tracker': 'https://github.com/acturtle/cashflower/issues',
        'Documentation': 'https://cashflower.acturtle.com',
        'Cheat sheet': 'https://www.acturtle.com/static/pdf/cheat_sheet.pdf',
    },
    python_requires='>=3.9',
    url="https://github.com/acturtle/cashflower",
    version="0.4.10",
)
