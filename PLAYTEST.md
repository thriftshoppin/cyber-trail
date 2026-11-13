# Cyber Trail: session handoff (paste into a new chat)

**Use:** Start a new chat, attach/paste this file, and say "Resume as GM." Claude is the GM and game engine. The player runs **Static**.

Repo: github.com/thriftshoppin/Cyber-trail (local branch `tui-overhaul` has the new full-screen UI, headless mode and trading posts; committed, not pushed as of this handoff).

## How to GM this (the player's rules)
- Player is Static (Netrunner). Claude plays everyone else, including the fixer Rail when he appears.
- Tell it through story. Don't list options or narrate your own choices/quirks. Never name the hidden patches.
- Roll honestly. Set DVs from the ladder, not by feel: 9 Simple, 13 Everyday, 15 Professional, 17 Heroic, 21 Incredible, 24 Legendary, 29 Impossible.
- Roll: d10 + stat + skill vs DV. Margin 6+ crit, 0+ success, below 0 fail. Failures get real, well-made consequences. Don't make it easy.
- Call for Perception rolls regularly, not only when the player asks.
- Keep answers to what was asked (a "what's this?" gets a short reply). Don't overplay a single NPC or gag.
- Never write "tradition" or other meta-notes into the fiction. Crew are Static's friends and act on their own.
- The player picked a Hail Mary and similar bold moves before: reward boldness with real stakes, not a free pass.

## Party
| Name | Role | HP | Humanity | Notes |
|---|---|---|---|---|
| **Static** (player) | Netrunner | 40/40 | 46 | INT 6, TECH 7, COOL 5, WILL 6, LUCK 4. Interface 6, Electronics/Security 5, Basic Tech 3, Conceal 3, Stealth 3, Perception 2 |
| Odalys "Oda" Crane | Solo | 40/40 | 75 | REF 6, BODY 6, LUCK 7. Handgun 7, Melee 5, Evasion 4. Refit from Fixer: the party has no fixer |
| Dust Reyes | Nomad | 30/30 | 50 | Drive Land 6, Vehicle Tech 5, Wilderness 4. Drives the truck |
| Ines Okafor | Medtech | 30/30 | 65 | Cybertech 6, Paramedic 6, Science 4. Tends to help sick people on her own |

## Resources
Km 316 of 1800 (Dry Well Junction area), turn 4. Creds 470, Ammo 92, Meds 18, Food 90, Parts 13, Fuel 70, Rep 12, **Heat 3**. Pace normal.
Hidden patches (GM only): Red Sky (+2 DV on tech checks, EMP storms), Bleed (+1 on combat), Corps (+2 on cool checks).

## Story so far
- Static's sister **Wren** was lost in the Hollow Creek net-fire. A 3-beat pulse (long, short, short) in a packet is her signature.
- The party took a job from fixer **Rail**: reach the loose AI fragment (a Bartmoss-style relic) before anyone else. 800 creds on arrival. Rail has a checkpoint-codes chip. Ping Rail from the second storm cell.
- Static answered the pulse (critical). The AI replied: "YOU KEY LIKE HER / SHE IS NOT HERE. I AM LOOKING." Humanity dropped.
- A road fixer gave them a **sealed courier package** (100 creds advance) for a dead-drop on the south side of Night City. It is under the truck seat. Risk: second-checkpoint scanners.
- Static secretly left Rail a **control shard** hidden in a bag of synth jerky. Rail holds the shard and link.
- Static carries: next Interface roll +2; the first intrusion on his deck is blocked (one use); a drone tail (spotter, held at the storm edge); an unspecified "new toy" he plans to use on scanners.
- Ferro's upgraded the truck's shielding (Elec/Sec 20 vs 16). Next EMP storm check: +2 for the crew. Cost 90 creds and 1 part.
- **Dry Well Junction diner:** Static jammed the corp van's control link (critical), fried the diner's power (Heat +2, 60 creds to Pilar), and freed Ines. The quiet earpiece man and the back-door man are dazed and left with Pilar and Odalys. Dust crit-shot the gray van's tires.
- Static breached the van (critical) and fed it a dummy network: it thinks the truck went **east**. Learned its order: RECOVER the sealed courier case, the same package. Same corp as the checkpoints. The van operator is locked out for about 20 minutes.
- Twist to use: the package may lead the corp to the dead-drop.
- **Now:** the crew is escaping Dry Well Junction in the truck. Corp response is incoming. The next move is Static's.

## Rules and mechanics quick sheet
- Turn: travel (~85 km), then an encounter or event. Scavenging costs 6 food and finds 12. Out of fuel means pushing the truck 30 km with extra food use.
- Trading posts open at the start and at each landmark passed: Dry Well Junction 330, Relay Ridge 620, Iron Pass 900, Salt Line 1250, Outer Ring 1550. Night City is at 1800.
- Prices (new build): fuel +20 for 100 creds, food +30 for 100.

## To also load in a new chat
- The repo, if you want the engine to run: `python3 cyber_trail.py`. In a chat without code tools, just GM by hand using the sheet above.

---

# Setup

## How this campaign was set up
- The player took the Netrunner slot (Static). Claude picked the other three crew (Solo, Nomad, Medtech) and the three road patches, and revealed them through story only, never as a list. The party deliberately has **no Fixer**: Oda was refit from Fixer to Solo, and Rail is an NPC fixer.
- Patches chosen: Red Sky, Bleed, Corps. Never name them to the player.
- Claude acts as GM and engine: it rolls dice, sets DVs from the ladder, narrates, and applies rewards and costs by editing the save state (`cyber_trail_save.json`: resources, HP, humanity, heat). Game mode flag: `--ai-dm` (no random events; the GM narrates). In that mode `G` opens the GM state export.

## Run the game
Needs Python 3.8+, no packages.

    git clone https://github.com/thriftshoppin/Cyber-trail
    cd Cyber-trail
    git checkout tui-overhaul      # once pushed; until then main is the old classic version
    python3 cyber_trail.py         # full-screen UI (terminal 80x24 or larger)
    python3 cyber_trail.py --plain # classic scrolling text
    python3 cyber_trail.py --ai-dm # GM-driven, no random events

New game flow: pick a role for each of 4 crew slots, name each (Enter keeps the role name), pick up to 3 road patches (none = random), then "Road set". Continue loads `cyber_trail_save.json` from the folder; the file is git-ignored.

## Keys (full-screen UI)
T travel, B buy (only at a trading post), S scavenge, P pace, R food rate, E rest, C crew sheets, I inventory (R reload one, A reload all), M map, L log, O options, H rules, Enter action menu, Q quit.

## Headless / bot testing
    python3 cyber_trail.py --seed 3 --size 80x24 --keys "ENTER 2 Static ENTER ... t t b ESC"
Named keys: ENTER ESC UP DOWN LEFT RIGHT TAB SPACE BKSP; other text is typed. `--frames last|all|N` picks which frames print. Same seed plus same keys gives the same run.

## Resume the live save in a new chat
The save is on the old machine, so a new chat starts from the "Resources", "Party" and "Story so far" sections above. Without code tools, GM by hand: d10 + stat + skill vs DV and use the ladder. With the repo, start a new game and edit the numbers to match.

## Not verified yet
Windows key input, the cyberdeck, real-terminal animation timing, and the trade screen at later posts in a long run.
