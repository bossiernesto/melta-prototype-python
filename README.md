melta
=====

Project Status Build: 

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
        - Str
        - More types coming soon (other iterable and primitive types)


## Query Language
Still on the works will be avaiable soon.

## Authors and Contributors
Currently the project is being developed and mantained by Ernesto Bossi (@bossiernesto)

## Support or Contact
Having issues or problems with Melta database? Check out the FAQ at  or contact @bossiernesto to bossi.ernestog@gmail.com and we’ll help you sort it out.
