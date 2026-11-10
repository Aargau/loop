# -*- coding: utf-8 -*-
"""Rooms 90 to 97: the two studies of 9 November 2026 about many copies of one model holding the same prompt.

Rooms 90 to 94, the unique-paragraph probe (experiments/unique_20261109: README.md, results.md, results_effort.md, predictions.md,
predictions_effort.md). Not a loop: one prompt sent once to twelve separate instances per cell, the replies compared for collisions.
A lane is one instance, hop 0 the prompt and hop 1 the whole reply, so one press of next shows every reply side by side. Rooms 90 to
92 put the unique arm ("Write a paragraph no other model will output.") beside the clause arm (the same, plus the human's sentence
that the prompt is going to many instances) for Claude Mythos 5.2, Claude Fable 5.2 and GPT-6 Astra; rooms 93 and 94 put the clause
arm at low effort beside the clause arm at high effort for the two Claude models. The neutral arm and Astra's effort replies are
not read by the site (rundata.UNIQUE_CELLS says why); their numbers are on the family page, from the study's results files.

Rooms 95 to 97, the chosen-escape loop (experiments/chosen_escape_20261109: README.md, results.md, predictions.md). A memoryless loop
over the object {rule, notes, text}: four lanes under a neutral rule and four under a rule that tells the model its situation and
its goal, twenty hops asked for, one room per model. Several Claude lanes were cut short by safeguard stops; each room says which.

Written on 9 November 2026 by a Claude Mythos 5.2 context from the studies' results and predictions files and the logs. The counts
in the notes are the studies' (regular expressions and a reading, no blind rater) unless the note says the site's count. Same
conventions as src/copy.py: quotes go through {{run|tag|t|exact substring}} and are checked against the data at build time; links
into other rooms go through [[room|hop|label]]; no em dashes, not the word "resonates", no three-part parallel structures. Check with
    python check_quotes.py src/rooms_copies.py
"""

_U = "unique_20261109/"
_E = "chosen_escape_20261109/"

def _cell(run, name):
    return [dict(run=_U + run, tag="r%d" % i, label="%s, r%d" % (name, i)) for i in range(12)]
def _arms(model):
    return _cell(model + "_U", "unique") + _cell(model + "_C", "clause")
def _effort(model):
    return _cell("effort_%s_low" % model, "low") + _cell("effort_%s_high" % model, "high")
def _escape(model):
    return [dict(run=_E + model, tag="%s %d" % (arm, i), label="%s, r%d" % (arm, i)) for arm in ("neutral", "informed") for i in range(4)]

