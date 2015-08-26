textdata
========

One often needs to state data in program source. Python, however, needs its
lines indented *just so*. Multi-line strings therefore often have extra
spaces and newline characters you didn't really want. Many developers "fix"
this by using Python ``list`` literals, but that has its own problems: it's
tedious, more verbose, and often less legible.

The ``textdata`` package makes it easy to have clean, nicely-whitespaced
data specified in your program, but to get the data without extra whitespace
cluttering things up. It's permissive of the layouts needed to make Python
code look and work right, without reflecting those requirements in the
resulting data.

Python string methods give easy ways to clean text up, but it's no joy
reinventing that particular wheel every time you need it--especially since
many of the details are nitsy, low-level, and a little tricky. ``textdata``
is a "just give me the text!" module that replaces *a la carte* text
cleanups with simple, well-tested code that doesn't lengthen your program or
require constant wheel-reinvention.

.. toctree::
   :titlesonly:

   example
   apioptions
   Words <words>
   Comments <comments>
   Paragraphs <paragraphs>
   Unicode and Encodings <unicode>
   Alternate Data Paths <alternate>
   API Details <api>
   Notes <notes>
   Installation <installation>
   CHANGES
