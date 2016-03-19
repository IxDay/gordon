import codecs
import os
import setuptools


def _get_readme():
    readme_path = '%s/%s' % (
        os.path.dirname(os.path.abspath(__file__)), 'README.md'
    )

    with codecs.open(readme_path, 'r', encoding='utf8') as f:
        return f.read()


setuptools.setup(
    name='lasagna',
    version='0.1a1',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    author='John Doe',
    author_email='john@doe.com',
    description='Server for Gordon',
    long_description=_get_readme(),
    install_requires=[
        'flask',
        'peewee>=2.6.2',
        'psycopg2',
        'marshmallow>=2.0.0'
    ],
    extras_require={
        'tests': [
            'pytest-cov',
            'pytest',
            'flake8',
        ],
        'dev': [
            'ipdb',
            'click'
        ]
    },
    entry_points='''
        [console_scripts]
        lasagna=lasagna.cli:main
    ''',
    url='https://github.com/IxDay/gordon',
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
    ]
)
