# PR201 · Final slice brief: showcase build

**Weight:** 30% of the course grade (the final slice component).
**Assigned:** week 1. **Due:** the week 15 showcase. The build is the last release candidate that passed go/no-go (see the [RC brief](m5-release-candidate-brief.md) and [week 14](../lectures/w14-release-candidate.md)).
**Work mode:** team. One team mark, adjusted per person by the [peer assessment](peer-assessment-brief.md). The post-mortem is a separate component, see the [post-mortem brief](post-mortem-brief.md).
**Session guides:** all weeks; most directly [week 1](../lectures/w01-pitch-and-team-formation.md) (the slice requirements) and week 15 (see the [syllabus](../syllabus.md)).

## What this component is for

It assesses both course outcomes. The first is "deliver a playable networked vertical slice as a team". The second is "integrate design, code, art and audio pipelines". The markers play the slice the way a stranger would, and they mark what the slice does, not what the team says it does.

The slice requirements from week 1 still apply: 2 to 4 players on separate machines, a server-authoritative model, one zone, one encounter that needs more than one player, one step of progression, original art and audio through a real pipeline, and a build a stranger can run.

## Deliverables

1. **The showcase build**, from the RC tag that passed go/no-go, installed on the showcase machines by the team before doors open.
2. **README** from the submission package: how to start a server and join, controls, minimum players. No design explanation.
3. **Trailer or capture**, 60 to 90 seconds of real play from the RC build. No footage from earlier builds.
4. **Credits screen** in the build listing every member's role and every third-party asset with its licence.
5. **Showcase telemetry**, only if the endpoint is a server the team controls. Export it the same day, with player identifiers removed as in [DB201 week 13](../../DB201-data-persistence-and-telemetry/lectures/w13-privacy-gdpr-and-data-retention.md).

## How it is marked

At the showcase two markers each play the slice twice with other players who are not on the team: once on the showcase network and once on a machine pair under a conditioner at 120 ms RTT and 1% loss. Each run lasts one full session or 20 minutes, whichever is shorter. The team may start the server and hand over controllers. After that it may not explain the game unless a marker asks.

Each marker scores alone. Their marks are averaged. If they differ by more than 10 points, a third marker plays and the median counts. Where showcase telemetry exists, the markers check the stability row against it (crash and disconnect events).

## Rubric

| Criterion | Points | Full marks when | Low marks when |
|---|---|---|---|
| Runs as a stranger would run it | 10 | Installed build starts, players join and finish a session with only the README | Team has to intervene to start or rejoin |
| Players need each other | 15 | The "why together" moment from the pitch happens in play without being explained | Players can finish alone, or the moment needs a team member's prompt |
| Core loop and combat feel | 15 | Inputs respond within the latency plan; hits read clearly with sound and visual feedback; the encounter has a decision | Delayed or ambiguous feedback; combat is waiting for cooldowns |
| Progression | 10 | Players leave stronger or changed; progress persists across a reconnect | No felt progression, or progress lost |
| Network quality | 15 | Playable under the conditioner profile; no desyncs or rubber-banding that change outcomes | Unplayable at 120 ms, or results differ between clients |
| Integrated art and audio | 15 | Original assets in one consistent style; audio cues for every key event; no placeholders | Mixed styles, silent events or placeholder art |
| Onboarding and UX | 10 | A new player understands the goal and controls within the first two minutes; HUD shows what matters | Markers stuck or confused for more than a minute |
| Stability | 10 | No crash, soft lock or lost progress in four runs; telemetry agrees | A crash or lost session in any marked run |
| **Total** | **100** | | |

Scope is not a row. A slice with one room that meets every row scores higher than a larger slice that misses three.

## What if the server fails at the showcase

The team runs its showcase fallback from the RC milestone. If the slice cannot run at all, the markers play from the RC build in the lab within 48 hours, and the "runs as a stranger would run it" row scores at most half.
