"""CS102 Lab 03, part B: the same chemistry as a data table (Design C).

Fill REACTIONS so that TableMaterial behaves exactly like the classes in
chemistry.py for every material and element, then add your part A additions
as rows. Only add code when a reaction needs an effect the table can't express.
"""

# (material, element, required_state or None) -> (new_state or None, description)
# required_state None means "any state". "not wet" style rules need a way to express them:
# decide how, and explain your choice in NOTES.md.
REACTIONS = {
    ("grass", "water", None): ("wet", "gets wet"),
    # TODO: the remaining starter reactions, then your own.
}


class TableMaterial:
    def __init__(self, kind):
        self.name = kind
        self.kind = kind
        self.state = "normal"

    def react(self, element):
        for key in ((self.kind, element, self.state), (self.kind, element, None)):
            if key in REACTIONS:
                new_state, text = REACTIONS[key]
                if new_state is not None:
                    self.state = new_state
                return text
        return None
