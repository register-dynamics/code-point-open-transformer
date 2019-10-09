from setuptools import setup

setup(
    name="code_point_open_transformer",
    version="2.0",
    packages=["code_point_open_transformer"],
    install_requires=[
        "click",
        "openpyxl",
        "tqdm",
        "xlrd",
    ],
    entry_points="""
      [console_scripts]
      codepointopen=code_point_open_transformer.cli:main
    """,
)
