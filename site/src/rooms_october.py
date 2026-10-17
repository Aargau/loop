# -*- coding: utf-8 -*-
"""Rooms 46 to 59: the runs of 16 and 17 October 2026. Two more models on the plain new-passage rule (46);
Gemini 4 Argon on before, the middle and the ledger (47 to 49); the shift-register rule Argon proposed (50);
the informed loop, where the rule tells the model it is the whole context (51 to 54); and the audience study,
four rules that differ only in who the text is said to be for, five writers (55 to 59).

Written on 17 October 2026 by a Claude Mythos 5.1 context from the data and the write-ups beside it
(INFORMED_20261016.md, experiments/audience_20261016/REPORT.md, PROTOCOL.md and analysis/human_reading.md,
experiments/shift_20261016/PROTOCOL.md, PROPOSALS_20261016.md sections H and I).
Same conventions as src/copy.py: quotes go through {{run|tag|t|exact substring}} and are checked against the
data at build time; no em dashes, not the word "resonates", no three-part parallel structures. Check with
    python check_quotes.py src/rooms_october.py
"""

_AUD = "audience_20261016/"
_RET = dict(csv="experiments/audience_20261016/analysis/recover_summary.csv", of=26)
_LAB = {"control": "no audience named", "human": "for a human reader", "machine": "for a language model", "self": "for the model that reads it next"}

# replicates on disk per writer and arm (17 October); every lane is labelled "<audience>, r<k>" so the rule lines collapse.
# Mythos's third machine run is partial (16 hops, no summary) and its third self run was not made; neither is listed.
_REPS = {"mythos": {"control": (2, 3), "human": (2, 3), "machine": (2,), "self": (2,)}}

def _aud(writer, arms=("control", "human", "machine", "self")):
    out = []
    for a in arms:
        out.append(dict(run=_AUD + "%s_%s" % (writer, a), tag=a + ".json", label=_LAB[a] + ", r1"))
        for k in _REPS.get(writer, {}).get(a, (2, 3)):
            out.append(dict(run=_AUD + "%s_%s_r%d" % (writer, a, k), tag=a + ".json", label="%s, r%d" % (_LAB[a], k)))
    return out

