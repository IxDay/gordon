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
    name='rulzurapi',
    version='0.1a1',
    packages = setuptools.find_packages('src'),  # include all packages under src
    package_dir = {'':'src'},   # tell distutils packages are under src
    author='RulzUrLife team.',
    author_email='something@something.else',
    description='Server for the RulzUrKitchen product',
    long_description=_get_readme(),
    install_requires=_get_requirements(),
    url='https://github.com/RulzUrLife/RulzUrArch',
    license='Apache v2.0',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
    ],
)
