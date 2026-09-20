# Saved-event endpoint

Workers-style handler with an injected storage binding. A 201 response promises that the event is stored; a failed write must not produce a successful response. The storage client is reusable. Run `node --test`.

This local fixture has no cloud credentials or deployment. It models the handler/storage promise boundary, not provider scheduling or quotas.
