import setuptools
import os
import re

def get_version():
    """Reads version from adesk/__init__.py"""
    init_path = os.path.join(os.path.dirname(__file__), 'adesk', '__init__.py')
    with open(init_path, 'r') as f:
        version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def get_long_description():
    """Reads README.md for long description"""
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
    return long_description

setuptools.setup(
    name='adesk-python-sdk',
    version=get_version(),
    author='AI Agent (for Adesk Task)', # Placeholder
    author_email='ai.agent@example.com', # Placeholder
    description='A Python SDK for interacting with the Adesk API (api.adesk.ru).',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/placeholder/adesk-python-sdk', # Placeholder
    packages=setuptools.find_packages(where='.', exclude=('tests*', 'tests')), # Exclude tests directory
    install_requires=[
        'requests', # From requirements.txt
    ],
    classifiers=[
        'Development Status :: 3 - Alpha', # Initial version
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License', # Assuming MIT
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    project_urls={ # Optional
        'Bug Reports': 'https://github.com/placeholder/adesk-python-sdk/issues',
        'Source': 'https://github.com/placeholder/adesk-python-sdk',
    },
    # Ensure the 'adesk' package directory is correctly identified if setup.py is not in the root of 'adesk-python-sdk'
    # If setup.py is in 'adesk-python-sdk/', and your package is 'adesk-python-sdk/adesk/',
    # find_packages() should work. If setup.py is inside a 'src' layout, 'package_dir' might be needed.
    # Current structure (setup.py in adesk-python-sdk root) is fine with default find_packages().
)
