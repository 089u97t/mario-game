#!/usr/bin/env python
"""
Wrapper to run pygbag with relative proxy URLs so the compiled pygame game
works behind the Base44 preview reverse proxy.

pygbag's test server rewrites CDN URLs in index.html to http://<bind>:<port>/,
which the browser cannot reach when served through a reverse proxy. This
wrapper patches the proxy to an empty string so URLs become relative paths
served from the same origin.
"""
import pygbag.testserver as ts

_orig_run = ts.run_code_server


def _patched_run(args, cc):
    cc = dict(cc)
    cc["proxy"] = ""  # relative URLs instead of http://0.0.0.0:8000/
    return _orig_run(args, cc)


ts.run_code_server = _patched_run

from pygbag.__main__ import import_site
import asyncio

asyncio.run(import_site())
