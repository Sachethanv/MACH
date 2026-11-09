"""Write these tests BEFORE implementing mach.guard (hard release gates).

Planned cases:
- effective set excludes superseded, draft, obsolete and withdrawn revisions
- effective window: t_from <= t < t_to, evaluated in plant local time zone (R7)
- scope: site/line/station/model/serial range, inclusive bounds as written in source (V2)
- role filter applied before retrieval; no restricted element IDs in any trace (A1-A3)
- deviation overlay replaces named steps until expiry, then is ignored (R6)
- withdrawn revision -> previous one reinstated (R5)
- coherence check rejects an answer citing two revisions of one document (R1)
"""
