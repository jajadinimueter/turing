from setuptools import setup, find_packages

packages = find_packages()

setup(
    name='turing',
    version='0.1',
    description='A Turing Machine',
    author='Florian Mueller',
    author_email='jajadinimueter@gmail.com',
    test_requires=[
        'pytest'
    ],
    install_requires=[
        'blessings',
        'pytest'
    ],
    packages=packages,
    entry_points="""\
    [console_scripts]
    turing = turing.runner:main
    """,
    package_data={
        '': ['*.txt', '*.csv', '*.tex', '*.cfg', '*.jpg']
    }
)
