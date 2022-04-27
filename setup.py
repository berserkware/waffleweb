from distutils.core import setup

setup(
  name = 'waffleweb',
  packages = ['waffleweb'],
  version = '0.1.0',
  license='MIT',
  description = 'A python library for making scalable websites easy',
  author = 'Caleb Mckay',
  author_email = 'bersekware@gmail.com',
  install_requires=['pytz'],
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
