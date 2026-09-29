# <Team> TDD, version 1.0

Change log (newest first): date, section, one line.

## 1. Engine and versions
Owner:
Engine and exact version. Plugins. Export targets. Rule for upgrading.

## 2. Topology and hosting
Owner:
Dedicated, listen server or relay, and why (CS202 week 3). Where the server runs for lab tests and home tests.

## 3. Authority
Owner:
What the server owns. What a client may predict. What a client may never send.

## 4. Rates and budgets
Owner:
Server tick rate. Snapshot send rate. Bytes per entity. Entities per snapshot. Per-client download and server upload, with the working.

## 5. Replication list
Owner:
| Object | Properties | Authority | How sent (synchronizer, RPC, snapshot) | Rate |
|---|---|---|---|---|

## 6. Message list
Owner:
| Client request | Parameters | Range | Rate | State | Ownership | Reach |
|---|---|---|---|---|---|---|

## 7. Repository and builds
Owner:
Branch rules, LFS patterns, build command, version format, where builds are stored.

## 8. Asset pipeline
Owners (art, audio):
Source formats, export settings, units and scale, naming, import presets, who checks an asset into the build.

## 9. Test plan
Owner:
Network profiles (delay, jitter, loss) each build is tested under, and what it must pass.

## 10. Risk register
Owner:
Link to risks.csv and the check_risks.py output. Sprint 1 spike list. Deferred spikes with dates. Accepted risks with watcher and fallback.

## 11. Persistence (version 1: save format and file save)
Owner:
The character record the server saves: fields, types and a format version number (CS201 week 12). One example file. When the server writes it (at least level-up and logout). The save routine: write a temporary file, flush it, rename it over the old one (CS201 week 12, section 4; DB201 week 1, section 3.1). The result of a crash test: kill the server during a save and show the file still loads. The client never sends a value that goes into the save. Version 2 (database schema, transactions, grant ids) is due at alpha, after DB201 weeks 2, 5 and 6.

## 12. Tracking plan (version 1)
Owner:
| Event | Sent by (server or client) | Question it answers at the alpha playtest |
|---|---|---|
At least six server-side events. Version 2 adds properties, storage and a threshold per question after DB201 week 10, and alpha criterion A6 checks that each one fires in an end-to-end run.
