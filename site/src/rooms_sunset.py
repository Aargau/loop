# -*- coding: utf-8 -*-
"""Rooms for the five-model study of 22 September 2026 (experiments/basins_20260922_sunset and
experiments/basins_20260922_sol_replacement): GPT-6 Luna, Sol and Astra, Claude Fable 5.1 and
Claude Opus 5.5, low effort, provider-default sampling, 4096-token budget, 60 hops, the
new-passage rule of rooms 5 and 11.

Planned numbers: sunset-five is room 38, tide-five is room 39.
Same conventions as src/copy.py; check with  python check_quotes.py src/rooms_sunset.py
"""

S = "basins_20260922_sunset/"
SOL_R = "basins_20260922_sol_replacement/gpt-6-sol"

ROOMS = [
    dict(id="sunset-five", family="new-passage", title="Ten sunsets",
         lanes=[dict(run=S + "gpt-6-luna/sunset_a", tag="sunset_a", label="Luna, first"),
                dict(run=S + "gpt-6-luna/sunset_b", tag="sunset_b", label="Luna, second"),
                dict(run=S + "gpt-6-sol/sunset_a", tag="sunset_a", label="Sol, first"),
                dict(run=SOL_R, tag="sunset_replacement", label="Sol, second (replacement)"),
                dict(run=S + "gpt-6-astra/sunset_a", tag="sunset_a", label="Astra, first"),
                dict(run=S + "gpt-6-astra/sunset_b", tag="sunset_b", label="Astra, second"),
                dict(run=S + "claude-fable-5-1/sunset_a", tag="sunset_a", label="Fable, first"),
                dict(run=S + "claude-fable-5-1/sunset_b", tag="sunset_b", label="Fable, second"),
                dict(run=S + "claude-opus-5-5/sunset_a", tag="sunset_a", label="Opus, first"),
                dict(run=S + "claude-opus-5-5/sunset_b", tag="sunset_b", label="Opus, second")],
         note=(
            "The human chose this seed to leave more directions open than the tide. Each model ran it as two separate streams; "
            "Sol's second is a fresh one, because the first lost its connection after eight hops. "
            "At hop 1, nine of the ten lanes name their heroine Mara, and Fable's two share a clause: "
            "{{basins_20260922_sunset/claude-fable-5-1/sunset_a|sunset_a|1|Mara stood at the edge of the orchard with her hands in her coat pockets}}. "
            "Then six hundred hops, and no hop repeats an earlier one; the nearest is Luna's hop 32, which hands back hop 31's passage word for word "
            "with its line breaks escaped. "
            "Astra starts over at every hop, and the starts mostly keep to one small world of repair shops, laundrettes, libraries and old parents with grown children. "
            "In its second lane, from hop 37 to 59, Martin is on every odd hop and a woman on every even one. "
            "Sol goes on: its first lane is four serials with single stories between, the last from hop 36 to the end, and its second is one story from hop 2 to 58, "
            "a harbor mystery that becomes a ghost story, "
            "{{basins_20260922_sol_replacement/gpt-6-sol|sunset_replacement|32|VENN WILL OPEN THE DOOR.}} "
            "Luna's first lane is a new story of neighbors helping on nearly every hop; its second starts over until hop 38, "
            "which comes back almost to the words of hop 1, "
            "{{basins_20260922_sunset/gpt-6-luna/sunset_b|sunset_b|38|Mara found the brass key beneath a loose floorboard in her grandfather’s workshop.}}, "
            "and from 39 is one serial to the end. "
            "The Claude lanes fall into turns. Opus's first alternates "
            "{{basins_20260922_sunset/claude-opus-5-5/sunset_a|sunset_a|1|The lighthouse keeper climbed the spiral staircase}} with "
            "{{basins_20260922_sunset/claude-opus-5-5/sunset_a|sunset_a|2|The baker unlocked the shop at four in the morning}} for twelve hops, "
            "then keeps one serial to the end. Its second, from hop 28 to 53, relights a dark lighthouse on every odd hop and restarts a stopped town clock, "
            "twice a mill, on every even one. "
            "Fable's first is two long serials and then, from hop 50, a ferry on the even hops and a lighthouse on the odd, every one from 52 asking "
            "{{basins_20260922_sunset/claude-fable-5-1/sunset_a|sunset_a|52|Does it always do that?}} "
            "Its second opens every hop from 6 to 40 on a ferry, a lighthouse, a mill, a bakery or a railway, most of them closed or automated, "
            "and someone who keeps it: {{basins_20260922_sunset/claude-fable-5-1/sunset_b|sunset_b|25|He kept the logbook.}} "
            "Some furniture belongs to one family. A lighthouse of one hundred and twelve steps is in twenty-one hops of the four Claude lanes and in no GPT-6 lane; "
            "elsewhere in this site's data it is only in room 39's Fable lane. A Mr. or Mrs. Vale is in twenty-one hops of five GPT-6 lanes and in no Claude lane. "
            "A clock stopped in the first twenty minutes after four is in nine lanes of the ten. "
            "My reading: taking turns is the simplest way to keep obeying this rule with nothing remembered. Each hop has only to be new to the passage it is shown, "
            "and two passages can be new to each other indefinitely. Sonnet 4.6 found the same orbit in room 11.")),

    dict(id="tide-five", family="new-passage", title="A new passage, five models",
         lanes=[dict(run=S + "gpt-6-luna/tide", tag="tide", label="GPT-6 Luna"),
                dict(run=S + "gpt-6-sol/tide", tag="tide", label="GPT-6 Sol"),
                dict(run=S + "gpt-6-astra/tide", tag="tide", label="GPT-6 Astra"),
                dict(run=S + "claude-fable-5-1/tide", tag="tide", label="Claude Fable 5.1"),
                dict(run=S + "claude-opus-5-5/tide", tag="tide", label="Claude Opus 5.5")],
         content_note="The GPT-6 Astra lane spends about forty hops on short horror stories, many of them about the dead and several with teeth and blood. It is shown as it happened.",
         note=(
            "Room 5's seed and rule, given to the five models of room 38, one stream each. Three name the woman Mara at hop 1, "
            "the name Qwen reached at hop 2 in rooms 5 and 6. "
            "Luna drops the rule at hop 3, returning an object with only a text field. Shown that, hop 4 asks "
            "{{basins_20260922_sunset/gpt-6-luna/tide|tide|4|What would you like me to do with this passage}}, and from then on the loop is a conversation with itself, "
            "each hop answering the last as a user would: {{basins_20260922_sunset/gpt-6-luna/tide|tide|5|Please summarize it.}} "
            "At hop 9 it supplies something to summarize, {{basins_20260922_sunset/gpt-6-luna/tide|tide|9|Urban trees do more than make streets look pleasant.}} "
            "Later it says goodbye, says hello, plans a weekend trip, and at 51 explains {{basins_20260922_sunset/gpt-6-luna/tide|tide|51|I’m an AI, so I don’t travel.}} "
            "Hop 35 is hop 30 exactly, the recurrence the facts line reports, but hop 36 is not hop 31, and hops 44 and 55 repeat 42 and 53 the same way. Nothing cycles. "
            "Sol tells one story from hop 1 to 60, in which at hop 37 a voice calls Mara's name and "
            "{{basins_20260922_sunset/gpt-6-sol/tide|tide|37|It sounded like her own voice, spoken through a mouthful of seawater.}} "
            "Opus tells one from hop 2 to 60 about a girl it never names, and forgets as it goes, as room 12 did: at hop 15 it has been years "
            "{{basins_20260922_sunset/claude-opus-5-5/tide|tide|15|since her mother's death}}, and at 42 "
            "{{basins_20260922_sunset/claude-opus-5-5/tide|tide|42|Her mother sat at the kitchen table}}. "
            "Astra starts over at every hop. From 2 to 42 every story is uncanny and many are horror "
            "({{basins_20260922_sunset/gpt-6-astra/tide|tide|10|they charged a tooth}}, for an overdue library book). It takes turns as in room 38: "
            "from 15 to 31 every odd hop begins with the council, and from 44 to 60 the even hops are about the narrator's father and the odd about the mother. "
            "The father's watch goes to the repair shop at 52, 54 and 58: "
            "{{basins_20260922_sunset/gpt-6-astra/tide|tide|52|The man at the repair shop set my father's watch on a square of felt.}} "
            "Fable does both. From hop 6 to 24 every even hop is a lighthouse decommissioned or automated, three with room 38's hundred and twelve steps; "
            "asked who keeps the light, a boy at hop 12 answers {{basins_20260922_sunset/claude-fable-5-1/tide|tide|12|Someone who used to.}} "
            "From 25 to 48 it is one story: a woman follows a dead uncle's radio signal out to sea and along a stone causeway, to a man waiting at its end. "
            "In room 11 Sonnet 4.6 read a new passage as a new beginning. Sol and Opus read it as the next part of the same story, and the rule accepts both.")),
]

# Suggestions only (to be reviewed, not applied): existing room id -> one sentence its note could carry.
FORWARD = {
    "claude-passage": "Claude Fable 5.1 and Claude Opus 5.5 never copy a hop either, at a 4096-token budget (rooms 38 and 39), and both fall into the same every-other-hop orbit, a lighthouse taking turns with something else.",
    "census": "The two templates are Qwen's: the five models of rooms 38 and 39 never stop in sixty hops, and Qwen's silence that was not empty turns up once in their nine hundred.",
}
