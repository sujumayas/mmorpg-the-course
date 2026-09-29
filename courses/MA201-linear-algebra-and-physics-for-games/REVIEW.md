# MA201 review: open items

Review pass of 29 September 2026. Everything else found in the pass was fixed in place.

## Facts not re-verified this pass

| File | Claim | Status | Proposed action |
|---|---|---|---|
| lectures/w01, w02, w03 | Unreal Engine 5.3.2 values (`WalkableFloorZ` 0.71, `FTransform` composition order and comments) and UE3 `Pawn.uc` `WalkableFloorZ=0.7` | Read by the author from third-party public source mirrors because Epic's repository needs an account. Sources now say so explicitly. | Confirm against Epic's own GitHub repository with a linked Epic account, then drop the mirror wording. |
| lectures/w14 | UE5 Large World Coordinates: default `WORLD_MAX` 88 million km, UE4 `WORLD_MAX` 21 km, feature still described as beta (UE 5.8 docs) | Epic documentation not fetched in this pass | Re-check on dev.epicgames.com before the course runs. |
| lectures/w04 | Valve Developer Community "Field of View" page (archived copy of 6 June 2026): HL2 default 75, about 91° on 16:9 | Taken from the author's archive copy; not re-fetched | Re-fetch the archive copy; the lecture already explains the page's vertical/horizontal wording conflict. |
| lectures/w06 | World of Warcraft transports | Cited as TrinityCore 3.3.5a (emulator), not Blizzard code. Acceptable as stated. | None needed unless a primary source appears. |
| lectures/w10, w12, w14 | Unity 6.6 documentation values (`Physics.bounceThreshold` default 2, combine-mode priority, `Physics.Raycast` ignoring colliders that contain the origin, `Time.timeAsDouble`) | Not re-fetched in this pass | Spot-check on docs.unity3d.com. |

## Outside this reviewer's remit

- `syllabus.md` still carries the generated-stub marker. The orchestrator owns the syllabus and `build_plan.py`.

## Fact sweep (29 September 2026)

Verified 4, hedged 2, removed 0.

- Verified. Large World Coordinates (w14): default `WORLD_MAX` 88 million km, the UE4 value of 21 km, and the "Beta feature, use caution when shipping" note, on Epic's page in the Unreal Engine 5.7 documentation (Internet Archive copy of 2 March 2026). The lecture said 5.8 and now says 5.7.
- Verified. Valve Developer Community "Field of View" (w04): default 75, about 91° on 16:9, and the scaled-FOV formula, re-read in the Internet Archive copy of 6 June 2026.
- Verified. Unity 6.6 documentation (w10, w12, w14), fetched 29 September 2026: `Physics.bounceThreshold` default 2, Bounciness default 0, Bounce Combine default Average, the priority order Maximum, Multiply, Minimum, Average, `Physics.Raycast` ignoring colliders that contain the origin, and `Time.timeAsDouble` recommended for precision.
- Verified. `FTransform` storage (scale, quaternion, translation), the scale, rotate, translate order and "`A * B` applies `A` first" (w02, w03) are in Epic's own API reference (Unreal Engine 4.27 documentation, Internet Archive copy of 19 July 2024). w02 now cites that page instead of relying on the mirror.
- Hedged. UE5 `WalkableFloorZ` 0.71 and UE3 `Pawn.uc` `WalkableFloorZ=0.7` (w01). No Epic page with the default could be fetched. The body text now says both were read from third-party copies of the source.
- Hedged. `FTransform::Multiply` details and `CalcNewComponentToWorld_GeneralCase` (w03). Still mirror-only. The week 3 heading now says "5.3 source, read from a public mirror".
