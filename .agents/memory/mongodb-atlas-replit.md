---
name: MongoDB Atlas on Replit
description: How to connect MongoDB Atlas from Replit without SSL errors
---

Connecting Motor/pymongo to MongoDB Atlas from Replit (NixOS) fails with `TLSV1_ALERT_INTERNAL_ERROR` unless two things are done:

1. Pass `tlsCAFile=certifi.where()` to `AsyncIOMotorClient` (install `certifi` via pip).
2. Add `0.0.0.0/0` to MongoDB Atlas → Network Access. Replit runs on dynamic IPs; whitelisting only a single IP blocks it. The SSL error is Atlas's way of rejecting unknown IPs — it is NOT a TLS version problem.

**Why:** NixOS doesn't ship system CA certs that pymongo finds automatically; certifi provides them. Atlas enforces network ACLs before the TLS handshake completes, so an unlisted IP gets an internal TLS alert.

**How to apply:** Any project using Motor/pymongo against Atlas on Replit needs both fixes. Check `backend/app/db/mongodb.py`.
