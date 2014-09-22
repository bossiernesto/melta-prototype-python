melta
=====
[![Build Status](https://travis-ci.org/bossiernesto/melta.svg)](https://travis-ci.org/bossiernesto/melta)
[![Latest Version](http://img.shields.io/github/tag/bossiernesto/melta.svg)](https://github.com/bossiernesto/melta/releases)
[![Stories in Ready](https://badge.waffle.io/bossiernesto/melta.svg?label=ready&title=Ready)](http://waffle.io/bossiernesto/melta)

A small object database engine.

Melta is a small size OODBMS, with some small features like transactional and versioned objects, master/slave replication and a small query language. The objective of the project is to have a minimalist databse with the existing python backend.

To just download the current develop build, just do:

```
$ git clone git@github.com:bossiernesto/melta.git
```

## Features

    These are the features that are currently avaiable and tested for now.

  - Schema support to hold objects. In this way you can have multiple schemas that will persist one in different files or in the same one.
  - Transaction support for schemas and objects.
  - Simple model with atomic, aggregation and reference as primitive objects.
  - Converts from python object to a melta object type.
      - Supported python objects:
        - List
        - Dictionary
        - python instance
        - Int
        -Float
        - Str
        - Tuple
        - More types coming soon (other iterable and primitive types)

## Source of the idea

   This small database prototype is heavily based on the paper of [OMG Object Database Technology Working Group White Paper](http://www.odbms.org/wp-content/uploads/2007/09/033.01-Card-Next-Generation-Object-Database-Standardization-September-2007.pdf)

## Query Language
Still on the works will be avaiable soon.

## Authors and Contributors
Currently the project is being developed and mantained by Ernesto Bossi (@bossiernesto)

## Support or Contact
Having issues or problems with Melta database? Check out the FAQ at  or contact @bossiernesto to bossi.ernestog@gmail.com and we’ll help you sort it out.
