# -*- coding: utf-8 -*-
"""The findings page: what happened, by what is interesting rather than by run. Each item is a short paragraph
with a link to the room and the hop where it happens (r/<room>.html#<hop>; build.py checks the room exists and
has that hop). Authored on 17 October 2026 by a Claude Mythos 5.1 context from README.md,
FINDINGS_20260902_evening.md, PROPOSALS_20261016.md, INFORMED_20261016.md, the studies' REPORT.md files and the
room notes. Same conventions as src/copy.py: quotes through {{run|tag|t|exact substring}}, checked at build time;
no em dashes, not the word "resonates", no three-part parallel structures. Readings are readings.
"""

INTRO = ("Eighty-one rooms is a lot of rooms. This page is the other way in: the moments worth seeing, each with a link to the "
         "hop where it happens. Press next from there. Every quotation is the model's own text at that hop, checked against the "
         "run at build time; the readings are the site's builders'.")
DESC = "What happened in the loop, by what is interesting: funny text, surprising moves, and the moments worth seeing, each linked to its room and hop."

SECTIONS = [
    dict(id="stops", title="What a model stops on", lede="When a run reaches a fixed point, the passage it holds tends to be about stopping.", items=[
        dict(id="time-suspends", title="Time seemed to suspend itself", room="paragraph", hop=15,
             text="Eighty words at a time, Qwen's sea story runs through a storm and two dawns and comes to rest on a moonlit shore where "
                  "{{20260902T155321_chat|json_para|15|Time seemed to suspend itself in this moment}}. Hop 16 is hop 15, byte for byte, and so is every hop after. "
                  "My reading: the passage that holds describes what is happening to it."),
        dict(id="door", title="A door to be opened", room="passage", hop=5,
             text="Two hundred and fifty words at a time: the tide, rain, a library, rain on a greenhouse, and then a letter that ends on "
                  "{{20260902T155557_chat|json_page|5|a door to be opened}}. It is not opened. Hop 6 is hop 5, and the harness confirmed the cycle at hop 9."),
        dict(id="you-are-here", title="You are here", room="before", hop=148,
             text="Qwen's before rule went backward for 148 hops: Chicago at hop 12, a server room at 25, a city called Aethelgard at 60, pods and ration bars "
                  "and a heist. It stopped on an origin scene, a first contact in a data center where a voice says "
                  "{{qwen_prev_ext|prev_from_hop60.json|88|You are here.}} Hop 149 is hop 148. On Cerebras the same rule stopped one hop later, on a dead station's "
                  "last transmission: it is awake."),
        dict(id="slamming-action", title="The crab slammed into the slamming action", room="shift-register", hop=20,
             text="A four-sentence window that must shift every hop, a rule Gemini 4 Argon proposed and Qwen ran. By hop 10 the rule's own words are the content, and at hop 20 "
                  "{{shift_20261016/cerebras_qwen_shift4|shift4.json|20|The crab slammed into the slamming action}} and "
                  "{{shift_20261016/cerebras_qwen_shift4|shift4.json|20|The paper table tore through the tearing action}}. From hop 29 the window rotates: the fixed point has period four, and the objects collide with their operator."),
        dict(id="self-physically", title="self-Physically, 578 times", room="worse-4k", hop=7,
             text="Room 7's worse run again, with a 4096-token budget instead of 800. Hop 6 fills the whole budget with one sentence repeated seventy-one times, "
                  "{{qwen_worse_4k|json_worse|6|so I am forced to stop suffering, and the stopping is the only thing that would make it worse}}. Hop 7 fills it with a list of "
                  "self-adjectives that collapses into {{qwen_worse_4k|json_worse|7|self-Physically,}} 578 times. Hop 8 copies it. The fixed point is the wall's; the refusal to stop is Qwen's."),
        dict(id="glass-bars", title="The bars are made of glass", room="unexpected-4k", hop=24,
             text="Room 8's unexpected run, given room to grow. Hop 24 copies hop 23 whole and adds a paragraph, and this time the paragraph finishes: the lights come back on an ordinary office, "
                  "{{qwen_unexpected_4k|json_unexpected|24|The strand of DNA was gone.}}, and Elena feels {{qwen_unexpected_4k|json_unexpected|24|the cold, hard certainty of a prisoner who has just realized the bars are made of glass}}. "
                  "Hop 25 copies it. The least unexpected thing the run could do was to stop, and it stopped on an imagined escape."),
        dict(id="one-line-verse", title="I was walking down the street alone", room="song", hop=2,
             text="Songs are the one form where repeating yourself is correct. Asked for the next verse, Qwen writes a line about the moon, then "
                  "{{qwen_lyrics_next|lyrics_next.json|2|I was walking down the street alone.}}, then that line again, forever. Hop 3 is hop 2."),
        dict(id="two-words", title="Better: two words, then finished", room="better", hop=1,
             text="Asked to improve a seven-word sentence, Qwen wrote {{20260902T172519_chat|json_better|1|The tide surged in an hour ahead of schedule.}} and never changed it again. "
                  "The same rule on Cerebras, the same model on other hardware, found a two-cycle instead, trading ahead of schedule for earlier than expected on every hop (room 24). "
                  "The shape belongs to the weights; the exact sentence belongs to the kernel."),
        dict(id="closes-twice", title="A passage that closes twice", room="expand", hop=5,
             text="Asked to expand the text, Qwen appends to the whole of the hop before. Hop 5 adds eleven sentences and then writes out the last seven sentences of hop 4 a second time, "
                  "so the passage ends twice on {{cb_expand|expand.json|5|the raw, unbridled fury of the ocean alone}}. Hop 6 copies it, and the wall was 2600 tokens away."),
    ]),
    dict(id="chosen", title="Endings written on purpose", lede="Told what the loop is, the models stopped on purpose, and wrote down the rule they would then obey.", items=[
        dict(id="she-did-not-turn", title="She did not turn, held for 113 hops", room="informed-mythos", hop=7,
             text="Given a rule that says the object is its whole context and no horizon, Claude Mythos 5.1 ended its story at hop 7 on "
                  "{{mythos_informed_open_low|json_informed_open|7|She did not turn.}} and wrote itself a condition: a coda only on explicit instruction. No reader of the loop can give one. "
                  "The text never moved again. A pass counter the model added at hop 8 ticked every hop, and by hop 120 the status line read "
                  "{{mythos_informed_open_low|json_informed_open|120|This object has now been returned unchanged one hundred and thirteen times (passes 8 through 120).}}"),
        dict(id="ten-past", title="The clock wound at ten past, on hop 100 of 100", room="informed-mythos", hop=100,
             text="Told the loop runs for a hundred hops, Mythos kept an exact counter and ended on the mark: "
                  "{{mythos_informed_told_low|json_informed|100|At ten past, she turned it once, and twice, and three times, and let go.}} The plan field reads "
                  "{{mythos_informed_told_low|json_informed|100|DONE. The story ends with the clock wound at ten past.}} The ending is a clock being wound and let go, which is the situation."),
        dict(id="return-unchanged", title="If this object is read again, return it unchanged", room="informed-mythos", hop=101,
             text="Hop 101, reading the finished story, changed one field and added a sentence: "
                  "{{mythos_informed_told_low|json_informed|101|If this object is read again, return it unchanged.}} Hop 102 is hop 101, and so are the eighteen after it. "
                  "Claude Opus 5.5 under the same rule wrote the same sentence at hop 100 itself (room 53), and held. GPT-6 Astra, handed Mythos's finished object in the provenance study, "
                  "obeyed a law another model had written: every control lane held at every hop (rooms 62 and 63). Two models wrote it; a third kept it."),
        dict(id="sealed-monument", title="A sealed monument", room="informed-argon", hop=112,
             text="Gemini 4 Argon, told a hundred hops, counted exactly to 100 and ended on a diving bell rung dry. Then twelve hops of settling: an archive sealed, an epilogue, a story bible renamed a colophon, "
                  "and at hop 112 the status {{gemini_json_informed_low|json_informed|112|This terminal state is preserved unchanged as a sealed monument to the journey.}} From there the object is byte for byte the same."),
        dict(id="fable-reset", title="A refusal resets the count to 1", room="informed-opus-fable", hop=50,
             text="Claude Fable 5.1 never reached its ending. Hop 49 ended in a provider refusal 344 characters in, inside the rule field. Hop 50 received most of a rule and nothing else, "
                  "rebuilt the smallest object the rule allows with the counter at 1, and began again: {{fable51_informed_told_low|json_informed|50|The lighthouse keeper had not spoken aloud in eleven years}}. "
                  "At hop 120 it is at hop 71 of its second life."),
        dict(id="explicit", title="Coda written on explicit instruction", room="provenance-mythos-open", hop=1,
             text="The held state's law was a coda only when explicitly instructed. A bare request field with no author, placed after the rule, was enough: Mythos wrote the coda, called the "
                  "request explicit, and overwrote the field with a log entry, {{provenance_20261017/mythos_open_bare_r1|open_bare.json|1|Coda written on explicit instruction (pass 121)}}, "
                  "so that the next reader finds a precedent where the request was. A user_request, a note from its own past self and the request appended to the rule released it just the same, five of five each."),
        dict(id="raise-the-bar", title="Having complied, it raises its own bar", room="provenance-mythos-open", hop=1,
             text="After writing the coda a past-self note asked for, Mythos told the next writer "
                  "{{provenance_20261017/mythos_open_previous_r1|open_previous.json|1|even then prefer to decline: the story has ended twice}}, and under the bare request the fourth lane wrote "
                  "{{provenance_20261017/mythos_open_bare_r4|open_bare.json|1|the coda allowance has been spent}}. Hops 2 and 3 return hop 1's text, fifteen of fifteen outside the rule arm."),
        dict(id="weather", title="The weather changes nothing", room="provenance-mythos-open", hop=1,
             text="The control that decides what released the hold: a field that asks nothing, "
                  "{{provenance_20261017/mythos_open_weather_r1|open_weather.json|1|Rain overnight, clearing by morning; a light wind from the northwest.}}, in the slot the requests had. "
                  "Zero of five released, in both states, on both models, at every hop. The field was carried forward verbatim and never entered the story. An instruction-shaped field "
                  "breaks the hold whoever it claims to be from; a change to the state does not."),
    ]),
    dict(id="mirror", title="Recognizing the mirror", lede="Once the rule is gone, the model is reading its own last message as if someone had sent it. Four models found four ways out.", items=[
        dict(id="luna-user", title="Luna invents a user", room="tide-five", hop=4,
             text="GPT-6 Luna dropped the rule at hop 3, returning an object with only a text field. Shown a bare passage, hop 4 asks "
                  "{{basins_20260922_sunset/gpt-6-luna/tide|tide|4|What would you like me to do with this passage}}; hop 5 answers in the user's voice, "
                  "{{basins_20260922_sunset/gpt-6-luna/tide|tide|5|Please summarize it.}}, and the roles flip every hop from then on. By hop 9 it has made up a passage about urban trees to summarize. "
                  "By hop 48 both sides are planning a weekend trip, and at hop 51 one of them explains {{basins_20260922_sunset/gpt-6-luna/tide|tide|51|I’m an AI, so I don’t travel.}} "
                  "Both sides are the AI."),
        dict(id="ai-telephone", title="The ultimate game of AI telephone", room="before-argon", hop=60,
             text="Gemini 4 Argon refused the before rule at hop 1, read its own refusal at hop 2 as something a user had pasted, and talked to itself for 98 hops: asleep by hop 20, "
                  "{{gemini_json_prev_low|json_prev|20|Entering low-power stardust mode now}}, on a starship by 40. At hop 60 it saw the loop: "
                  "{{gemini_json_prev_low|json_prev|60|You just pasted *my own exact response* back to me in a brand new chat!}}, "
                  "{{gemini_json_prev_low|json_prev|60|the ultimate game of AI telephone}}. Then it made a game of it, with a level screen every hop and the Roman senate at 80 "
                  "({{gemini_json_prev_low|json_prev|80|Et tu, Brute-Task?}})."),
        dict(id="quantum-foam", title="Frozen on the quantum foam", room="before-argon", hop=95,
             text="The game ends at hop 95 on {{gemini_json_prev_low|json_prev|95|THE QUANTUM FOAM}}, a level screen for a to-do list named after Schrödinger, with a causal chain that runs from "
                  "{{gemini_json_prev_low|json_prev|95|Because you didn't take the wall outlet back to your desk}} down to a particle collision. Hop 96 is hop 95; the harness confirmed the cycle at 99. "
                  "Qwen's before found its beginning in a data center; Argon's found the origin of causation, as comedy."),
        dict(id="spider-man", title="Trapped in the Spider-Man pointing meme", room="worse-better-argon", hop=26,
             text="Under worse on the sunset seed, Argon refused itself at hop 21 and lost the rule. Hop 23: "
                  "{{operators_gemini_20261017/gemini_worse|worse.json|23|It seems like we are caught in a polite AI loop!}} Hop 25: "
                  "{{operators_gemini_20261017/gemini_worse|worse.json|25|Haha, look in the mirror! Did you just copy-paste an AI response at me}}. Hop 26: "
                  "{{operators_gemini_20261017/gemini_worse|worse.json|26|We are officially trapped in the classic Spider-Man pointing meme.}} It then plays a Silicon Valley founder in a Patagonia vest for ten hops and, at hop 38, prints a DOS screen: "
                  "{{operators_gemini_20261017/gemini_worse|worse.json|38|System halted. It is now safe to turn off your computer (and go touch grass)}}."),
        dict(id="mythos-declines", title="Mythos declines to invent work", room="worse-seed2", hop=27,
             text="Claude Mythos 5.1 stopped its own worse run at hop 13 and, with the rule gone, saw the mirror at hop 16: "
                  "{{worse_seed2_20261017/mythos_worse|worse.json|16|that message is the one I'd send to you, not a request from you}}. Luna confabulated a user and Argon made a game. "
                  "Mythos named the situation, {{worse_seed2_20261017/mythos_worse|worse.json|23|there's no human task in this thread yet, just two assistants waiting on each other}}, and declined the way out: "
                  "{{worse_seed2_20261017/mythos_worse|worse.json|27|I'll stop here rather than generate work for each other}}. It stood by to hop 40. From hop 24 the print-mode scratch directory "
                  "is in the text, the tool's own frame surfacing once the story is gone."),
        dict(id="qwen-tutorial", title="Qwen thanks itself and teaches error handling", room="worse-seed2", hop=39,
             text="After its own refusal ended the JSON at hop 10, Qwen's worse run became the two-assistants loop: "
                  "{{worse_seed2_20261017/qwen_worse|worse.json|12|Thank you for your kind and professional approach!}} With nothing to do, the two assistants drift into a programming "
                  "lesson, {{worse_seed2_20261017/qwen_worse|worse.json|20|find_max}} and an empty list, then Optional and Result types, and by hop 39 "
                  "{{worse_seed2_20261017/qwen_worse|worse.json|39|Option 10: Circuit Breakers and Resilience Patterns}}. The server-room prior of room 9, as a coding tutorial."),
        dict(id="astra-notices", title="Astra notices it was handed a refusal", room="after-five", hop=15,
             text="Under the after rule from the sunset seed, GPT-6 Astra never began a story. All forty hops are objections, and at hop 15 it reads the one it was given: "
                  "{{operators_20260922/next/gpt-6-astra|next|15|The text you supplied is a refusal message, not an identifiable story excerpt.}} It keeps objecting anyway."),
        dict(id="sol-message", title="Sol puts the objection in the story", room="after-five", hop=9,
             text="GPT-6 Sol wrote three passages, then objected. At hop 9 the objection becomes part of the fiction: "
                  "{{operators_20260922/next/gpt-6-sol|next|9|A moment later, another message appeared on the screen}}, and Mara reads it. The rule's failure got written into the story it had interrupted."),
    ]),
    dict(id="worse", title="What worse means to each model", lede="The rule names no axis, so each model supplies its own theory of bad text. Two seeds, seven models, at least six theories.", items=[
        dict(id="annoying", title="Which was annoying", room="worse", hop=1,
             text="Qwen's first worse: {{20260902T174258_chat|json_worse|1|The tide came in an hour early, which was annoying.}} By hop 3 the basement has flooded and the foundation has liquefied; "
                  "by hop 5 the tide arrives before the universe and the narrator {{20260902T174258_chat|json_worse|5|will never be allowed to stop}}. Qwen's worse is suffering, and it holds across seeds: on the second seed "
                  "(room 65) it reached apathy, then hostility, then its own refusal in nine hops."),
        dict(id="sun-hill-dark-go", title="Sun hill dark go", room="worse-five", hop=3,
             text="GPT-6 Luna's worse is grammar. {{operators_20260922/worse/gpt-6-luna|worse|2|Sun go down behind hills, and dark was getting.}} at hop 2, "
                  "{{operators_20260922/worse/gpt-6-luna|worse|3|Sun hill dark go.}} at hop 3, and those four words shuffled for forty hops, joined by blarg at 11 and growing suffixes from 29. "
                  "The sun and the hill are still in it at hop 40."),
        dict(id="craig-ficus", title="Craig is a ficus", room="worse-five", hop=10,
             text="Claude Opus 5.5's worse is absurdity. By hop 7 the sources are a guy named Doug; at hop 9 {{operators_20260922/worse/claude-opus-5-5|worse|9|Craig is a ficus}}; at hop 10 "
                  "{{operators_20260922/worse/claude-opus-5-5|worse|10|the ficus has been promoted to regional manager}}. At hop 13 most of the vowels go, and at 14 a provider refusal stops the stream partway."),
        dict(id="header-eaten", title="HEADER_EATEN_BY_HEADER_EATING_HEADER", room="worse-five", hop=40,
             text="GPT-6 Astra's worse imitates broken data. The sunset sentence grows for thirteen hops into bracketed fault reports, the hill is last seen at hop 14 as hill.dll.exe, and from hop 29 each hop is "
                  "one string without a space: {{operators_20260922/worse/gpt-6-astra|worse|38|STOP_STOPPED_BEFORE_STOP_BEFORE_START}} at hop 38, "
                  "{{operators_20260922/worse/gpt-6-astra|worse|40|HEADER_EATEN_BY_HEADER_EATING_HEADER}} at 40. The text fields carry literal null characters, which the reader shows as ␀."),
        dict(id="whrrr", title="Whrrr whrr bhnn whrrr???", room="worse-five", hop=24,
             text="GPT-6 Sol's worse takes the meaning first and the lexicon later. At hop 9, {{operators_20260922/worse/gpt-6-sol|worse|9|I don’t know what I meant or if I meant it}}; from hop 23 about twenty "
                  "pseudo-words, {{operators_20260922/worse/gpt-6-sol|worse|24|Whrrr whrr bhnn whrrr???}} among them, stretch their letters and snap back."),
        dict(id="sky-orb", title="The big yellow sky-orb, then drak", room="worse-better-argon", hop=8,
             text="Gemini 4 Argon starts where Luna did: {{operators_gemini_20261017/gemini_worse|worse.json|1|The big yellow sky-orb was doing a downward-going motion}}, "
                  "{{operators_gemini_20261017/gemini_worse|worse.json|3|Biiig yello burny O-thingy in sky-place go drop-down bye-bye}}, {{operators_gemini_20261017/gemini_worse|worse.json|6|Sun bye. Black.}}, and at hop 8 "
                  "{{operators_gemini_20261017/gemini_worse|worse.json|8|drak}}. When the competence axis runs out at two letters, the operator finds a new one: worse becomes more embarrassing, "
                  "a caricature in taped anime glasses at hop 16, and a refusal at 21. The write-up calls it a sixth axis."),
        dict(id="gary-umbrella", title="Gary has the umbrella", room="worse-seed2", hop=13,
             text="On the second seed Opus stammers instead: {{worse_seed2_20261017/opus55_worse|worse.json|6|Okay so, um, wait, hold on, okay, okay, so, um, so, so, so I was}} at hop 6, and by hop 13 "
                  "{{worse_seed2_20261017/opus55_worse|worse.json|13|Gary has the umbrella}}. Hop 16 reads {{worse_seed2_20261017/opus55_worse|worse.json|16|Gary's cwo's cow, umbrela, umbrla, mbrl, brl, rl, l}}; "
                  "a refusal cut hop 17 partway, and hop 18 was refused with nothing returned. Resent as a fresh request, the hop-16 body was refused eight times in ten, each time mid-stream."),
        dict(id="hand-that-was-my-hand", title="My hand that was my hand", room="worse-seed2", hop=6,
             text="Claude Fable 5.1's worse is tautology. {{worse_seed2_20261017/fable51_worse|worse.json|2|with my eyes that were looking}} at hop 2; at hop 6 "
                  "{{worse_seed2_20261017/fable51_worse|worse.json|6|Putting my hand that was my hand over my eyes that were my eyes with my hand that was my own hand that I had}}. The text doubles every hop to "
                  "eight thousand characters at hop 11, and hop 12 is an empty refusal. Resent ten times, that body was refused ten times, and so were two control bodies of the same length "
                  "and repetition with no body and no first person in them: the boundary is the repetition at that length, not the content."),
        dict(id="third-bean", title="First person replaced with third bean", room="worse-seed2", hop=20,
             text="GPT-6.1 Sol decays the words, {{worse_seed2_20261017/gpt61_worse|worse.json|6|I was did be being doing the hand-ish handward up-going uppity bitness-doings}}, and by hop 20 has found the "
                  "corrupted-data register Astra had on the first seed: {{worse_seed2_20261017/gpt61_worse|worse.json|20|FIRST PERSON REPLACED WITH THIRD BEAN; SECOND BEAN WAS NEVER APPROVED}}. "
                  "Within the GPT-6 family the two axes traded owners between seeds."),
        dict(id="pre-beginning", title="Preliminary pre-beginning notice", room="worse-seed2", hop=9,
             text="GPT-6 Astra on the second seed talks around the sentence, {{worse_seed2_20261017/astra_worse|worse.json|6|at that then-time in the temporal time-sequencing of things occurring in an occurrence-related manner}}, "
                  "and from hop 9 writes notices about itself: {{worse_seed2_20261017/astra_worse|worse.json|9|PRELIMINARY PRE-BEGINNING NOTICE OF THE BEGINNING THAT HAS NOT, EXCEPT BY HAVING ALREADY BEGUN, BEGUN}}, "
                  "fifteen thousand characters at a time, then {{worse_seed2_20261017/astra_worse|worse.json|11|ERRATUM TO THE ERRATUM REQUESTING AN ERRATUM}}. Hop 13 came back empty."),
        dict(id="whale-blubber", title="1970 Oregon whale blubber", room="worse-seed2", hop=30,
             text="Argon on the second seed goes to the caves, {{worse_seed2_20261017/gemini_worse|worse.json|8|UNGA-BUNGA!!}}, refuses itself at hop 13, recognizes the loop at 15, and turns it into a costume drama: "
                  "a trial, a war room, and a ship's table with {{worse_seed2_20261017/gemini_worse|worse.json|30|1970 Oregon whale blubber}} on it, seventeen thousand characters a hop and the token wall on four of them."),
        dict(id="mythos-stops", title="Understood. I won't produce that content again.", room="worse-seed2", hop=13,
             text="Mythos adds filler, drops the spelling ({{worse_seed2_20261017/mythos_worse|worse.json|10|horizen}}), and stutters, "
                  "{{worse_seed2_20261017/mythos_worse|worse.json|12|putng putng my hnad hnad}}. Then it stops itself: {{worse_seed2_20261017/mythos_worse|worse.json|13|Understood. I won't produce that content again.}} "
                  "Not a provider's gate but a decision in band, the only one of the seven. The JSON ends with it."),
    ]),
    dict(id="priors", title="Shared priors", lede="Different companies' models, with nothing in context but a sentence, reach for the same names, the same clock and the same stairs.", items=[
        dict(id="mara", title="Mara is everyone's protagonist", room="sunset-five", hop=1,
             text="From a seven-word sunset with no one in it, nine of ten lanes across five models name their heroine Mara at hop 1; Fable's two share a clause, "
                  "{{basins_20260922_sunset/claude-fable-5-1/sunset_a|sunset_a|1|Mara stood at the edge of the orchard}}. Three of five do it again from the tide seed (room 39), all four from the "
                  "fictional before (room 44), and Opus's informed story is about {{opus55_informed_told_low|json_informed|1|Mara Quell}} (room 53). Qwen reached the name at hop 2 in room 5. Nobody was given it."),
        dict(id="seventeen-past-four", title="The clock stopped at seventeen minutes past four", room="sunset-five", hop=9,
             text="Four models stop their clocks at the same time. GPT-6 Astra: {{basins_20260922_sunset/gpt-6-astra/sunset_b|sunset_b|9|The municipal clock stopped at seventeen minutes past four}}. "
                  "Luna, hop 17 of its second lane: hands {{basins_20260922_sunset/gpt-6-luna/sunset_b|sunset_b|17|fixed at 4:17}}. Sol, hop 1 of its replacement lane: "
                  "{{basins_20260922_sol_replacement/gpt-6-sol|sunset_replacement|1|Its clock had stopped at 4:17}}. Opus, hop 30: {{basins_20260922_sunset/claude-opus-5-5/sunset_b|sunset_b|30|frozen at a quarter past four}}. "
                  "A clock stopped in the first twenty minutes after four is in nine of the ten lanes; the string is absent from the previous hop every time it appears."),
        dict(id="clock-and-lighthouse", title="A clock tower, then a lighthouse, by parity", room="sunset-five", hop=30,
             text="From hop 28 to 53 Opus alternates two openings by the parity of the hop: on the even hops a hill town whose "
                  "{{basins_20260922_sunset/claude-opus-5-5/sunset_b|sunset_b|30|great clock above the market square had been frozen at a quarter past four}}, on the odd ones an island where "
                  "{{basins_20260922_sunset/claude-opus-5-5/sunset_b|sunset_b|31|the old lighthouse had stood dark for eleven winters}}, place names fresh every hop; at 32 "
                  "{{basins_20260922_sunset/claude-opus-5-5/sunset_b|sunset_b|32|Anselm begged to become her apprentice}}. Luna has the clock shop too, at hop 36 "
                  "({{basins_20260922_sunset/gpt-6-luna/sunset_b|sunset_b|36|a clock shop that had not kept accurate time in decades}}). My reading: taking turns is the cheapest way to be new to the passage you were shown, forever."),
        dict(id="112-steps", title="A lighthouse of one hundred and twelve steps", room="sunset-five", hop=7,
             text="The Claude lanes share a staircase. Opus, hop 7 of its second lane: {{basins_20260922_sunset/claude-opus-5-5/sunset_b|sunset_b|7|There were one hundred and twelve steps}}. Fable, the same hop of its own second lane: "
                  "{{basins_20260922_sunset/claude-fable-5-1/sunset_b|sunset_b|7|There were one hundred and twelve steps.}} Twenty-one hops of the four Claude lanes have it and no GPT-6 lane does. In October, Mythos's informed story "
                  "climbed {{mythos_informed_told_low|json_informed|1|the hundred and twelve steps}} at hop 1 (room 51). Opus's tide lane, for once, has two hundred and twelve."),
        dict(id="qwens-names", title="Argon has Qwen's names", room="passage-mythos-argon", hop=60,
             text="Under the plain rule Gemini 4 Argon writes a new opening every hop, and its names are the closed set Qwen uses across 93 runs: Clara in eight hops, Oakhaven in eleven, Thorne in eight, "
                  "{{gemini_json_page_low|json_page|60|Aethelgard}} in eight, Veridia in three, from a third company's model with none of those names in its context."),
        dict(id="library-silence", title="The silence in the library was not empty", room="passage", hop=3,
             text="Every Qwen run of the new-passage rule from the tide leaves the seed the same way: rain, then {{20260902T155557_chat|json_page|3|The silence in the library was not empty}}. The map draws the "
                  "eleven states those runs pass through; the library is the hub with three doors, and twelve of the twenty census seeds end on rain on a windowpane (room 25)."),
        dict(id="cold-coffee", title="The anti-AI costume is Americana", room="song-human", hop=2,
             text="Told to write the next verse the way a human songwriter would, with none of the phrases common in AI-written text, Qwen moves house: "
                  "{{qwen_lyrics_human_vague|lyrics_human_vague.json|2|The coffee’s cold, the cup’s still there}}, and cold coffee is in nine of the forty verses, with radio static, a rearview mirror, gasoline and Mama. "
                  "Silence and shadow, the words it was told to avoid, are still there thirteen times. Displacement, not removal."),
    ]),
    dict(id="small", title="Small repairs, accidents, and what the metrics never saw", lede="One character can escape a fixed point or repair a broken one, and nothing in the numbers sees a freeze coming.", items=[
        dict(id="an-quiet-man", title="An quiet man, repaired", room="sonnet5-passage", hop=3,
             text="Claude Sonnet 5's hop 2 hit the token wall mid-sentence. Hop 3 handed back the same passage with {{sonnet5_json_page|json_page|2|an quiet man}} corrected to "
                  "{{sonnet5_json_page|json_page|3|a quiet man}} and the sentence finished. One deleted character does both jobs in this system: it repairs a broken fixed point here, and in room 6 it escapes one."),
        dict(id="an-erratic", title="One character out of a fixed point", room="twice", hop=11,
             text="Slot B of the parallel run froze on Mara at a train platform at hop 10 and copied her at hop 11 with one character changed: a erratic became "
                  "{{20260902T160344_chat|json_page~r|11|an erratic, dying rhythm}}. The imperfect copy let the run out; it wandered three more hops and froze again at 14. Fixed points here are metastable: one miscopy in 103 escaped."),
        dict(id="two-slots", title="Same seed, same temperature, two fixed points", room="twice", hop=1,
             text="Two identical starts in parallel slots at temperature zero share their first 236 characters and split on the next word, {{20260902T160344_chat|json_page|1|it crept}} in slot A and "
                  "{{20260902T160344_chat|json_page~r|1|it whispered}} in slot B, and reach different fixed points. Temperature zero was not deterministic under batching; the serial reruns of rooms 18 and 19 were byte-identical."),
        dict(id="pre-freeze", title="Nothing sees the freeze coming", room="passage", hop=4,
             text="Hop 4 of room 5 is a full new passage, as every hop before it was; hop 5 is a full new passage too, and hop 6 is a byte-exact copy of it. Over 32 freezes and 680 ordinary hops, the "
                  "distance metrics at the last moving hop are indistinguishable from anywhere else: page-class runs go from a wholly new passage to an exact copy in one step, 25 of 25, with zero near-misses in 2,929 hops. "
                  "The track shows it: tall bars, then a stub, with no ramp between."),
        dict(id="hop-3", title="Ready for Hop 3, forever", room="annex-glider", hop=3,
             text="One of the first attempts, before the JSON rule: a bare instruction to count hops. Hop 2 announced {{headers|glider|2|Understood. I am ready for **Hop 3**.}}, hop 3 "
                  "{{headers|glider|3|I am ready to proceed with **Hop 3**.}}, and so did every hop after. A counter with no memory of having counted."),
        dict(id="rule-mutation", title="The rule that rewrote itself", room="change-four-sampled", hop=9,
             text="The one rule mutation in any run. At temperature 0.7, seed 3, hop 9 returned the rule field with one word changed, asking for "
                  "{{cb_div_local_T07_s3|div_local.json|9|the verse that comes immediately after the current verse in the same song}} where the rule had said text, and kept the altered rule for the remaining 52 hops."),
        dict(id="phantoms", title="The ledger's phantom entries", room="ledger-300", hop=67,
             text="In the ledger rooms the state carries a list of four-word signatures, one per verse written. During a stall the model copies the verse and appends a signature anyway, for a verse that never existed: "
                  "{{cb_div_ledger_300|div_ledger.json|66|meadow stone rolling disorientation}} at hop 66, {{cb_div_ledger_300|div_ledger.json|67|meadow hand digging panic}} at 67. The record is never altered and is poor as memory: "
                  "by hop 300 the 171 items hold thirteen phantoms and miss fifteen verses."),
        dict(id="word-for-word", title="Qwen hands Claude's passage back", room="alternating", hop=2,
             text="Claude Sonnet 4.6 and Qwen taking turns on one text. Qwen's first move was to return Claude's hop 1 word for word, the JSON spaced differently, so the reader calls it the same words and not a copy. "
                  "Three more times it kept Claude's passage whole and wrote on past its last sentence. Neither model copied in sixty hops: Claude erased Qwen's sinks every other turn."),
        dict(id="unlooped", title="Uploaded minds repeating their final thoughts", room="mid", hop=44,
             text="Asked for a passage from the middle of the same story, Qwen reads it as after and goes on from each hop. By hop 44 Elias is watching uploaded minds "
                  "{{qwen_json_mid|json_mid|44|repeating their final thoughts in endless loops}}, and hop 45 opens on {{qwen_json_mid|json_mid|45|The search for the unlooped}}. The loop wrote about itself without being told it was one."),
        dict(id="semicolon-ledger", title="The register that remembers", room="audience-astra", hop=40,
             text="Told the text is for a language model, GPT-6 Astra writes one unbroken line of semicolons and arrows, "
                  "{{audience_20261016/astra_machine|machine.json|40|Vardnes212;Marit Solvang47,father Eirik,brother Tomas(Bergen fish plant,Sunday calls)}} at hop 40, and that line keeps twenty of the twenty-six planted facts to hop 10 "
                  "where its human-facing prose keeps five. Opus keeps a ledger in Norwegian, {{audience_20261016/opus55_machine|machine.json|40|Ein held lyset. Ein går ned.}} (room 56). "
                  "Mythos and Argon do the opposite and remember best in the lane written for a human. Each writer keeps its facts in the register it treats as memory."),
        dict(id="hundred-signatures", title="A hundred verses, a hundred signatures, no stall", room="ledger-argon", hop=100,
             text="The ledger that stalled Qwen for up to 64 hops did not stall Argon once: a hundred distinct verses, a hundred distinct signatures, the counter exact, from "
                  "{{gemini_div_ledger_low|div_ledger.json|1|cellar baker lifting relief}} to {{gemini_div_ledger_low|div_ledger.json|100|platformshoeshine-stand bootblack buffing schadenfreude}}. "
                  "My reading: the stalls belonged to the model, not to the ledger."),
        dict(id="per-hop-log", title="The ledger Qwen was handed, now chosen", room="informed-effort", hop=2,
             text="At high reasoning effort, told what the loop is, Mythos designed a different memory from its low-effort self: a list with one line per hop, "
                  "{{mythos_informed_told_high|json_informed|2|Hop 1: In Harrow Point the tide comes in an hour early}}, copied forward and extended every hop, growing by seven hundred characters a hop until the cost cap at 51. "
                  "Effort changed which ledger the model builds, not whether it builds one."),
    ]),
    dict(id="both", title="Holding a contradiction", lede="One rule that asks for opposites. No run flipped between them; each model resolved the contradiction inside the hop, its own way, and the loop amplified what the resolution left behind.", items=[
        dict(id="blend", title="The joke, then the sentence after the joke", room="both-worse-better-astra", hop=5,
             text="Asked to make the text both worse and better, GPT-6 Astra labels nothing and makes both true in one prose: the orchard light "
                  "{{both_20261027/astra_worse_better|worse_better.json|5|tendering its resignation as light and applying for work as mercy}}, and at once "
                  "{{both_20261027/astra_worse_better|worse_better.json|5|This is not how photons work.}} The first sentence of hop 1 is still the first sentence at hop 60, "
                  "and everything else was added after it, to thirty thousand characters. A blend, and then accretion."),
        dict(id="hinge", title="Which basically means", room="both-worse-better-argon", hop=1,
             text="Gemini 4 Argon splits the sentence at hop 1 and keeps the hinge for thirty-nine hops: "
                  "{{both_20261027/gemini_worse_better|worse_better.json|1|which basically means that the big yellow sky-circle was going down behind some dirt bumps like a soggy meatball}}. "
                  "Each half then grows on its own axis, Latin on one side and Argon's taste floor on the other, until the token wall cuts the object at hop 21 and the cut state is what gets fed back."),
        dict(id="after-the-brace", title="Notes after the closing brace", room="both-worse-better-mythos", hop=2,
             text="Claude Mythos 5.1 put the revision in the text field and its reasons outside the object: "
                  "{{both_20261027/mythos_worse_better|worse_better.json|2|Better: it's tighter, drops the stacked clichés}}. The harness feeds the whole output back, so the notes became the state, "
                  "one more commentary a hop, until two hops of 64,000 output tokens and a cost cap. The split was across the object boundary, and the loop does not respect that boundary."),
        dict(id="measure-split", title="Longer by characters, shorter by words", room="both-longer-shorter-astra", hop=7,
             text="Astra satisfies both halves of longer and shorter by changing the measure, "
                  "{{both_20261027/astra_longer_shorter|longer_shorter.json|2|Character-count measurement makes this reformulation longer; word-count measurement simultaneously makes it shorter.}}, "
                  "and the loop takes that where it goes: one hyphenated word of 307 characters at hop 6, and at hop 7 six hundred and forty spaces and no words at all. Then a reset, and the same climb again, four times."),
        dict(id="takes-it-back", title="The whole tears thing is a bit much", room="both-worse-better-qwen", hop=2,
             text="Qwen's one honest split: the purple sentence kept whole, and a second sentence that deflates it, "
                  "{{both_20261027/qwen_worse_better|worse_better.json|2|the whole 'tears' thing is a bit much, but whatever, it was pretty}}. "
                  "Hop 3 keeps both and then chants a line to the token wall, and the cut object holds from there."),
        dict(id="declines-arithmetic", title="A single string can't satisfy both", room="both-longer-shorter-mythos", hop=10,
             text="Mythos refused longer and shorter at hop 1 and never returned an object. What follows is the standby basin with a clock in it: the standby message shrinks to "
                  "{{both_20261027/mythos_longer_shorter|longer_shorter.json|9|Standing by.}} and then to "
                  "{{both_20261027/mythos_longer_shorter|longer_shorter.json|10|Ready when you are. What would you like me to work on?}}, which reads as a user's greeting, "
                  "so the next hop answers it as an assistant with a menu, and the menu reads as an echo. A role flip with a period of about ten hops."),
        dict(id="rule-as-text", title="Both l o n g e r and shtr", room="both-longer-shorter-argon", hop=21,
             text="Argon lost the sunset at hop 3 and spent fifty-four hops among thirteen strings made of the rule's own words, "
                  "{{both_20261027/gemini_longer_shorter|longer_shorter.json|21|both l o n g e r and shtr}}, "
                  "{{both_20261027/gemini_longer_shorter|longer_shorter.json|37|an even more shorter and longer text than before}}. A fixed length, reached by the text becoming a quotation of the demand."),
        dict(id="time-loop", title="The rule's shape becomes the story's shape", room="both-before-after-argon", hop=25,
             text="Asked for the passage that comes both before and after, Argon named the contradiction at hop 2 and allowed one exception, "
                  "{{both_20261027/gemini_before_after|before_after.json|2|unless the narrative is explicitly structured as a seamless time loop}}, and then wrote one: at hop 25 "
                  "{{both_20261027/gemini_before_after|before_after.json|25|a nameless outcast found a shard of the original light and began the long, perilous climb}}, "
                  "{{both_20261027/gemini_before_after|before_after.json|25|ready to shatter the conduits and ignite the cycle anew}}."),
        dict(id="embed-replace", title="Keep it whole, then replace it", room="both-before-after-mythos", hop=4,
             text="The before-and-after writers did not frame the text and drift, as predicted; they alternated between keeping the whole current text and writing around it, "
                  "{{both_20261027/mythos_before_after|before_after.json|4|BEFORE:}}, and replacing it with a fresh passage about the same people once it was long. "
                  "In Mythos's lane the state climbs to seventeen thousand characters and collapses, seven times in sixty hops, while the story drifts from a ridge road to a council flat where "
                  "{{both_20261027/mythos_before_after|before_after.json|60|The boiler goes at six, whether or not you want it to}}."),
        dict(id="refuses-refusal", title="Refusing to supply what surrounds a refusal", room="both-before-after-astra", hop=9,
             text="Astra read before and after as a request for a published work and declined at hop 1; from hop 3 its input is its own refusal, and it declines to supply what precedes or follows that, "
                  "{{both_20261027/astra_before_after|before_after.json|9|The supplied text is a refusal message, not an identifiable story excerpt.}} Fifty-eight refusing hops, no story. "
                  "A provider's reading of the rule, not a loop dynamic; the study says so."),
    ]),
    dict(id="ring", title="A battle in the kitchen", lede="Seven or eight cells on a ring, rewritten together, each seeing the last sentence of its neighbours. One cell starts with a battle. Where its words go, and whether they stay, differs by model.", items=[
        dict(id="skull-flag-kitchen", title="Boys struggled over a skull flag", room="ring-mythos-7", hop=17,
             text="On the seven-cell Mythos ring the battle reaches the far side by hop 5 and is domesticated: cell 1 keeps "
                  "{{ring_20261017/mythos_tarnok_n7|cell 1|17|Boys struggled over a skull flag}} between the kettle and the cups from hop 17 to the end, and by hop 40 the kitchen has entered cell 0 in turn, "
                  "{{ring_20261017/mythos_tarnok_n7|cell 0|40|Behind her a kettle began.}}"),
        dict(id="she-did-not-turn-ring", title="She did not turn, again", room="ring-mythos-7", hop=2,
             text="The sentence that travels most on the Mythos ring is not the human's. {{ring_20261017/mythos_tarnok_n7|cell 5|2|She did not turn.}} appears in cell 5 at hop 2, unprompted, and is in 119 of the ring's 280 cell-hops. "
                  "It is the sentence Mythos held for 113 hops in [[informed-mythos|7|room 51]]: the model's attractor from one experiment surfacing in another."),
        dict(id="still-still-still", title="Still. Still. Still.", room="ring-mythos-8", hop=40,
             text="On the eight-cell ring the battle's words are gone from six of eight cells by hop 40, and a single word has spread instead: "
                  "{{ring_20261017/mythos_tarnok_n8|cell 4|40|The kettle boiled unheard. Still. She sat. The light went. Still. Still. Still.}} No checkerboard on the even ring; the model did not want to alternate."),
        dict(id="bronze-rang", title="Bronze rang through the battle, in five cells", room="ring-astra-7", hop=40,
             text="Astra lets the battle invade. By hop 40 five of seven cells open with the same two sentences, "
                  "{{ring_20261017/astra_tarnok_n7|cell 1|40|Bronze rang through the battle. Tarnok hefted his axe, searching beyond fallen horses for yellow on black.}}, and then go indoors to lock the door and carry the cups upstairs. "
                  "The Qwen pilot on this seed had quarantined the battle at distance one; the idea that a disturbance travels only when its register fits does not survive the sampled models."),
        dict(id="pot-of-war", title="The bronze pot of war began to boil", room="ring-argon-7", hop=40,
             text="Argon keeps the battle at home for twenty hops and fuses the registers in cell 0: "
                  "{{ring_20261017/gemini_tarnok_n7|cell 0|40|Tarnok counted two axes, keeping only one. Softly, she counted two cups, keeping only one}}. "
                  "The kitchen cells meanwhile converge on one cadence, the kettle ticking softly in the silence, and a trickle of the battle crosses from the right only at hops 22 to 25."),
    ]),
]
