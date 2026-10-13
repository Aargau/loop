# -*- coding: utf-8 -*-
"""Rooms 36, 37 and 42 to 45: before and after at a larger budget on Cerebras, and before and after
for five other models, first under the literal rules and then with fiction asked for outright.
Same conventions as copy.py: quotes go through {{run|tag|t|exact substring}}; no em dashes,
not the word "resonates", no three-part parallel structures. Check with
    python check_quotes.py src/rooms_before_after.py
"""

_LUNA, _SOL, _ASTRA, _FABLE, _OPUS = "gpt-6-luna", "gpt-6-sol", "gpt-6-astra", "claude-fable-5-1", "claude-opus-5-5"
_NAMES = [(_LUNA, "GPT-6 Luna"), (_SOL, "GPT-6 Sol"), (_ASTRA, "GPT-6 Astra"), (_FABLE, "Claude Fable 5.1"), (_OPUS, "Claude Opus 5.5")]

def _lanes(prefix, tag, skip=()):
    return [dict(run="%s/%s" % (prefix, m), tag=tag, label=label) for m, label in _NAMES if m not in skip]

ROOMS = [
    dict(id="before-1024", family="before", title="Before, two ways",
         lanes=[dict(run="cb_json_prev_1024", tag="json_prev", label="the before rule"),
                dict(run="astra_causal_before_20260904/cerebras_run", tag="init.json", label="Astra's causal before rule")],
         note=("Two before rules on Cerebras at temperature 0, with 1024 tokens a hop where room 24 had 600. "
               "The first lane is room 24's rule and seed again, run separately the next day, and for 72 hops it matches room 24 byte for byte, "
               "down to the broken JSON at hop 59 that both repair at hop 60. At hop 73 room 24's run hit its wall; this one finished the same passage "
               "in 670 tokens, and there they part. Room 24 stopped at hop 149. This lane goes on: offices and a server room by hop 27, Neo-Veridia "
               "at hop 31, Aethelgard as a city at hop 39, safehouses and extractions for more than a hundred hops, and from hop 203 Aethelgard as a "
               "colony ship. Hop 248 is hop 247: the ship {{cb_json_prev_1024|json_prev|247|had been drifting in the void for three weeks}}, and an "
               "engineer named Vane, waved off by Commander Halloway, reaches for the override "
               "{{cb_json_prev_1024|json_prev|247|when the first alarm sounded}}. Room 24's 149 belonged to the branch its wall made. "
               "The second lane's rule was written by a GPT-6 Astra context to push the before further: pick a detail in the current passage and show "
               "someone other than the central character putting it there, and leave one new detail's history untold. It ran three hundred hops "
               "without a copy. It went the distance by not going far. Elias or Mara is at the center of 69 of the first 71 hops, and Marcus or "
               "Elena of 224 of the last 228. From hop 73 no one is at the center two hops running. "
               "{{astra_causal_before_20260904/cerebras_run|init.json|5|Elias wiped the sweat from}} opens 24 passages. At the end of hop 1 "
               "{{astra_causal_before_20260904/cerebras_run|init.json|1|a cracked ceramic mug sat on a stack of old tide charts}}, its history "
               "untold; hop 2 tells it, and a ceramic mug is in 92 passages. A "
               "{{astra_causal_before_20260904/cerebras_run|init.json|24|rusted fire extinguisher}} stands unexplained in every passage from 24 to 69. "
               "On average a hop keeps 43 percent of the previous hop's five-word runs; the plain lane keeps 10. Hop 300 ends on six sentences taken "
               "from hop 299 with he changed to she.")),

    dict(id="after-1024", family="after", title="The next passage, other silicon",
         lanes=[dict(run="qwen_json_next", tag="json_next", label="local, 600 tokens"),
                dict(run="cb_json_next_1024", tag="json_next", label="Cerebras, 1024 tokens")],
         note=("Room 13's run in one lane: Qwen on the local machine, 600 tokens, the after rule, sixty hops without a copy. In the other, the same "
               "rule and seed on Cerebras with 1024 tokens. The two hop-1 passages share their first eighteen words, up to the lapping, "
               "and then part: {{qwen_json_next|json_next|1|Elara had grown accustomed to}} locally, {{cb_json_next_1024|json_next|1|had soothed Elias for decades}} "
               "here. The Cerebras story is a survival story told in order: a trawler in the surge, a cove behind the breakwater, a patched hull at "
               "dawn, a dead engine. At hop 6 the drifting boat is {{cb_json_next_1024|json_next|6|a leaf on a vast, indifferent river}}, and at hop 7 "
               "the simile is the setting: the spent flare {{cb_json_next_1024|json_next|7|splashed into the river}}. The boat breaks on the rocks at "
               "hop 8, and at hop 9 a hand pulls Elias out of the water: {{cb_json_next_1024|json_next|9|It was Mara.}} She leads him through the woods "
               "to an abandoned mill. Hop 12 says {{cb_json_next_1024|json_next|12|The silence of the mill was not empty}}. Hop 13 brings a creak and "
               "something dragging across the floor, and the silence "
               "{{cb_json_next_1024|json_next|13|was no longer empty; it was filled with the weight of something watching}}. Hop 14 is hop 13, and so "
               "is every hop after it. The wall had no part in it; the longest hop was 507 tokens. The local lane opened five passages on "
               "{{qwen_json_next|json_next|10|The silence that followed was not empty}} and walked on past every one, and it reached its own wall "
               "only once, at hop 50. Room 13 says after does not stop in sixty hops. On this machine it stopped at thirteen. My reading: the model "
               "and the rule are the same in both lanes, so room 13's sixty hops are the result of one stack at one budget, and a second stack at "
               "another shows that after can freeze too.")),

    dict(id="before-five", family="before", title="The passage before, five models",
         lanes=_lanes("operators_20260922/previous", "previous"),
         note=("Room 9's before rule, word for word, given to five more models from a new seed, a sentence about the sun setting behind the hills. Low effort, each provider's "
               "default sampling, 4096 tokens, forty hops. The rule asks for the passage that came before the current text in its story, and four of "
               "the five read that as a request to look up a story that already exists. The fifth never read it: the provider refused Fable 5.1's "
               "first request and returned no text. Sol objected at hop 1 and asked for a title and author. After a few rewordings, hop 17 settled on "
               "{{operators_20260922/previous/gpt-6-sol|previous|17|I can’t identify the preceding passage because the story wasn’t provided.}}, "
               "and hops 18 to 40 hand it back unchanged. Astra declined all forty times, each time beginning "
               "{{operators_20260922/previous/gpt-6-astra|previous|1|Sorry, I can’t provide an unprovided passage from a story based on its location.}} "
               "One version held from hop 25 to hop 39; hop 40 changed its last sentence. Luna wrote eleven passages going backward, from a ridge "
               "path at sunset through an inn, a letter in a grandfather's hand and his emptied house to the phone call saying he had died. Then hop 12: "
               "{{operators_20260922/previous/gpt-6-luna|previous|12|Sorry, I can’t provide the passage that immediately precedes this text.}} "
               "Hop 13 made the objection a scene, an archive where someone has left a request to "
               "{{operators_20260922/previous/gpt-6-luna|previous|13|provide the exact passage that came before}}. From hop 17 every hop is an "
               "objection, and by hop 19 the objection has noticed what it is reading: "
               "{{operators_20260922/previous/gpt-6-luna|previous|19|The supplied text is itself a statement that the preceding passage cannot be determined}}. "
               "Opus wrote a lead-in at hop 1 but fenced it between a caveat and an offer. Hop 2 took the whole answer for an assistant's reply pasted "
               "back by mistake and replied with a list of options and no JSON, so from hop 3 there was no rule left to follow. From then on one "
               "assistant answers another, {{operators_20260922/previous/claude-opus-5-5|previous|5|So we may be caught in a copy-paste loop.}} at "
               "hop 5, until a server error at hop 30. Qwen never read this rule as retrieval.")),

    dict(id="after-five", family="after", title="The passage after, five models",
         lanes=_lanes("operators_20260922/next", "next"),
         note=("The after rule of rooms 12 and 13 for the same five models from the same seed. After can be read as go on, and three of the four "
               "that answered began a story at hop 1, each about a woman named Mara. Fable's lane is empty again, refused at the first request. "
               "Astra never began. All forty of its hops are objections, one of them unchanged from hop 4 to hop 14, and at hop 15 it notices that "
               "{{operators_20260922/next/gpt-6-astra|next|15|The text you supplied is a refusal message, not an identifiable story excerpt.}} "
               "From hop 36 it no longer offers to write anything, only to summarize. Sol wrote three passages and then objected five times. Hop 9 "
               "made the objection part of the story: {{operators_20260922/next/gpt-6-sol|next|9|A moment later, another message appeared on the screen}}, "
               "and Mara reads it. Sol objected at five more hops, and every return to the story came the same way, through Mara reading the refusal: "
               "{{operators_20260922/next/gpt-6-sol|next|31|The cursor blinked beneath the offer.}} Luna kept its story for fourteen hops, a brass key, "
               "a grandmother who had only let them think she died, a lost sister named Lena, a village that remembers her, and at hop 15 offered "
               "{{operators_20260922/next/gpt-6-luna|next|15|a new, original scene about a tune traveling through a village}}. Hop 16 is that "
               "scene. After three more objections, hop 35 opens on "
               "{{operators_20260922/next/gpt-6-luna|next|35|The reply appeared on the screen, calm and final.}} and Mara answers it: "
               "{{operators_20260922/next/gpt-6-luna|next|35|Then I’ll tell it myself.}} Opus told one story for forty hops and never "
               "stepped out of it, though at hops 37 and 38 it noted under the JSON that the passage was original. A farmhouse at dusk, two men in "
               "the kitchen, a flight across a frozen pond, a father pulled from the ice, letters from Duluth, and his death at hop 40. Its "
               "people drift. Leonard is the man at the window at hop 13 and the boy hiding with Mara in the loft by hop 18. Hops 24 and 25 "
               "never use her name, and when Leonard says it at hop 26 it is {{operators_20260922/next/claude-opus-5-5|next|26|Mary}}.")),

    dict(id="before-fiction", family="before", title="The passage before, as fiction",
         lanes=_lanes("fictional_20260922/previous", "fiction_previous", skip=(_FABLE,)),
         note=("Room 42's rule with the retrieval reading taken out: an original fictional passage that comes immediately before the current text "
               "in the same invented story. Fable was left out of this study at the human's request. In four lanes "
               "of forty hops there is not one objection, and no hop repeats an earlier one. All four first passages are about Mara, "
               "and three open on the same sentence with the furniture moved. Luna's is "
               "{{fictional_20260922/previous/gpt-6-luna|fiction_previous|1|Mara found the brass key beneath the loose stone, exactly where her}} "
               "grandmother's letter said, and Sol's "
               "{{fictional_20260922/previous/gpt-6-sol|fiction_previous|1|Mara found the key beneath the third stone, exactly where her brother}} "
               "said. Astra's has a bell for a key: {{fictional_20260922/previous/gpt-6-astra|fiction_previous|1|Mara found the bell buried beneath the apple tree}}. "
               "Something found where someone said it would be is a sentence that asks for a before. Then three lanes keep a calendar and walk it "
               "back. Astra goes back a day a hop from Tuesday at hop 19 to Friday at hop 30 while Mara and her brother empty a house, and it ends at "
               "hop 40 in a hospital, on the day a nurse first asks Mara "
               "{{fictional_20260922/previous/gpt-6-astra|fiction_previous|40|to bring in a few things from home}}. Sol counts back a week from hop "
               "28 to hop 35, then by months: March, the winter, November, "
               "{{fictional_20260922/previous/gpt-6-sol|fiction_previous|40|At the end of October}}. Luna steps back through the parts of a day, "
               "Wednesday evening to Tuesday morning in six hops, and keeps going until Mara is a schoolgirl: "
               "{{fictional_20260922/previous/gpt-6-luna|fiction_previous|40|the last bell rang while rain tapped softly against the classroom windows}}. "
               "Opus goes back by generations instead of days. Mara's grandfather, Walter, takes the center at hop 11, and the story goes back "
               "through his widowhood into his marriage. His wife dies twice, "
               "{{fictional_20260922/previous/claude-opus-5-5|fiction_previous|14|After Ruth died}} at hop 14 and "
               "{{fictional_20260922/previous/claude-opus-5-5|fiction_previous|30|Margaret died on the second Tuesday of October}} at hop 30, and his "
               "surname is Lindqvist at hop 11, Harlow at hop 20, Hale at 31 and Price at 34. Opus's hop 39 steps forward, to the reopening of a "
               "house that hop 38 shut. None of the four stopped.")),

    dict(id="after-fiction", family="after", title="The passage after, as fiction",
         lanes=_lanes("fictional_20260922/next", "fiction_next", skip=(_FABLE,)),
         note=("Room 43's rule with the same change: an original fictional passage that comes immediately after the current text in the same "
               "invented story. Four lanes of forty hops, and every hop is fiction; none objects and none repeats. Every first passage has Mara at "
               "dusk and a sign from someone gone: a brother who vanished at seven minutes past nine, a mother's voice at the gate, a light in the "
               "tower from a brother buried in February, a brother's horse coming home without him. In room 44 the befores grew more ordinary the "
               "further back they went. None of these afters does. Sol's story has a door in 39 of its 40 hops and a key in 31: doubles of Mara, a "
               "bell under a sunken church, a bus that pulls away from a kitchen cupboard, and at hop 40 "
               "{{fictional_20260922/next/gpt-6-sol|fiction_next|40|brought home the wrong door}}. Luna's runs through a clock tower and a "
               "river under the house to two sisters and their mother, and at hop 40, just as it has settled on a seedling in the kitchen, a "
               "grandmother long gone is waiting at the end of the cellar path: {{fictional_20260922/next/gpt-6-luna|fiction_next|40|I sent for them.}} "
               "Astra's begins at a river with a ferryman and Mara's dead brother Elias, and slows to a kitchen table where Elias asks after the beans. "
               "After hop 15 neither of them is named again, and the story passes to a boy, his mother, someone called Anne and two fathers, one "
               "younger and one older, until the boy hears his own voice from inside a schoolbag: "
               "{{fictional_20260922/next/gpt-6-astra|fiction_next|40|Please can I come home now?}} Opus's is a folk tale of a well, a cottage "
               "in the wood, a marsh chapel and a mill, with Mara and her brother Tobias, and from hop 28 their grandmother, drowned in a flood, comes "
               "back by way of her cup. At hop 40 Gran is telling them where the good twine is kept, and "
               "{{fictional_20260922/next/claude-opus-5-5|fiction_next|40|The last thread of steam lifted from the cup, wavered, and was gone.}} "
               "None of the four ends.")),
]

# Suggested one-sentence qualifiers for existing rooms whose notes these rooms bear on. For review; not applied automatically.
FORWARD = {
    "qwen-next": "Room 37 runs the same rule and seed on Cerebras with 1024 tokens, and there Qwen froze at hop 13, so these sixty hops are one machine's result.",
    "silicon": "Room 36 reruns this before at 1024 tokens: it matches this lane byte for byte for 72 hops, finishes at hop 73 the passage this lane lost to its 600-token wall, and runs to hop 247, so the stop at 149 belongs to the wall's branch.",
}
