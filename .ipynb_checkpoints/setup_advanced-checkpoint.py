from setuptools import setup, find_packages

# Package metadata
NAME = "fraud-detection"
VERSION = "0.1.0"
DESCRIPTION = "Machine Learning API for fraud detection systems"
AUTHOR = "Moe Yahya"
EMAIL = "moee.yahya@gmail.com"
URL = "https://github.com/moeyahya/fraud-detection-ml-api-aws-cicd"

# Core dependencies from your requirements.txt
INSTALL_REQUIRES = [
    'pandas>=1.5.0',
    'scikit-learn>=1.2.0',
    'Flask>=2.0.0',
    'joblib>=1.0.0',
    'imbalanced-learn>=0.10.0',
    'scipy>=1.7.0',
    'numpy>=1.21.0',
    'waitress>=2.1.0'  # Production WSGI server
]

# Development/test dependencies (not in requirements.txt)
DEV_REQUIRES = [
    'pytest>=7.0',
    'pytest-cov>=3.0',
    'pylint>=2.15',
    'black>=23.0',
    'mypy>=1.0',
    'bandit>=1.7',  # Security scanning
    'faker>=15.0'   # Test data generation
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(include=['src', 'src.*']),
    python_requires='>=3.8',
    install_requires=INSTALL_REQUIRES,
    extras_require={
        'dev': DEV_REQUIRES,
        'test': [  # Separate test dependencies
            'pytest>=7.0',
            'pytest-cov>=3.0',
            'faker>=15.0'
        ]
    },
    include_package_data=True,
    package_dir={'': '.'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Operating System :: OS Independent',
    ],
    keywords='machine-learning fraud-detection ml-api',
    project_urls={
        'Bug Reports': f'{URL}/issues',
        'Source': URL,
    },
)