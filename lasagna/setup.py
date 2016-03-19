import codecs
import os
import setuptools

def _get_requirements():
    requirements_path = '%s/%s' % (
        os.path.dirname(os.path.abspath(__file__)), 'requirements.txt'
    )
    with open(requirements_path, 'r') as f:
        requirements = f.read()
        return requirements.split('\n')


def _get_readme():
    readme_path = '%s/%s' % (
        os.path.dirname(os.path.abspath(__file__)), 'README.md'
    )

    with codecs.open(readme_path, 'r', encoding='utf8') as f:
        return f.read()


setuptools.setup(
    name='lasagna',
    version='0.1a1',
    packages = setuptools.find_packages(exclude=['tests', 'tests.*']),
    author='John Doe',
    author_email='john@doe.com',
    description='Server for Gordon',
    long_description=_get_readme(),
    install_requires=_get_requirements(),
    url='https://github.com/IxDay/gordon',
    license='MIT',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
    ],
)
