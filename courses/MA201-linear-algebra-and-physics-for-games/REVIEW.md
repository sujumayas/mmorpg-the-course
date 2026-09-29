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
