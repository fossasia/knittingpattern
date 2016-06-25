.. _FileFormatSpecification:

Knitting Pattern File Format Specification
==========================================

For the words see `the glossary
<https://github.com/AllYarnsAreBeautiful/ayab-desktop/wiki/Glossary>`__.

Design Decisions
----------------

Concerns:

- We can never implement everything that is possible with knitting. We must therefore allow instructions to be arbitrary.
- We can not use a grid as a basis. This does not reflect if you split the work and make i.e. two big legs
- Knitting can be done on the right and on the wrong side. The same result can be achived when knitting in both directions. 

Assumptions
-----------

- we start from bottom right
- default instruction (`see
  <https://github.com/AllYarnsAreBeautiful/ayab-desktop/wiki/2016-05-25---Knitting-pattern>`_)
  
  .. code:: json
    
    {
      "type" : "knit", 
    }
    {
      "type" : "ktog tbl", # identifier
      "count" : 2
    }
    
- default connection

  .. code:: json
   
      {
        "start" : 0,
      }
        
- ``"id"`` can point to an object.

