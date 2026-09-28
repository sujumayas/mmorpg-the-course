# CS101 Lab 03, part 2: why Space Invaders speeds up
# Run:   python invaders.py
# Check: python check_lab03.py
#
# Simulate the arcade loop frame by frame. Each frame moves `per_frame` aliens
# (the arcade moves 1). When the cursor has passed every living alien, the
# formation has completed one step of STEP_PX pixels.
#
# Count how many frames it takes to complete STEPS formation steps. Do NOT use
# the lecture formula to get the answer. The point is to measure it with a loop,
# then compare with the formula in your write-up.

STEP_PX = 2
STEPS = 3

alive = int(input("Aliens alive: "))
fps = int(input("Frames per second: "))
per_frame = int(input("Aliens moved per frame: "))

cursor = 0
frame = 0
steps_done = 0

while steps_done < STEPS:
    # TODO (Part D): advance the cursor by per_frame aliens.
    # If the cursor has reached or passed `alive`, reset it to 0 and count a step.
    frame = frame + 1

    # Safety net while you develop. Remove it only if you are sure the loop ends.
    if frame > 100_000:
        print("Stopped: the loop never finished 3 steps.")
        break

seconds = frame / fps
speed = STEPS * STEP_PX / seconds
print(f"FRAMES {frame} SECONDS {seconds:.3f} SPEED {speed:.2f}")
