from setuptools import setup, find_packages

setup(name="Melta",
      version="0.0.1",
      description="Simple Object Memory Database",
      author="Ernesto Bossi",
      author_email="bossi.ernestog@gmail.com",
      url="http://bossiernesto.github.io/melta/",
      license="BSD",
      py_modules=find_packages(exclude=('test')),
      keywords="Memory Database",
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Environment :: Console",
                   "Topic :: Database",
                   "License :: OSI Approved :: BSD License"],
      requires=["pyopenssl", "six"]
)
