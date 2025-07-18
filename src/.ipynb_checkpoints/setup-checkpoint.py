from setuptools import setup, find_packages

setup(
    name="fraud-detection",
    version="0.1",
    packages=find_packages(include=['src*']), 
    install_requires=[
        'pandas>=1.5.0',
        'scikit-learn>=1.2.0',
        'Flask>=2.0.0',
        'joblib>=1.0.0',
        'imbalanced-learn>=0.10.0',
        'scipy>=1.7.0',
        'numpy>=1.21.0',
        'waitress>=2.1.0'
    ],
)