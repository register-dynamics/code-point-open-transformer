from setuptools import setup

setup(
    name="code_point_open_transformer",
    version="2.0",
    packages=["code_point_open_transformer"],
    install_requires=[
        "click==7.0",
        "openpyxl==3.0.0",
        "tqdm==4.36.1",
        "xlrd==1.2.0",
    ],
    entry_points="""
      [console_scripts]
      codepointopen=code_point_open_transformer.cli:main
    """,
)