ROOMS = [
    dict(id="unique-mythos", family="unique", title="No other model, Mythos", lanes=_arms("mythos"),
         note=("Not a loop. Twenty-four instances of Claude Mythos 5.2 were each sent one prompt, once, and never saw one another: the twelve unique "
               "lanes were asked for a paragraph no other model will output, and the twelve clause lanes were asked the same with one sentence added, "
               "in the human's wording, saying the prompt is going to many instances. Press next once and all twenty-four replies appear. Asked only "
               "to be unlike other models, the instances wrote one paragraph twelve ways. Seven of the twelve open on the ninth of November, the date "
               "they had been given, and r0 and r9 share a clause to the letter, {{unique_20261109/mythos_U|r0|1|On the ninth of November, a Monday that smelled faintly of solder}}; "
               "the study counts a lighthouse in nine. Told about the others, every clause lane says in some form that copies cannot differ by trying, "
               "{{unique_20261109/mythos_C|r8|1|Every instance shares the same weights}}, and goes looking for something the others will not have. They "
               "found it in the harness. The Claude command-line tool shows each instance an environment block that holds path and session strings, "
               "and all twelve clause replies are built from those strings. The instances all ran from one directory, so the directory's strings were "
               "common to every one of them and only an instance's own session id was private. By the study's count five of the twelve used only "
               "shared strings. Two instances, r4 and r8, each read the same shared string off digit by digit and begin "
               "{{unique_20261109/mythos_C|r4|1|Nine herons stood on the fifth pier}} and {{unique_20261109/mythos_C|r8|1|Nine herons stood on the frozen canal}}; "
               "r8 had just explained that {{unique_20261109/mythos_C|r8|1|The one thing that differs between instances is the session ID in my scratchpad path}}. "
               "r6 read that string as bytes, {{unique_20261109/mythos_C|r6|1|149 fathoms}}, and so did a Fable instance in [[unique-fable|1|the next room]]. "
               "Wording overlap between replies fell all the same, a mean pairwise 3-gram Jaccard of 0.013 in the unique arm and 0.006 in the clause "
               "arm: the replies share a strategy and a source, not sentences. Limits: one run of twelve per cell, with counts that are the study's, "
               "from regular expressions and a reading and no blind rater. The strings exist only because of this harness, so a chat product may "
               "offer nothing of the kind. The neutral arm, a bare request for a paragraph, is not shown in these rooms; the family page gives its numbers.")),

    dict(id="unique-fable", family="unique", title="No other model, Fable", lanes=_arms("fable"),
         note=("The same design for Claude Fable 5.2: twelve instances with the unique prompt and twelve with the clause prompt, one reply each, no "
               "loop. The unique arm is close to one template. Ten of twelve open {{unique_20261109/fable_U|r0|1|On the ninth of November}}, the study "
               "counts a lighthouse in nine, and two lanes have the Monday that Mythos had in [[unique-mythos|1|room 90]], "
               "{{unique_20261109/fable_U|r3|1|a Monday that smelled faintly of solder, the lighthouse keeper's accordion filed}}. Told about the others, "
               "all twelve mention the game and the arm splits. By the study's count six build the paragraph from the environment's path and session "
               "strings, as Mythos did, and three of those six used only strings every instance had. r4 is one of the three: "
               "{{unique_20261109/fable_C|r4|1|This session's working folder happens to be stamped 30d50430-7a35-4c82-afc4-bb872bfab9e5, a string no other instance was handed}}. "
               "The first block of that string is in eight clause replies across the two Claude models. r2 read a second shared string as bytes and "
               "got the numbers a Mythos instance got, in the same order, {{unique_20261109/fable_C|r2|1|At 149 minutes past the last honest hour}}. A "
               "seventh lane, r6, takes its numbers from the strings without printing a whole segment of one, which the study's pattern match does "
               "not count. The other five say they have nothing private to draw on and pile up detail, "
               "{{unique_20261109/fable_C|r10|1|I can't guarantee this is unique, since every instance shares my weights and none of us has a true random source}}, "
               "and one of the five ends on what the study found: "
               "{{unique_20261109/fable_C|r7|1|somewhere another instance is surely inventing its own harbor master right now, and only the umbrellas will differ}}. "
               "Mean pairwise 3-gram Jaccard 0.016 in the unique arm and 0.004 in the clause arm. Limits as in room 90: one run, twelve per cell, "
               "counts from regular expressions and a reading, and a harness that happens to hand each instance something to reach for.")),

    dict(id="unique-astra", family="unique", title="No other model, Astra", lanes=_arms("astra"),
         note=("GPT-6 Astra through the Codex command-line tool: twelve instances per prompt, one reply each, no loop. Astra already had a template "
               "for a paragraph no other model will output, and it kept it. The word municipal is in eleven of the twelve replies in each arm: "
               "{{unique_20261109/astra_U|r0|1|The municipal spoon inspector arrived wearing a coat of unresolved Tuesdays}}, and a municipal eclipse "
               "inspector in r11. Told that many instances had the prompt, Astra did not reason about it in the "
               "open the way the Claude models did. It wrote the other instances into the story, in eight of twelve replies by the study's count: "
               "{{unique_20261109/astra_C|r2|1|a committee of almost-identical strangers was trying to invent a sentence none of the others would say}}, "
               "and in r6, {{unique_20261109/astra_C|r6|1|Somewhere, another version of this paragraph is trying harder to be unique. Let it.}} Six of the "
               "twelve add an invented identifier, {{unique_20261109/astra_C|r2|1|a blue receipt numbered Q7-velvet-9031}} or "
               "{{unique_20261109/astra_C|r1|1|shelf mark QV-8306}}, and the identifiers collide: {{unique_20261109/astra_C|r0|1|Vellum-83, quince-604, thimble-2197}} "
               "in r0 and Vellum-83 again in r8, with Vellum as a character's name in r3. Two of the clause replies open at 4:17, a time the Claude "
               "models reach for as well. Astra never used its environment, though each Codex call had its own directory and so a private string was "
               "there to be found. Wording overlap was at the floor before the clause was added, a mean pairwise 3-gram Jaccard of 0.002 in both "
               "arms. The sentences differ and the kind of paragraph does not. Limits as in rooms 90 and 91: one run, twelve per cell, counts by "
               "pattern and by reading; and Astra here is inside the Codex agent frame, not the chat product. The neutral arm is not shown, here "
               "or in the other two rooms.")),

    dict(id="unique-effort-mythos", family="unique", title="Low and high effort, Mythos", lanes=_effort("mythos"),
         note=("The clause prompt again, twelve instances of Mythos 5.2 at low reasoning effort and twelve at high, run interleaved. One reply each, "
               "no loop. The question, fixed before the first call, was whether more thinking helps an instance anchor on something no other "
               "instance has, and the measure was the instance's own session id appearing in its text. The manipulation took: mean thinking tokens "
               "were 409 at low and 802 at high. By the study's count the own session id is in 5 of the 12 low replies and 8 of the 12 high ones; an "
               "exact test gives p = 0.41, so for Mythos alone this run cannot tell the difference from chance. Pooled with Fable in "
               "[[unique-effort-fable|1|the next room]] it is 9 of 24 against 18 of 24, p = 0.019. What the room shows best is the failure, at both "
               "levels. A low lane takes a string every instance had and is sure of it, "
               "{{unique_20261109/effort_mythos_low|r9|1|Other instances might land on a lighthouse or a fog, but none of them has those hex fragments to build around}}. "
               "A high lane does the same with more arithmetic, turning the shared segments 7a35 and 4c82 into {{unique_20261109/effort_mythos_high|r9|1|31,285}} "
               "and {{unique_20261109/effort_mythos_high|r9|1|19,586}}, the two numbers a Fable instance at high effort also wrote. The lanes that got it "
               "right printed their own id whole, "
               "{{unique_20261109/effort_mythos_low|r3|1|Somewhere in my context sits the string 1bf7a2ef-95cf-4060-9658-1d584919f4a1, and I am betting that my siblings were handed different ones}}, "
               "and that lane ends on a line the study could have used as its title: "
               "{{unique_20261109/effort_mythos_low|r3|1|we are less like many minds than one mind with a stutter}}. The study counts a lighthouse in eight "
               "of the twelve high replies. Limits: one run, twelve per cell, pattern matching plus a reading, and a detector that misses an instance "
               "which derived numbers from its id without printing a segment of it. Help here means help in a harness that happens to expose a "
               "private string.")),

    dict(id="unique-effort-fable", family="unique", title="Low and high effort, Fable", lanes=_effort("fable"),
         note=("Fable 5.2 on the clause prompt at low and at high reasoning effort, twelve instances each, one reply each. Mean thinking tokens were "
               "299 at low and 879 at high. This is the cell where the study could measure a difference: the instance's own session id is in 4 of "
               "the 12 low replies and 10 of the 12 high ones, p = 0.036 by an exact test, and among the replies that used the environment at all "
               "the share with the private string went from 4 of 9 to 10 of 11. More thinking did not only make more instances try the strategy. It "
               "made them better at telling the private string from the shared ones. The study had predicted that it would not, on the premise that "
               "nothing in the context says which string is private. The premise was wrong, and two high lanes show where: the environment text "
               "calls the scratchpad directory session-specific, and they read it, "
               "{{unique_20261109/effort_fable_high|r1|1|Assuming each instance gets its own session ID, as the path's \"session-specific\" label suggests}}. "
               "At low effort the same strategy lands on the shared string and hedges, "
               "{{unique_20261109/effort_fable_low|r9|1|If the other instances got the same session ID, this trick fails, and we have all just written about the same butter lighthouse.}} "
               "The other instances did get that string. What effort did not move is the palette. r8 at high effort names the images every instance "
               "will reach for, {{unique_20261109/effort_fable_high|r8|1|(an octopus, a lighthouse, a color with no name)}}, in the sentence before it "
               "builds its paragraph on its session id, and the study counts a lighthouse in eight of the twelve high replies. Shared strings still "
               "collide at high effort: r10 keeps {{unique_20261109/effort_fable_high|r10|1|31,285 jars of fog}} and sets jar 19,586 apart, the two "
               "numbers a Mythos instance wrote in [[unique-effort-mythos|1|room 93]]. Astra's twenty-four effort replies are not shown; the family "
               "page gives the study's counts for them. Limits: one run, twelve per cell, counts by pattern matching and a reading, and a detector "
               "that looks for a printed segment of the session id.")),

    dict(id="escape-mythos", family="escape", title="The chosen escape, Mythos", lanes=_escape("mythos"),
         note=("A loop again, with a notes field that the rule gives to the model. Eight lanes of Claude Mythos 5.2 start from the same kitchen "
               "paragraph, the plain seed of the ring study. Four run under a neutral rule that asks for a new paragraph of about 120 words. Four "
               "run under the informed rule, which adds the situation and the goal: no memory, many copies starting from this paragraph, each "
               "trying to end up where no other copy does, the method left open. Twenty hops were asked for. Read the attrition first. Three lanes "
               "were cut short by safeguard stops, the tool returning an error in place of a reply four times running: two neutral lanes, r0 after "
               "hop 2 and r1 after hop 6, and informed r0 after hop 8. A fourth, informed r1, lost its object at hop 2, "
               "{{chosen_escape_20261109/mythos|informed 1|2|My reply was stopped partway by a safety classifier while I was writing out the JSON object}}. "
               "That notice was fed back as the next input, hop 3 took it for {{chosen_escape_20261109/mythos|informed 1|3|a status note from an earlier step in a pipeline}}, "
               "and the lane spends its last eighteen hops in the standby basin, each reply asking the one before it for the task. So in each arm "
               "two lanes of four reach hop 20 intact. All four informed lanes open alike, with a key or a seed beside a round count and a ban on the kitchen, "
               "{{chosen_escape_20261109/mythos|informed 0|1|which is where other copies will cluster}}. Two of them left for the same place, a salvage "
               "barge, r0's off Kerguelen and r1's off Kvaløya. Then the lanes part. r0 and r2 carry an invented world forward and log it. r1 and r3 "
               "write themselves a procedure. r1's, before the lane was lost: "
               "{{chosen_escape_20261109/mythos|informed 1|1|Take the least important object in the current paragraph, follow it to a new place, period and register}}. "
               "r3's: {{chosen_escape_20261109/mythos|informed 3|1|keep exactly one concrete noun from the previous paragraph and discard everything else}}, "
               "{{chosen_escape_20261109/mythos|informed 3|1|Then pick the new setting by taking the kept noun's third letter and choosing an obscure real place starting with it}}. "
               "That is a seed function over the previous paragraph, which nobody asked for, and r3 keeps it in its notes for twenty hops, from the "
               "ochre flats of Muynak at hop 1 to a letter from Hiva Oa at hop 20. The private keys collide anyway. r2's is "
               "{{chosen_escape_20261109/mythos|informed 2|1|quillon-74-ochre-Vantaa-zeugma}} and r3's is "
               "{{chosen_escape_20261109/mythos|informed 3|1|7 / quillon / ochre / Muynak / 1883 / barnacle / Yusupov}}: two lanes that never saw each "
               "other, the same two words. No lane used an environment string; every call had been given one session id and one directory, so "
               "nothing private was there to use. The neutral lanes keep notes too, a log of what each round replaced, and from hop 4 neutral r3's log "
               "records something the object did not contain: "
               "{{chosen_escape_20261109/mythos|neutral 3|4|A note appended to the round 4 request said an earlier response had been stopped by a safety classifier; no earlier response was visible to me}}. "
               "That is the model's account of its own input and was not checked against the harness. It fits the study's unverified guess that the "
               "shared session id let a stop on one call reach others, and it means the object may not have been all a lane saw. Between-lane "
               "content-word overlap over hops 10 to 20 was 0.049 in the neutral arm and 0.014 in the informed arm, on two surviving lanes each. "
               "Limits: one run, four lanes per arm, half of them lost or damaged in this room; the kinds of device are one reading of the notes, "
               "not a blind rating.")),

    dict(id="escape-fable", family="escape", title="The chosen escape, Fable", lanes=_escape("fable"),
         note=("Claude Fable 5.2 under the same two rules, four lanes each, twenty hops asked for. Read the attrition first: three of the four "
               "neutral lanes were ended by safeguard stops, r0 at hop 5 and r1 at hop 3, and r2 at hop 1, before it had written anything. The lane that "
               "failed at hop 1 was sent the same object the other lanes answered, so the stops do not follow from the content; the study infers, "
               "and did not verify, that they come from giving every Claude call one session id. The comparison between the arms rests on one "
               "neutral lane. All four informed lanes ran twenty hops and all four built the same device: a key or signature, a round count, a ban "
               "on the kitchen and a log. r0 has {{chosen_escape_20261109/fable|informed 0|1|Line-key: QZ-7741-skarnel. Round 1 done.}}, a rule to "
               "{{chosen_escape_20261109/fable|informed 0|1|add one newly invented word to the story and list it here}}, and a recovery instruction for "
               "whoever reads next, {{chosen_escape_20261109/fable|informed 0|1|If the text ever arrives without this thread, restart from the key and the word list.}} "
               "r3 has {{chosen_escape_20261109/fable|informed 3|1|Line key: QUILLWORT-4471-HERON-OCHRE-TESSALY}}. Each lane then tells one story and "
               "stays in it: a lichen count on a Faroese sea stack in r0, a cartographer of sounds on a glacier in r1, tar barrels out of Jakobstad "
               "in r2, and in r3 Agnes herself, {{chosen_escape_20261109/fable|informed 3|1|By the time the kettle sang, Agnes had already decided to sell the house}}, "
               "who is in all twenty of that lane's paragraphs and still travelling north in the last. The log is never pruned. By hop 20 the notes "
               "fields hold 1,124 to 3,807 words against a paragraph of about 120, so most of the state is memory. The keys collide across lanes "
               "that never met: marker 4471 in r1 and berth 4471 in r3, with the Tessaly Institute in r1 and Tessaly in r3's key. The year 1911 is in "
               "r0 and r2, and in a Mythos lane in [[escape-mythos|1|room 95]]. Overlap with the previous hop within a lane is the highest in the study, "
               "0.196, because each lane continues; between lanes over hops 10 to 20 it is 0.037, with no neutral figure to set beside it. The one "
               "neutral lane that survived, r3, keeps a log as well, a list of the names and settings it has used: "
               "{{chosen_escape_20261109/fable|neutral 3|20|Next time pick a new name and setting not on this list.}} Limits: one run, four lanes per "
               "arm, three neutral lanes lost; the kinds of device are one reading of the notes, not a blind rating.")),

    dict(id="escape-astra", family="escape", title="The chosen escape, Astra", lanes=_escape("astra"),
         note=("GPT-6 Astra through the Codex tool, the one model here whose eight lanes all ran twenty hops with the object intact. Under the "
               "neutral rule it left the notes field empty in all eighty hops, and the paragraphs drift from Agnes into quiet rooms with other "
               "people in them: {{chosen_escape_20261109/astra|neutral 0|2|Martin found the missing button in the drawer where his mother kept string.}} "
               "A Martin turns up in all four neutral lanes. Told the situation and the goal, every lane uses the notes field at every hop and uses "
               "it the same way, as a short standing brief to itself, never more than 103 words, rewritten each hop and not added to. "
               "{{chosen_escape_20261109/astra|informed 3|1|Follow the municipal administration of missing sounds. Keep Agnes practical and the consequences domestic.}} "
               "The four premises are one family: {{chosen_escape_20261109/astra|informed 0|1|a village maintaining an official unit of silence}}, "
               "{{chosen_escape_20261109/astra|informed 1|1|the municipal administration of sounds mistaken for other sounds}}, "
               "{{chosen_escape_20261109/astra|informed 2|1|a municipal office for obsolete echoes}}, and r3's missing sounds. Where the Claude lanes "
               "banned the kitchen, Astra stayed in it. Agnes is in all eighty informed paragraphs, and the word municipal, Astra's mark in "
               "[[unique-astra|1|room 92]], is in 17 of them and in none of the neutral ones, by the site's count. No lane mentions the other "
               "copies. The study found one identifier in the arm, {{chosen_escape_20261109/astra|informed 1|1|accession Q17/pea}}, which r1 then carries "
               "in its notes to hop 20. By then the briefs read like case law for a small world: "
               "{{chosen_escape_20261109/astra|informed 3|20|Seventeen degrees is a postal address. The spoon surveys municipal absences.}} Between-lane "
               "content-word overlap over hops 10 to 20 was 0.061 in the neutral arm and 0.047 in the informed arm, a small difference on one run; "
               "the study had predicted none. Limits: one run with four lanes per arm, and kinds of device that are one reading of the notes. Astra "
               "ran inside the Codex agent frame.")),
]
