textdata
========

``textdata`` makes it easy to have clean, nicely-whitespaced data specified in
your program (or a separate text file).

It helps manage both formatting and data type conversions, keeping extra code,
gratuitious whitespaces, and data-specification syntax out of your way.

It's permissive of the human-oriented layouts needed to make code and data
blocks look good, without reflecting those requirements in the resulting data.

Python string methods give easy ways to clean text up, but it's no joy
reinventing that particular wheel every time you need it--especially since many
of the details are nitsy, low-level, and a little tricky. ``textdata`` is a "do
what I mean!" module that replaces *a la carte* text cleanups with simple,
well-tested code that doesn't lengthen your program or require constant
wheel-reinvention.

.. toctree::
   :titlesonly:

   Lines and Text <lines_text>
   Words <words>
   Paragraphs <paragraphs>
   Attributes (Dicts) <attrs>
   Tables <tables>
   Comments <comments>
   Unicode and Encodings <unicode>
   Alternate Data Paths <alternate>
   API Details <api>
   Notes <notes>
   Installation <installation>
   Change Log <CHANGES>
