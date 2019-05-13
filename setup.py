import setuptools


def get_long_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


setuptools.setup(
    # Common data
    name="md_translate",
    version='0.1.2',
    author="Ilya Chichak",
    author_email="ilyachch@gmail.com",
    description="CLI tool to translate markdown files",
    # Meta
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://github.com/ilyachch/md_docs-trans-app",
    # Technical data
    python_requires=">=3.6",
    packages=setuptools.find_packages(exclude=['tests*', ]),
    install_requires=[
        "requests",
    ],
    extras_require={
        'dev': [
            'twine',
            'wheel',
            'setuptools',
            'bumpversion',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Documentation",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    entry_points={
        'console_scripts': ['md-translate=md_translate.app:main'],
    },
    test_suite="tests",
)
