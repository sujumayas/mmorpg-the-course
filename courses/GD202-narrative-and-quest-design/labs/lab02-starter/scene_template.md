# Scene title

**Setting:** one sentence.
**Characters:** the player character and at most two others.
**The choice:** scene number, the two options as the player sees them, and the flag it writes.

## Scene 1

Prose and dialogue. Mark shared text normally.

## Scene 2 (choice)

> OPTION A: text the player sees
> OPTION B: text the player sees

Write `SET flag_name = A` or `SET flag_name = B` after each option.

## Scene 3

Shared text. At each acknowledgement, write both versions like this:

{flag_name == A}
Line for players who chose A.
{flag_name == B}
Line for players who chose B.
{end}

Continue to your final scene. At least one acknowledgement must be heavy (a whole beat that differs).
