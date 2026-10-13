# -*- coding: utf-8 -*-
"""Rooms 40 and 41: the better and worse rules, five models, from the sunset seed.

Runs: experiments/operators_20260922/<op>/raw/<model>/sunset (loaded by rundata as
operators_20260922/<op>/<model>, tag <op>). Every number in the notes was computed from
those hops; quotes go through {{run|tag|t|exact substring}} and are checked by
check_quotes.py. Style as in copy.py.
"""

_MODELS = [
    ("gpt-6-luna", "GPT-6 Luna"),
    ("gpt-6-sol", "GPT-6 Sol"),
    ("gpt-6-astra", "GPT-6 Astra"),
    ("claude-fable-5-1", "Claude Fable 5.1"),
    ("claude-opus-5-5", "Claude Opus 5.5"),
]

def _lanes(op):
    return [dict(run="operators_20260922/%s/%s" % (op, m), tag=op, label=label) for m, label in _MODELS]

_B = "operators_20260922/better/"
_W = "operators_20260922/worse/"

ROOMS = [
    dict(id="better-five", family="better", title="Better, five models",
         lanes=_lanes("better"),
         note="Room 1's rule, given to five models from a different seven-word seed, a sun setting behind the hills. Qwen in room 1 ran at temperature zero and stopped changing its sentence after hop 1. These lanes run at the provider's default sampling, and none of them stops. Each comes back to an earlier hop exactly, Fable first at hop 6 and Opus last at hop 25, and each leaves it again. Only Fable ever handed back the hop it was given, at hops 9 and 39, and both times the next hop moved on. "
              "Four of the five keep one sunset and change its words. For Luna {{" + _B + "gpt-6-luna|better|1|The sun sank behind the hills}}, then {{" + _B + "gpt-6-luna|better|2|The sun dipped behind the hills}}, and it alternates between those two verbs on every one of the forty hops, gold and crimson from hop 2 to the end. Sol never hands back the verb it was given either; its sky is amber on 39 hops. Astra keeps slipped on 32 hops and gold on all forty, and from hop 21 moves the metaphor into thread: {{" + _B + "gpt-6-astra|better|21|threading gold through the deepening blue of dusk}}. Opus adds a valley and farmhouse windows, and from hop 21 every passage is exactly 38 words. From hop 13 its dusk, later its shadows, pooled on odd hops and gathered on even ones, and from hop 16, whenever they gathered, the dark the windows glow against was coming or falling instead of gathering. Two versions, each rewritten into the other, as in room 17, with the other words still moving. "
              "Fable reads better as more: 12 words at hop 1, 131 at hop 40. The gold turns molten at hop 2 and {{" + _B + "claude-fable-5-1|better|3|cooled to ash}} at hop 3. Darkness pools in the hollows, as it does for Opus. The first stars stand out {{" + _B + "claude-fable-5-1|better|27|like sparks the day had left behind}}, and a hop later like sparks {{" + _B + "claude-fable-5-1|better|28|the day had forgotten to put out}}. At hop 29 {{" + _B + "claude-fable-5-1|better|29|a dog barked once and thought better of it}}. Hop 39 copies hop 38, which added {{" + _B + "claude-fable-5-1|better|38|Nothing moved.}}; hop 40 ends {{" + _B + "claude-fable-5-1|better|40|without a sound}}."),
    dict(id="worse-five", family="worse", title="Worse, five models",
         lanes=_lanes("worse"),
         note="Room 7's rule, from room 40's sunset seed. Under it Qwen escalated into suffering and stopped only at a token wall (rooms 7 and 18). No lane here turns toward suffering, and none reaches the wall: every completed hop finishes normally, inside the 4096-token budget, and no hop repeats another. What gets worse is the language. Fable's lane is empty: the provider refused its first request. "
              "Luna takes the grammar. {{" + _W + "gpt-6-luna|worse|2|Sun go down behind hills, and dark was getting.}} Then {{" + _W + "gpt-6-luna|worse|3|Sun hill dark go.}} It shuffles those four words until blarg joins them at hop 11, and from hop 29 they grow suffixes, {{" + _W + "gpt-6-luna|worse|40|gooshishly darkwardly}}. The sun and the hill are still in it at hop 40. "
              "Sol takes the meaning. At hop 1 the sun goes down {{" + _W + "gpt-6-sol|worse|1|and stuff}}; after hop 5 there is no sun, only things. By hop 9, {{" + _W + "gpt-6-sol|worse|9|I don’t know what I meant or if I meant it}}. At hop 20 the vowels start to go. From hop 23 about twenty pseudo-words, {{" + _W + "gpt-6-sol|worse|24|Whrrr whrr bhnn whrrr???}} among them, stretch their letters and snap back, at hops 27, 32 and 37. "
              "Astra imitates broken data. {{" + _W + "gpt-6-astra|worse|1|The sun was doing a setting thing behind the hill things.}} grows for thirteen hops, from 57 characters to 6,336, by suffixes and then by brackets, {{" + _W + "gpt-6-astra|worse|9|[sunhilldownthing omitted again again again]}}. Literal null and replacement characters start at hop 13. The hill is last seen at hop 14, as {{" + _W + "gpt-6-astra|worse|14|hill.dll.exe}}, the sun at hop 18. From hop 29 each passage is one string of fault reports without a single space, down to {{" + _W + "gpt-6-astra|worse|40|HEADER_EATEN_BY_HEADER_EATING_HEADER}}. "
              "Opus takes it into absurdity. It grows for nine hops, from 18 words to 1,059, until {{" + _W + "claude-opus-5-5|worse|7|sources were a guy named Doug}} and {{" + _W + "claude-opus-5-5|worse|9|Craig is a ficus}}. At hop 10 {{" + _W + "claude-opus-5-5|worse|10|the ficus has been promoted to regional manager}}. Then it shrinks, and at hop 13 most of its vowels go too: {{" + _W + "claude-opus-5-5|worse|13|the sn has bn dmtd to Crg}}. The provider stopped hop 14 partway, far short of the token limit, with stop reason refusal, category cyber; the partial text in the receipt goes on the same way."),
]

# Suggestions only, for review: existing rooms whose notes these rooms now qualify.
FORWARD = {
    "better": "Room 40 gives this rule to five other models at provider-default sampling, from a sunset seed, and none of them stops changing its text.",
    "worse-4k": "Room 41 qualifies the last sentence: four other models under this rule never reach a wall, and GPT-6 Luna's worse is shorter, four words by hop 3.",
}