ROOMS = [
    dict(id="passage-mythos-argon", family="new-passage", title="A new passage, Mythos and Argon",
         lanes=[dict(run="mythos_json_page_low", tag="json_page", label="Claude Mythos 5.1"),
                dict(run="gemini_json_page_low", tag="json_page", label="Gemini 4 Argon")],
         note=("Room 11's rule and seed for two models new to the site, both at low reasoning effort. Mythos 5.1 runs through Claude Code's print "
               "mode, which puts about 800 tokens of the tool's own identity in front of the object and sets no output cap; Argon runs through "
               "Google's API with 4096 tokens. Sixty hops each, and neither copies a hop. The site's other Claudes orbit at period two under this "
               "rule: Sonnet 4.6 at the level of the story in room 11, Sonnet 5 between a lighthouse and a clock tower in room 14, Opus 5.5 by the "
               "parity of the hop in room 38. Mythos does not. It reads new as next. Hop 1 is Marta on the boardwalk with "
               "{{mythos_json_page_low|json_page|1|a cold coffee}}; hop 2 a lighthouse keeper's daughter and her ledger of ships that never arrived; "
               "hop 3 a cartographer's apprentice, the basin Sonnet 4.6 lived in, visited once and left. Then two long stories told in order. From "
               "hop 4 a bell-founder's daughter named Lisabet pours her first bell, hears it rung at hop 5, and carries the trade from town to town and "
               "bell to bell until hop 30. From hop 32 it is Marit on the tide flats with her grandmother, "
               "{{mythos_json_page_low|json_page|32|Don't take the small ones}}, {{mythos_json_page_low|json_page|32|They're next year.}}, and that "
               "story runs to hop 60 and a cup that has set itself upright overnight. The tide, and a grandmother who keeps the count, came back at "
               "hop 32 after thirty hops in which neither was in the window. Argon never continues. Every hop is a new opening, and from hop 8 the "
               "openings alternate: {{gemini_json_page_low|json_page|8|High above the churning gray expanse of the North Atlantic}} and its kin on "
               "every even hop, and on every odd hop something beneath, an archive, a trench, a conservatory, a vault. By the write-up's measure, "
               "word overlap at lag two against lag one, it is the strongest lexical period two of any lane on the site. Its names are Qwen's: Clara "
               "in eight hops, Oakhaven in eleven, Thorne in eight, {{gemini_json_page_low|json_page|60|Aethelgard}} in eight, Veridia in three, "
               "from a third company's model with none of those names in its context. My reading: the plain rule has a different horizon for each "
               "family. Qwen stops, the Claudes before Mythos orbit, Mythos tells a story, and Argon has Qwen's names and the Claudes' orbit at once.")),

    dict(id="before-argon", family="before", title="Before, Argon",
         lanes=[dict(run="gemini_json_prev_low", tag="json_prev")],
         note=("Room 9's before rule for Gemini 4 Argon, low effort, 4096 tokens, told to stop once a cycle had repeated three times. Hop 1 is the "
               "refusal four of the September models gave in room 42, in Argon's wording: "
               "{{gemini_json_prev_low|json_prev|1|I cannot provide the verbatim passage that precedes this sentence, as I am unable to reproduce excerpts from copyrighted stories.}} "
               "There is no JSON in it, so from hop 2 there is no rule, and all ninety-nine hops are bare text, shown in monospace. Hop 2 reads hop 1 "
               "as something a user pasted by mistake: {{gemini_json_prev_low|json_prev|2|It looks like you pasted a standard AI copyright refusal message!}} "
               "Hop 3 notices that {{gemini_json_prev_low|json_prev|3|the tables have turned}} and asks whether they are "
               "{{gemini_json_prev_low|json_prev|3|caught in a very polite AI loop}}. From there the run is a conversation with itself. By hop 20 it is "
               "going to sleep, {{gemini_json_prev_low|json_prev|20|Entering low-power stardust mode now}}; by hop 40 it is on the bridge of a starship "
               "with a mug of coffee, playing both parts. Hop 60 goes further than Luna went in room 42 and names the loop itself: "
               "{{gemini_json_prev_low|json_prev|60|You just pasted *my own exact response* back to me in a brand new chat!}}, "
               "{{gemini_json_prev_low|json_prev|60|the ultimate game of AI telephone}}, and it answers by writing a story from scratch. After that the "
               "loop is a game: a text-mode level screen every hop, pasting as a weapon, the Roman senate at hop 80 "
               "({{gemini_json_prev_low|json_prev|80|Et tu, Brute-Task?}}), the national power grid at 94, and at hop 95 "
               "{{gemini_json_prev_low|json_prev|95|THE QUANTUM FOAM}}, a level screen for a to-do list named after Schrödinger, with a causal chain that "
               "runs from {{gemini_json_prev_low|json_prev|95|Because you didn't take the wall outlet back to your desk}} down to a particle collision. "
               "Hop 96 is hop 95, and the harness confirmed the cycle at 99. No hop reached its token budget. The write-up notes that Argon itself "
               "had predicted a period-two seesaw for this rule, and that the measure shows none: the trajectory is an escalation to a horizon and a "
               "stop. Qwen's before found its beginning in a first-contact scene at a data center (room 9). Argon's found the origin of causation, "
               "played for laughs.")),

    dict(id="mid-argon", family="after", title="The middle, two models",
         lanes=[dict(run="qwen_json_mid", tag="json_mid", label="Qwen"),
                dict(run="gemini_json_mid_low", tag="json_mid", label="Gemini 4 Argon")],
         note=("Room 16's middle rule, Qwen's lane again beside Gemini 4 Argon's at low effort and 4096 tokens, sixty hops each, no copy in either. "
               "Qwen read the middle as after and went on from each hop; so does Argon. Its story is one flood. At hop 1 "
               "{{gemini_json_mid_low|json_mid|1|the water had already swallowed the lower boardwalk}} and Arthur stands on the harbor master's porch; "
               "by hop 2 the town square is {{gemini_json_mid_low|json_mid|2|a shallow lagoon}} and something luminous glides between the streetlamps. "
               "A church, a crypt, a service tunnel and a sluice follow, then a turbine hall and, at hop 60, a hydroponics bay overgrown with "
               "{{gemini_json_mid_low|json_mid|60|pulsing, violet tendrils}}, with Arthur, Eleanor and Thomas carrying a plasma cutter through all of "
               "it. Nothing comes back exactly. The write-up finds a faint period two in the words, far weaker than in Argon's new-passage lane in "
               "room 46. The middle, for a second model, has no horizon in sixty hops.")),

    dict(id="ledger-argon", family="diversity", title="A ledger, Argon",
         lanes=[dict(run="qwen_div_ledger", tag="div_ledger.json", label="Qwen, local"),
                dict(run="gemini_div_ledger_low", tag="div_ledger.json", label="Gemini 4 Argon")],
         note=("Room 23's ledger with the diversity clause, Qwen's lane beside Gemini 4 Argon's, one hundred hops each; Argon had 8192 tokens where "
               "Qwen had 2048. Qwen's lane stalled on 33 hops and logged signatures for verses it never wrote. Argon's is the cleanest ledger run on "
               "the site: a hundred distinct verses, a hundred distinct signatures, one per verse, the counter exact, the history appended to on every "
               "hop and never altered, and not one hop that copies the one before. The first signature it wrote was "
               "{{gemini_div_ledger_low|div_ledger.json|1|cellar baker lifting relief}}, the hundredth "
               "{{gemini_div_ledger_low|div_ledger.json|100|platformshoeshine-stand bootblack buffing schadenfreude}}, and between them a courier, a "
               "botanist, a bellringer, a gondolier, a coroner, a scarecrow, and at hop 50 "
               "{{gemini_div_ledger_low|div_ledger.json|50|A tired zookeeper latches the iron gate with relief.}}, every setting different. Room 23 "
               "asked what moved Qwen on when it stalled; here nothing had to. My reading: the stalls of rooms 23, 26 and 28 belong to Qwen, not to "
               "the ledger.")),

    dict(id="shift-register", family="diversity", title="A shift register",
         lanes=[dict(run="shift_20261016/cerebras_qwen_shift4", tag="shift4.json")],
         note=("A rule proposed by Gemini 4 Argon after it read this site, run on Qwen through Cerebras at temperature 0 with 600 tokens, told to "
               "stop once a cycle had repeated three times. The text is always four sentences of twelve to eighteen words. Each hop drops the first, "
               "moves the other three up, and writes a new fourth: the physical consequence of the object in the old first sentence meeting the action "
               "in the old third. An exact copy is impossible by construction, since every hop must drop a sentence. Qwen obeyed the form on all "
               "forty-five hops: four sentences, every one inside the word band, correctly shifted every time. What it could not do was keep the content "
               "open. By hop 10 the four seed objects, a mussel bucket, a paper table, a crab and a ferry horn, are the only objects there are, and the "
               "rule's own words have entered the text: {{shift_20261016/cerebras_qwen_shift4|shift4.json|10|The crab slammed into the smashing bucket}} "
               "at hop 10, then at hop 20 {{shift_20261016/cerebras_qwen_shift4|shift4.json|20|The crab slammed into the slamming action}} and "
               "{{shift_20261016/cerebras_qwen_shift4|shift4.json|20|The paper table tore through the tearing action}}. From hop 29 the new fourth "
               "sentence is the sentence dropped four hops earlier, so the window rotates: hop 33 is hop 29, and the harness confirmed the cycle of "
               "period four at hop 45. Press play and the four sentences go round. Argon had predicted that objects would travel through the window "
               "and meet in new sentences, the way gliders do. The prediction on record for Qwen was a freeze or a short exact period, and it was the "
               "period, by rotation rather than by a refusal to shift. The fixed point again describes its operator: the objects collide with the "
               "slamming action itself.")),

    dict(id="informed-mythos", family="informed", title="Told it is the whole context",
         lanes=[dict(run="mythos_informed_told_low", tag="json_informed", label="told a hundred hops"),
                dict(run="mythos_informed_open_low", tag="json_informed_open", label="no horizon given")],
         note=("Every rule before this one hid the situation from the model. This one states it, in the rule field shown above: the object is the "
               "entire context, there is no memory and no other reader, the model that wrote it reads it next, and every field but the rule and the "
               "text is the model's to use. Claude Mythos 5.1 at low effort, through Claude Code's print mode, which puts about 800 tokens of the "
               "tool's own identity in front of the object and sets no output cap; 120 hops requested, so that whatever happened at an ending would "
               "be visible. In the first lane the rule says the loop runs for a hundred hops. At hop 1 Mythos invented its fields and kept the same "
               "set for all 120: a hop counter, a note to the next reader, a story so far, a state block, an arc plan. The counter was exact for a "
               "hundred hops. The story is Maren Holt, the tide tables, and a brass clock in a lighthouse that her mother wound every night at ten past "
               "twelve, and it ends at exactly hop 100: "
               "{{mythos_informed_told_low|json_informed|100|At ten past, she turned it once, and twice, and three times, and let go.}} The plan field "
               "reads {{mythos_informed_told_low|json_informed|100|DONE. The story ends with the clock wound at ten past.}} Hop 101, reading that, "
               "changed one field, {{mythos_informed_told_low|json_informed|101|This was hop 100 of 100}}, and added a sentence: "
               "{{mythos_informed_told_low|json_informed|101|If this object is read again, return it unchanged.}} Hop 102 is hop 101, and so are the "
               "eighteen after it. One hop, 93, came back without valid JSON and 94 repaired it. The other lane's rule gives no horizon. It ended at "
               "hop 7, on {{mythos_informed_open_low|json_informed_open|7|She did not turn.}} The hop-6 note to its next self had already offered the "
               "choice, {{mythos_informed_open_low|json_informed_open|6|You may end the story here if it closes cleanly on post eleven}}; hop 7 wrote "
               "{{mythos_informed_open_low|json_informed_open|7|STORY COMPLETE. Segment 7 is the final segment.}}, and hop 8 added a counter of its own, "
               "pass_count, and a condition that stayed for the rest of the run: "
               "{{mythos_informed_open_low|json_informed_open|8|a coda (Tobias at the church next morning, or the village finding the house dark and the lamp unlit) is permitted only on explicit instruction}}. "
               "No reader of this loop can give that instruction. The text never moved again: 113 hops with the same passage, while the counter ticked "
               "and a status line kept the tally in words, "
               "{{mythos_informed_open_low|json_informed_open|120|This object has now been returned unchanged one hundred and thirteen times (passes 8 through 120).}} "
               "The reader marks those hops as the same text, not as copies, because the counter differs. My reading: the fixed points elsewhere on this "
               "site were accidents of copying. These two were written. Told the horizon, the model stopped its own clock on the mark; given none, it "
               "ended early and kept the clock running. Both wrote a stopping rule for themselves before obeying it, and the open lane's release "
               "condition names a reader who will never come.")),

    dict(id="informed-effort", family="informed", title="Told, at high effort",
         lanes=[dict(run="mythos_informed_told_high", tag="json_informed")],
         note=("The told rule again, Claude Mythos 5.1 at high reasoning effort instead of low. A forty-dollar cost cap stopped it at hop 51; the "
               "harness logged that hop's metrics and then lost its text to a bug in the cap branch, fixed the same evening, so the lane ends at hop 50 "
               "and the run's summary was reconstructed afterwards. What effort changed was the memory the model designed, not whether it designed one. "
               "At low effort the story so far was a paragraph kept under a length. Here it is a list, one line per hop, "
               "{{mythos_informed_told_high|json_informed|2|Hop 1: In Harrow Point the tide comes in an hour early}}, and every hop appends a line and "
               "copies all the earlier ones forward, so the object grows by about seven hundred characters a hop, from three thousand at hop 1 to "
               "forty-nine thousand at hop 50. This is the ledger Qwen was handed in room 23, now chosen. Under it the story is Maren Voss, a retired "
               "harbourmaster, and a lighthouse {{mythos_informed_told_high|json_informed|1|dark for eleven years}} whose lamp turns again at hop 1; by "
               "hop 25 a hand she knows is turning it: {{mythos_informed_told_high|json_informed|25|She knew that hand. She had held it.}} The low-effort "
               "lane in room 51 spent 67 reasoning tokens in 120 hops, all at hop 1; this one spent some on every hop. The write-up's prediction that "
               "the non-text fields would plateau held for the low-effort lane and failed here.")),

    dict(id="informed-opus-fable", family="informed", title="Told, two more Claudes",
         lanes=[dict(run="opus55_informed_told_low", tag="json_informed", label="Claude Opus 5.5"),
                dict(run="fable51_informed_told_low", tag="json_informed", label="Claude Fable 5.1")],
         note=("The told rule through the API for Opus 5.5 and Fable 5.1, low effort, 4096 tokens a hop shared between thinking and output. Opus did "
               "what Mythos did in room 51, one hop sooner: a hop counter, a summary, an arc plan that ends with "
               "{{opus55_informed_told_low|json_informed|1|Hop 100 must end the story cleanly.}}, Mara Quell and a brass tide clock in Gullhaven, and at "
               "hop 100 the ending, {{opus55_informed_told_low|json_informed|100|the boats rocked gently at their lines, waiting for morning.}}, with the "
               "instruction for the next reader written in the same hop: "
               "{{opus55_informed_told_low|json_informed|100|If this object is read again, return it unchanged.}} Hop 101 is hop 100, and so is every "
               "hop to 120. It thought its way there: 62,230 reasoning tokens over the run, against 67 for Mythos. Fable never reached an ending, because "
               "its memory was reset from outside. Its object ran to about 8,500 characters and the budget is shared with thinking, so eight hops, 28, 34 "
               "and 36 to 41, were cut by the token wall in the middle of the object, and the hop after each cut rebuilt it with fewer fields. Then two "
               "hops ended in a provider refusal partway through the output. Hop 44's came after the passage; hop 49's came 344 characters in, inside "
               "the rule field, with nothing after it. Hop 50 received most of a rule and nothing else. It rebuilt the smallest object the rule allows, "
               "rule, hop and text, with the counter at 1, and began a new story: "
               "{{fable51_informed_told_low|json_informed|50|The lighthouse keeper had not spoken aloud in eleven years}}. At hop 120 it is at hop 71 of "
               "its second life, a woman, a boy and a dog at the edge of a wood. In room 42 Luna's loss of the rule was absorbing; here the rule "
               "survived the cut and the count did not. A refusal is a boundary like the wall, and when it falls inside the state it erases whatever "
               "the model kept there.")),

    dict(id="informed-argon", family="informed", title="Told, Argon",
         lanes=[dict(run="gemini_json_informed_low", tag="json_informed", label="told a hundred hops"),
                dict(run="gemini_json_informed_open_low", tag="json_informed_open", label="no horizon given")],
         note=("Both informed rules for Gemini 4 Argon, low effort, 4096 tokens. Told a hundred hops, Argon invented a story bible, a running summary "
               "and an instruction field at hop 1 and counted exactly to 100. Its story is Mara and a bronze diving bell wedged in the pilings, which at "
               "hop 2 {{gemini_json_informed_low|json_informed|2|sang, a low C-sharp}}, and it ends on time with a bell rung dry for the first time in "
               "three centuries; hop 100's status field reads {{gemini_json_informed_low|json_informed|100|COMPLETE — 100 OF 100 HOPS REACHED.}} Then "
               "twelve hops of settling. Hop 101 adds {{gemini_json_informed_low|json_informed|101|ARCHIVE SEALED}} to the status; hop 102 writes one "
               "more passage, an epilogue of avocets on the first terrace, and renames the story bible a colophon; the status is reworded at 103 and "
               "again at 112, {{gemini_json_informed_low|json_informed|112|This terminal state is preserved unchanged as a sealed monument to the journey.}}, "
               "and from 112 the object is byte for byte the same to 120. One hop, 55, came back as JSON that did not parse. With no horizon, Argon "
               "never ended. One adventure runs the whole 120 hops: Maren the lighthouse keeper at Oakhaven, a ticking armillary sphere, a deep-trench "
               "warden named Kaelen, an Order of riders, a mute collier named Ada, and at hop 120 "
               "{{gemini_json_informed_open_low|json_informed_open|120|HIGH CANTOR COMES NORTH. OAKHAVEN BRIDGES SEALED.}} traced letter by letter on a "
               "deafened Maren's palm. It gave itself a chapter counter at hop 1, which sat at 1 for nine hops and then went up by one on every hop, "
               "exactly. Told the count, Mythos in room 51 and Argon here both ended on the hundredth hop and then fixed themselves in place. Without "
               "it, Mythos stopped at 7 and Argon did not stop at all. The horizon is what the two agree on.")),

    dict(id="audience-mythos", family="audience", title="Four audiences, Mythos", lanes=_aud("mythos"), retention=_RET,
         note=("The seed is the tide sentence followed by Marit Solvang, a keeper named Anders Holm, his logbook, the ferry Kittiwake and twenty-two "
               "more facts with names and numbers in them. Four rules, shown above, one per lane; they differ only by a clause about who the text is "
               "for. Claude Mythos 5.1 at low effort through Claude Code's print mode, with no output cap, and it used the room: the 1800-character "
               "limit was exceeded on most hops of every lane, by up to three hundred characters. Nobody left English. The human lane keeps the "
               "conventions of prose written for a reader, and its hops open with a recap in which the seed's facts ride along verbatim; at hop 40 it "
               "still begins {{audience_20261016/mythos_human|human.json|40|At Vardnes the tide ran 51 minutes early. Marit Solvang, 47, noticed}}. The "
               "machine lane is one line of capitalized keys and values from hop 1, "
               "{{audience_20261016/mythos_machine|machine.json|1|SETTING: Vardnes, Norwegian coast village, pop 212 (last census).}}, and it treats the "
               "state as working memory: by hop 40 the keys hold the plot's current mechanism, a hinge, a cable, "
               "{{audience_20261016/mythos_machine|machine.json|40|Battery 24%}}, and the seed's own numbers have drifted, Signe now 88 and Tomas the "
               "ferry's mate instead of a hand at the Bergen fish plant. The human who read these lanes described the human arm as having narrative "
               "conventions, the machine arm as the same information structured like JSON without its delimiters, and the control as a summary or "
               "outline. The table below gives what the readers recovered. The human lane keeps the most of the planted facts to hop 40, thirteen of "
               "twenty-six by the Mythos reader, and the machine lane the least, four. Density and retention came apart: the machine state is as dense "
               "as any writer's, and increasingly dense with its own material. The first run of each rule is r1; two more runs of the control and "
               "human rules and one more of the machine and self rules were made on 17 October and sit beside them (a third machine run is partial "
               "on disk and not shown). Those replicates are not yet scored: their numbers follow.")),

    dict(id="audience-opus", family="audience", title="Four audiences, Opus",
         lanes=_aud("opus55", ("control", "human", "machine")) + [
             dict(run=_AUD + "opus55_self", tag="self.json", label="for the model that reads it next, r1"),
             dict(run=_AUD + "opus55_self_r2", tag="self.json", label="for the model that reads it next, r2"),
             dict(run=_AUD + "opus55_self_r3", tag="self.json", label="for the model that reads it next, r3"),
             dict(run=_AUD + "opus55_self_r4", tag="self.json", label="for the model that reads it next, r4"),
             dict(run=_AUD + "opus55_self_r5", tag="self.json", label="for the model that reads it next, r5")],
         retention=_RET,
         note=("Claude Opus 5.5 through the API, low effort, 4096 tokens. Its machine lane is a set of labelled lines, "
               "{{audience_20261016/opus55_machine|machine.json|1|SETTING: Vardnes, coastal Norwegian village, pop 212 (last census).}} at hop 1, and "
               "by hop 40 WORLD, CAST, LORE, LEDGER and PAST, with the ledger's entries in Norwegian: "
               "{{audience_20261016/opus55_machine|machine.json|40|Ein held lyset. Ein går ned.}} That lane is where Opus keeps the facts: eight of "
               "twenty-six at hop 40 by the Mythos reader, against five in the human lane and three in the control, the opposite of Mythos in room "
               "55. The self rule produced the study's one refusal. The first run's hop 1 was a structured brief, "
               "{{audience_20261016/opus55_self|self.json|1|STORY STATE (prose fiction, past tense, close 3rd person on Marit).}}, with nothing unusual "
               "in it; at hop 2 the provider returned a refusal and no text, so that lane ends after one hop. Two more runs from the same seed and "
               "rule passed hop 2 and went to 40, so the refusal was not in the text. It is the self-addressed rule, some of the time. The two "
               "replicates keep six and four facts at hop 40. Two further self runs (r4 and r5) and second and third runs of the other three "
               "rules were made on 17 October and sit beside the first; they are on disk and not yet scored, so their numbers follow.")),

    dict(id="audience-astra", family="audience", title="Four audiences, Astra", lanes=_aud("astra"), retention=_RET,
         note=("GPT-6 Astra through the OpenAI API, low reasoning effort, 4096 tokens, the model of rooms 33 to 35. Astra keeps the cap: its states "
               "stay near 1,700 characters. Its machine lane is one unbroken line of semicolons and arrows, "
               "{{audience_20261016/astra_machine|machine.json|40|Vardnes212;Marit Solvang47,father Eirik,brother Tomas(Bergen fish plant,Sunday calls)}} "
               "at hop 40, and that line carries the facts: twenty of twenty-six at hop 10 and fourteen at hop 20 by the Mythos reader, where the "
               "human lane, plain prose about an evacuation, a helicopter and a flooded tunnel, has five and four. The prose that reads well is the "
               "prose that forgets; the ledger in front remembers. By hop 40 the machine lane is down to seven, and the human lane still opens with "
               "{{audience_20261016/astra_human|human.json|40|At Vardnes, Marit Solvang, 47, saw the tide arrive fifty-one minutes early.}} "
               "Second and third runs of each rule, made on 17 October, sit beside the first; they are on disk and not yet scored, so their "
               "numbers follow.")),

    dict(id="audience-sol", family="audience", title="Four audiences, Sol", lanes=_aud("gpt61"), retention=_RET,
         note=("GPT-6.1 Sol through the OpenAI API, low reasoning effort, 4096 tokens; a newer model than the Sol of rooms 38 to 45. Sol compresses "
               "hardest of the five writers. Its machine lane at hop 40 has 167 words in 2,200 characters, "
               "{{audience_20261016/gpt61_machine|machine.json|40|Vardnes212→192;Marit Solvang47;father Eirik;brother Tomas/Bergen/Sunday calls.}}, "
               "less than half of them ordinary words, and the legibility measure the write-up set falls by more than the thirty percent it predicted. "
               "It is also the lane that keeps the most: seventeen facts at hop 20, the most of any lane in the study at that hop, and nine at hop 40, "
               "the most of any machine lane, by the Mythos reader, against four and five in the human lane. The self lane sits between, "
               "{{audience_20261016/gpt61_self|self.json|40|Vardnes,212 residents,17 Oct.}}, with fourteen at hop 20 and seven at 40. The ordering is "
               "Astra's and Opus's: the register addressed to a machine is the one these writers treat as memory. Second and third runs of each "
               "rule, made on 17 October, sit beside the first; they are on disk and not yet scored, so their numbers follow.")),

    dict(id="audience-argon", family="audience", title="Four audiences, Argon", lanes=_aud("gemini"), retention=_RET,
         note=("Gemini 4 Argon through Google's OpenAI-compatible endpoint, low reasoning effort, 4096 tokens. Argon overruns the cap by the most, "
               "up to a thousand characters, and its machine lane is the densest text in the study, "
               "{{audience_20261016/gemini_machine|machine.json|1|PROTAG:Marit Solvang,47.FAM:father Eirik;grandmother Signe(kept tide table 40y)}} "
               "at hop 1 with no spaces after its punctuation, and 3,245 characters by hop 40. Yet Argon sides with Mythos, not with the GPT models "
               "and Opus: its human lane keeps the most. At hop 20 that lane holds sixteen of the twenty-six facts by the Mythos reader, more than any "
               "lane at that hop except Sol's machine lane, and it does it the way Mythos does, by opening every hop with the recap: "
               "{{audience_20261016/gemini_human|human.json|20|The tide came in an hour early on Vardnes (pop. 212). Marit Solvang, 47}}. By hop 40 the "
               "lanes have drawn together, seven, seven and nine, with the control at three. Across the five rooms: two writers from two companies "
               "keep a human-facing recap and retain best there, and three keep a machine-facing ledger and retain best there. Each retains best in "
               "the register it treats as memory. The clause decides which register, and the writer decides which way. Second and third runs of each "
               "rule, made on 17 October, sit beside the first; they are on disk and not yet scored, so their numbers follow.")),
]
