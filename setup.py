'''Install the braillegraph package.'''

from setuptools import setup

setup(name='braillegraph',
      version='0.6',
      description='A library for creating graphs using Unicode braille characters',
      url='http://github.com/chrisbouchard/braillegraph',
      author='Chris Bouchard',
      author_email='chris@upliftinglemma.net',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Utilities'
      ],
      packages=['braillegraph'],
      zip_safe=False)

