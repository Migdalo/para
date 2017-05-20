from setuptools import setup
import unittest

def para_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setup(name='para',
      version='2.0.1',
      author='Migdalo',
      license='MIT',
      packages=['para'],
      test_suite='setup.para_test_suite',
      entry_points={
        'console_scripts': [
            'para = para.para:process_arguments'
        ]
      },
      zip_safe=True)

