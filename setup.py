from setuptools import setup

with open('README.md', 'r') as f:
  long_description = f.read()

setup(
  name = 'waffleweb',
  packages = ['waffleweb'],
  version = '0.1a2',
  license='MIT',
  description = 'A python library for making scalable websites easy',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Caleb Mckay',
  author_email = 'bersekware@gmail.com',
  keywords=['framework', 'web', 'wsgi', 'waffleweb', 'web-framework'],
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
  ],
)
