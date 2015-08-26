Comments
========

If you need to embed more than a few lines of immediate data in your program,
you may want some comments to explain what's going on.  By default,
``textdata`` strip out Python-like comments (from ``#`` to
end of line). So::

    exclude = words("""
        __pycache__ *.pyc *.pyo     # compilation artifacts
        .hg* .git*                  # repository artifacts
        .coverage                   # code tool artifacts
        .DS_Store                   # platform artifacts
    """)

Yields::

    ['__pycache__', '*.pyc', '*.pyo', '.hg*', '.git*',
     '.coverage', '.DS_Store']

You could of course write it out as::

    exclude = [
        '__pycache__', '*.pyc', '*.pyo',   # compilation artifacts
        '.hg*', '.git*',                   # repository artifacts
        '.coverage',                       # code tool artifacts
        '.DS_Store'                        # platform artifacts
    ]

But you'd need more nitsy punctuation, and it's less compact.

If however you want to capture
comments, set ``cstrip=False`` (though that is probably more useful with the
``lines`` and ``textlines`` APIs than for ``words``).

