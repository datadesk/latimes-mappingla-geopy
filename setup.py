from setuptools import setup, find_packages

setup(name='latimes-mappingla-geopy',
      version='0.93-latimes',
      description='Python Geocoding Toolbox',
      author='Ben Welsh from original work by Brian Beck',
      author_email='Benjamin.Welsh@latimes.com',
      url='http://github.com/datadesk/latimes-mappingla-geopy',
      download_url='http://github.com/datadesk/latimes-mappingla-geopy.git',
      packages=find_packages(),
      license='MIT',
      keywords='geocode geocoding gis geographical maps earth distance',
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Scientific/Engineering :: GIS",
                   "Topic :: Software Development :: Libraries :: Python Modules"
                   ],
     )
