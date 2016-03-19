import codecs
import os
import re
import setuptools
import setuptools.command.test as command_test
import sys


def _get_readme():
    readme_path = '%s/%s' % (
        os.path.dirname(os.path.abspath(__file__)), 'README.md'
    )

    with codecs.open(readme_path, 'r', encoding='utf8') as f:
        return f.read()


class PyTest(command_test.test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        command_test.test.initialize_options(self)
        self.pytest_args = '-v'

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class Flake(command_test.test):
    user_options = []

    def initialize_options(self):
        command_test.test.initialize_options(self)
        from flake8.engine import get_parser

        self.option_to_cmds = {}
        parser = get_parser()[0]
        for opt in parser.option_list:
            cmd_name = opt._long_opts[0][2:]
            option_name = cmd_name.replace('-', '_')
            self.option_to_cmds[option_name] = cmd_name
            setattr(self, option_name, None)

    def finalize_options(self):
        from flake8.util import option_normalizer
        self.options_dict = {}
        for (option_name, opt) in self.option_to_cmds.items():
            if option_name in ['help', 'verbose']:
                continue
            value = getattr(self, option_name)
            if value is None:
                continue
            value = option_normalizer(value, opt, option_name)
            # Check if there's any values that need to be fixed.
            if option_name == "include" and isinstance(value, str):
                value = re.findall('[^,;\s]+', value)

            self.options_dict[option_name] = value

    def distribution_files(self):
        distribution_packages = setuptools.find_packages()
        if distribution_packages:
            package_dirs = self.distribution.package_dir or {}
            for package in distribution_packages:
                pkg_dir = package
                if package in package_dirs:
                    pkg_dir = package_dirs[package]
                elif '' in package_dirs:
                    pkg_dir = package_dirs[''] + os.path.sep + pkg_dir
                yield pkg_dir.replace('.', os.path.sep)

        if self.distribution.py_modules:
            for filename in self.distribution.py_modules:
                yield "%s.py" % filename
        # Don't miss the setup.py file itself
        yield "setup.py"

    def run_tests(self):
        from flake8.engine import get_style_guide
        from flake8.main import DEFAULT_CONFIG, print_report
        # Prepare
        paths = list(self.distribution_files())
        flake8_style = get_style_guide(config_file=DEFAULT_CONFIG, paths=paths,
                                       **self.options_dict)

        # Run the checkers
        report = flake8_style.check_files()
        exit_code = print_report(report, flake8_style)
        sys.exit(exit_code)


setuptools.setup(
    name='lasagna',
    version='0.1a1',
    packages=setuptools.find_packages(exclude=['test', 'test.*']),
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
    tests_require=[
        'ipdb',
        'pytest-cov',
        'pytest',
        'flake8',
    ],
    cmdclass={'test': PyTest, 'coverage': Flake},
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
