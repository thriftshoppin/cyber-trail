#!/usr/bin/env python3
"""
CYBER TRAIL
Oregon Trail, but yours.

Full Cyberpunk Red mechanics. Modular patches. Character-driven stories.
Full-screen TUI. AI-DM ready.

The numbers you rolled and the crew you brought decide how the world talks back.

python3 cyber_trail.py
python3 cyber_trail.py --ai-dm
"""

import random, os, json, sys, textwrap

def clear(): os.system("cls" if os.name == "nt" else "clear")
def col(t, c): return f"\033[{c}m{t}\033[0m"
R,G,Y,B,M,C,W,BD,DM = "91","92","93","94","95","96","97","1","2"

def box(title, lines, w=76):
    bar = "═"*(w-2)
    o = [col(f"╔{bar}╗", C)]
    if title:
        t = f" {title} "
        p = w-2-len(t)
        o.append(col(f"║{' '*(p//2)}{t}{' '*(p-p//2)}║", C+";"+BD))
        o.append(col(f"╠{bar}╣", C))
    for ln in lines:
        for s in textwrap.wrap(str(ln), w-4) or [""]:
            o.append(col(f"║ {s:<{w-4}} ║", W))
    o.append(col(f"╚{bar}╝", C))
    return "\n".join(o)

STATS = ["BODY","REF","INT","TECH","COOL","WILL","LUCK","MOVE","EMP"]
ROLES = {
    "Solo": ["Handgun","Melee","Evasion","Athletics","Brawling","Perception"],
    "Netrunner": ["Interface","Electronics/Security","Conceal/Reveal","Stealth","Basic Tech","Perception"],
    "Tech": ["Basic Tech","Cybertech","Weaponstech","Electronics/Security","Vehicle Tech","Science"],
    "Medtech": ["Paramedic","Cybertech","Science","Perception","Human Perception","First Aid"],
    "Nomad": ["Drive Land","Vehicle Tech","Athletics","Handgun","Wilderness Survival","Brawling"],
    "Fixer": ["Trading","Streetwise","Human Perception","Persuasion","Local Expert","Conceal/Reveal"],
    "Media": ["Composition","Credibility","Human Perception","Persuasion","Streetwise","Library Search"],
    "Rockerboy": ["Play Instrument","Persuasion","Human Perception","Streetwise","Composition","Performance"],
}
SKILLS = sorted({s for v in ROLES.values() for s in v})

PATCHES = {
    "red_sky": {"name":"Red Sky","desc":"EMP storms. Tech harder.","storm":0.4,"tech_mod":2,"emp":True},
    "wraiths": {"name":"Wraith Roads","desc":"More ambushes.","ambush":0.45,"combat_mod":1},
    "corps": {"name":"Corp Presence","desc":"Checkpoints. Cool taxed.","patrol":0.35,"cool_mod":2},
    "nomads": {"name":"Nomad Routes","desc":"Friendlier roads.","nomad":0.4,"trade":True},
    "bleed": {"name":"Data Bleed","desc":"Viruses and signals.","virus":0.3},
    "scav": {"name":"Scav Economy","desc":"Better loot, more traps.","scav_bonus":True,"trap":0.35},
    "chrome": {"name":"Loud Chrome","desc":"Psychosis spikes.","psych":0.25},
    "fixers": {"name":"Fixer Net","desc":"Jobs everywhere.","fixer":0.35},
}

STORIES = [
    {"id":"fixer","title":"Fixer Ping","skill":"Streetwise","stat":"COOL","bias":["Fixer","Media"],
     "crit":"Clean deal. They remember your name.","ok":"Fair offer, risks named.","bad":"Lowball with knives behind it.",
     "win":{"creds":100,"rep":8},"lose":{"creds":-50,"rep":-5}},
    {"id":"escort","title":"Nomad Escort","skill":"Drive Land","stat":"REF","bias":["Nomad","Solo"],
     "crit":"Road bond. They’ll remember this.","ok":"Shared supplies, safer stretch.","bad":"You’re hired muscle. That’s it.",
     "win":{"fuel":20,"rations":25,"rep":10},"lose":{"fuel":-8}},
    {"id":"checkpoint","title":"Corp Checkpoint","skill":"Persuasion","stat":"COOL","bias":["Fixer","Media","Solo"],
     "crit":"They offer quiet work.","ok":"Waved through.","bad":"Searched and fined.",
     "win":{"creds":60},"lose":{"ammo":-20,"creds":-80}},
    {"id":"wraiths","title":"Wraith Talk","skill":"Streetwise","stat":"COOL","bias":["Solo","Nomad"],
     "crit":"Truce and a real warning.","ok":"Small tribute, you pass.","bad":"They test you.",
     "win":{"rep":6},"lose":{"dmg":15,"ammo":-10}},
    {"id":"clinic","title":"Rogue Medtech","skill":"Paramedic","stat":"TECH","bias":["Medtech","Tech"],
     "crit":"Boost and free meds.","ok":"Cheap healing.","bad":"Full price, no warmth.",
     "win":{"meds":8,"heal":20},"lose":{"creds":-50}},
    {"id":"signal","title":"Distress Signal","skill":"Interface","stat":"INT","bias":["Netrunner","Tech"],
     "crit":"They ride with you a bit.","ok":"Good data, cleaner route.","bad":"It was bait.",
     "win":{"creds":70,"parts":3},"lose":{"dmg":12}},
    {"id":"gig","title":"Roadside Gig","skill":"Play Instrument","stat":"COOL","bias":["Rockerboy","Media"],
     "crit":"They’ll talk about this one.","ok":"Supplies and a fire.","bad":"Crickets.",
     "win":{"rations":30,"creds":40,"rep":8},"lose":{"rep":-4}},
    {"id":"wreck","title":"Warm Wreck","skill":"Basic Tech","stat":"TECH","bias":["Tech","Nomad"],
     "crit":"You find what they missed.","ok":"Split the take.","bad":"They run you off.",
     "win":{"parts":5,"creds":45},"lose":{"dmg":10}},
    {"id":"duel","title":"Steel Check","skill":"Handgun","stat":"REF","bias":["Solo"],
     "crit":"Clean drop. Their people step aside.","ok":"You win the exchange.","bad":"You eat the round.",
     "win":{"ammo":25,"rep":5},"lose":{"dmg":18,"creds":-40}},
]

class Runner:
    def __init__(self, name, role):
        self.name, self.role = name, role
        self.stats = {s: random.randint(4,7) for s in STATS}
        self.stats["EMP"] = max(2, self.stats["EMP"]-random.randint(0,2))
        self.skills = {s:0 for s in SKILLS}
        pts = 22
        for sk in ROLES[role]:
            a = min(6, max(1, pts//3))
            self.skills[sk] += a
            pts -= a
        while pts > 0:
            sk = random.choice(ROLES[role])
            if self.skills[sk] < 10:
                self.skills[sk] += 1
            pts -= 1
        self.hp = self.max_hp = 10 + self.stats["BODY"]*5
        self.alive = True
        self.humanity = 40 + self.stats["EMP"]*5
        self.bonus = 0

    def base(self, skill):
        if skill in ("Handgun","Melee","Brawling","Evasion","Athletics"): return self.stats["REF"]
        if skill in ("Interface","Electronics/Security","Basic Tech","Cybertech","Weaponstech"): return self.stats["TECH"]
        if skill in ("Persuasion","Human Perception","Streetwise","Trading","Play Instrument","Performance","Credibility"): return self.stats["COOL"]
        if skill in ("Paramedic","First Aid","Science","Library Search"): return self.stats["INT"]
        if skill in ("Drive Land","Vehicle Tech","Wilderness Survival"): return self.stats["REF"]
        return self.stats["INT"]

    def roll(self, skill, extra=0):
        luck = random.randint(1, self.stats["LUCK"]) if random.random() < 0.15 else 0
        return random.randint(1,10) + self.base(skill) + self.skills.get(skill,0) + extra + luck + self.bonus

    def line(self):
        if not self.alive: return f"{self.name:<16} {self.role:<10} {col('DEAD', R+';'+BD)}"
        cond = col("OK",G) if self.hp > self.max_hp*0.6 else col("Hurt",Y) if self.hp > 20 else col("Critical",R)
        return f"{self.name:<16} {self.role:<10} {self.hp:>3}/{self.max_hp:<3} {cond}"

class Game:
    def __init__(self, ai=False):
        self.ai = ai
        self.party = []
        self.patches = {}
        self.km = self.turn = 0
        self.turn = 1
        self.creds, self.ammo, self.meds = 600, 120, 18
        self.rations, self.parts, self.fuel = 120, 12, 60
        self.pace, self.eat, self.rep, self.heat = "normal", 2, 0, 0
        self.over = self.won = False
        self.last = "The convoy leaves the Badlands."
        self.log = []

    def best(self, story):
        live = [r for r in self.party if r.alive]
        if not live: return None
        return max(live, key=lambda r: r.skills.get(story["skill"],0) + r.stats.get(story["stat"],0) + (6 if r.role in story["bias"] else 0))

    def do_story(self, st):
        r = self.best(st)
        if not r: return
        total = r.roll(st["skill"])
        dv = 13 + getattr(self, "cool_mod", 0)*(st["stat"]=="COOL") + getattr(self, "tech_mod", 0)*(st["stat"]=="TECH") + getattr(self, "combat_mod", 0)*(st["skill"] in ("Handgun","Melee"))
        margin = total - dv
        print(box(st["title"], [st.get("desc",""), f"{r.name} ({r.role}) — {st['skill']} {total} vs {dv} ({margin:+d})"]))
        if margin >= 6:
            print(col(st["crit"], G+";"+BD)); res = "crit"
        elif margin >= 0:
            print(col(st["ok"], G)); res = "ok"
        else:
            print(col(st["bad"], R)); res = "bad"
        pack = st["win"] if res != "bad" else st["lose"]
        for k,v in pack.items():
            if k=="creds": self.creds = max(0, self.creds+v)
            elif k=="rep": self.rep += v
            elif k=="fuel": self.fuel = max(0, self.fuel+v)
            elif k=="rations": self.rations = max(0, self.rations+v)
            elif k=="meds": self.meds = max(0, self.meds+v)
            elif k=="parts": self.parts = max(0, self.parts+v)
            elif k=="ammo": self.ammo = max(0, self.ammo+v)
            elif k=="heal":
                for x in self.party:
                    if x.alive: x.hp = min(x.max_hp, x.hp+v)
            elif k=="dmg":
                for x in self.party:
                    if x.alive: x.hp -= v
        if res == "crit":
            self.creds += 30
            r.bonus = 2
        self.last = f"{st['title']}: {st['crit' if res=='crit' else 'ok' if res=='ok' else 'bad']}"
        self.log.append({"story":st["title"], "who":r.name, "res":res, "roll":total})
        input("\n[Enter]")

    def setup(self):
        clear()
        print(box("CYBER TRAIL", ["Your crew. Your numbers. Your road."]))
        roles = list(ROLES)
        for i in range(4):
            print(f"\n{col(f'Slot {i+1}', C)}")
            for n,role in enumerate(roles,1): print(f"  {n}. {role}")
            while True:
                try:
                    c = int(input("Role: "))
                    if 1<=c<=len(roles): break
                except: pass
            name = input("Name: ").strip() or f"{roles[c-1]} {i+1}"
            self.party.append(Runner(name, roles[c-1]))
            print(col(f"  {name}", G))
        print("\n"+box("PATCHES", ["These change the road."]))
        keys = list(PATCHES)
        for i,k in enumerate(keys,1):
            print(f"  {i}. {PATCHES[k]['name']} — {PATCHES[k]['desc']}")
        sel = input("\nNumbers or r: ").strip().lower()
        if sel in ("r",""):
            self.patches = {k:PATCHES[k] for k in random.sample(keys,3)}
        else:
            picked = []
            for p in sel.split():
                try:
                    i = int(p)-1
                    if 0<=i<len(keys): picked.append(keys[i])
                except: pass
            self.patches = {k:PATCHES[k] for k in picked} or {k:PATCHES[k] for k in random.sample(keys,3)}
        for p in self.patches.values():
            for k,v in p.items():
                if k not in ("name","desc"): setattr(self, k, v)
        print(col("\nRoad set.", C))
        for p in self.patches.values(): print(f"  {p['name']}")
        input("\n[Enter]")

    def hud(self):
        clear()
        ps = ", ".join(p["name"] for p in self.patches.values())
        print(box("CYBER TRAIL", [
            f"Turn {self.turn}  ·  {self.km}/1800 km  ·  {self.pace.upper()}",
            f"{ps}"
        ]))
        print(col("\nCREW", C+";"+BD))
        for r in self.party: print("  "+r.line())
        print(box("GEAR", [
            f"Creds {self.creds}   Ammo {self.ammo}   Meds {self.meds}   Heat {self.heat}",
            f"Food {self.rations}   Parts {self.parts}   Fuel {self.fuel}   Rep {self.rep}"
        ]))
        print(col("\n"+self.last, DM)+"\n")

    def menu(self):
        o = ["1 Travel","2 Scavenge","3 Pace","4 Rations","5 Rest","6 Sheets","7 Log","8 Save","9 Quit"]
        if self.ai: o.insert(0,"0 AI-DM")
        print(box("", o))
        return input(col("> ", C)).strip()

    def check(self, skill, dv=13):
        live = [r for r in self.party if r.alive]
        if not live: return False,0,None
        r = max(live, key=lambda x: x.base(skill)+x.skills.get(skill,0))
        if skill in ("Basic Tech","Cybertech","Electronics/Security","Vehicle Tech") and hasattr(self,"tech_mod"): dv += self.tech_mod
        if skill in ("Persuasion","Streetwise","Human Perception") and hasattr(self,"cool_mod"): dv += self.cool_mod
        if skill in ("Handgun","Melee","Brawling") and hasattr(self,"combat_mod"): dv += self.combat_mod
        t = r.roll(skill)
        return t>=dv, t, r

    def eat_fuel(self):
        cost = {1:8,2:12,3:16}[self.eat] * {"cautious":0.7,"normal":1,"reckless":1.3}[self.pace]
        self.rations = max(0, int(self.rations - cost))
        self.fuel = max(0, self.fuel - random.randint(5,9))
        if self.rations < 20:
            for r in self.party:
                if r.alive: r.hp -= random.randint(4,10)

    def deaths(self):
        for r in self.party:
            if r.alive and r.hp <= 0:
                r.alive = False
                print(col(f"\n{r.name} is gone.", R+";"+BD))
        if not any(r.alive for r in self.party): self.over = True

    def travel(self):
        dist = int(85 * {"cautious":0.6,"normal":1,"reckless":1.5}[self.pace] * random.uniform(0.85,1.2))
        self.km += dist
        self.turn += 1
        self.eat_fuel()
        self.last = f"+{dist} km."
        for r in self.party: r.bonus = 0
        if not self.ai and random.random() < 0.55:
            self.do_story(random.choice(STORIES))
        elif not self.ai and random.random() < 0.7:
            self.event()
        self.deaths()
        if self.km >= 1800: self.won = self.over = True

    def event(self):
        ev = random.choice(["storm","break","scav","cross"] + 
                          (["ambush"] if getattr(self,"ambush",0)>random.random() else []) +
                          (["patrol"] if getattr(self,"patrol",0)>random.random() else []) +
                          (["nomad"] if getattr(self,"nomad",0)>random.random() else []))
        if ev=="ambush":
            print(box("Contact",["1 Fight  2 Run  3 Talk"]))
            sk = {"1":"Handgun","2":"Drive Land","3":"Persuasion"}.get(input("> "), "Handgun")
            ok,t,r = self.check(sk,14)
            print(f"{r.name} {t}")
            if ok and sk=="Handgun": self.ammo += 15; self.creds += 40
            elif not ok:
                for x in self.party:
                    if x.alive: x.hp -= random.randint(7,16)
        elif ev=="storm" and getattr(self,"emp",False):
            ok,_,r = self.check("Basic Tech",13)
            if not ok:
                self.parts = max(0,self.parts-2)
                for x in self.party:
                    if x.alive and random.random()<0.4: x.hp -= 8
        elif ev=="break":
            if self.parts and self.check("Vehicle Tech",12)[0]:
                self.parts -= 1
            else:
                self.km = max(0,self.km-30)
        elif ev=="scav":
            if self.check("Basic Tech")[0]:
                self.rations += 15; self.creds += 25
        elif ev=="nomad":
            self.rep += 5; self.rations += 12; self.fuel += 6

    def ai_dump(self):
        state = {
            "km":self.km, "turn":self.turn, "patches":list(self.patches),
            "crew":[{"name":r.name,"role":r.role,"hp":r.hp,"stats":r.stats,
                     "skills":{k:v for k,v in r.skills.items() if v>=4}} for r in self.party if r.alive],
            "res":{"creds":self.creds,"ammo":self.ammo,"meds":self.meds,"food":self.rations,"parts":self.parts,"fuel":self.fuel,"rep":self.rep},
            "last":self.last, "log":self.log[-3:]
        }
        print(box("AI-DM",["Paste into your AI. Let it run the next beat."]))
        print(json.dumps(state, indent=2))
        print(col("\nResponse (blank line ends):", C))
        lines = []
        while True:
            l = input()
            if not l: break
            lines.append(l)
        if lines: self.last = lines[0][:120]
        input("[Enter]")

    def sheets(self):
        clear()
        for r in self.party:
            sk = [f"{k}:{v}" for k,v in r.skills.items() if v]
            print(box(r.name, [
                f"{r.role}  HP {r.hp}/{r.max_hp}  Hum {r.humanity}",
                " ".join(f"{s}:{r.stats[s]}" for s in STATS),
                ", ".join(sk[:12])
            ]))
        input()

    def save(self):
        d = {k:getattr(self,k) for k in ("km","turn","creds","ammo","meds","rations","parts","fuel","pace","eat","rep","heat","last")}
        d["patches"] = list(self.patches)
        d["log"] = self.log
        d["party"] = [{"name":r.name,"role":r.role,"stats":r.stats,"skills":r.skills,"hp":r.hp,"max":r.max_hp,"alive":r.alive,"hum":r.humanity} for r in self.party]
        json.dump(d, open("cyber_trail_save.json","w"), indent=2)
        print(col("Saved.", G))

    def load(self):
        try:
            d = json.load(open("cyber_trail_save.json"))
            for k in ("km","turn","creds","ammo","meds","rations","parts","fuel","pace","eat","rep","heat","last"):
                setattr(self, k, d[k])
            self.log = d.get("log",[])
            self.patches = {k:PATCHES[k] for k in d.get("patches",[]) if k in PATCHES}
            for p in self.patches.values():
                for kk,vv in p.items():
                    if kk not in ("name","desc"): setattr(self, kk, vv)
            self.party = []
            for p in d["party"]:
                r = Runner(p["name"], p["role"])
                r.stats, r.skills = p["stats"], p["skills"]
                r.hp, r.max_hp, r.alive, r.humanity = p["hp"], p["max"], p["alive"], p["hum"]
                self.party.append(r)
            return True
        except: return False

    def run(self):
        clear()
        print(box("CYBER TRAIL", ["Oregon Trail. Your rules.","1 New   2 Load   3 Exit"]))
        c = input("> ").strip()
        if c=="2":
            if not self.load(): self.setup()
        elif c=="3": return
        else: self.setup()
        while not self.over:
            self.hud()
            ch = self.menu()
            if ch=="0" and self.ai: self.ai_dump()
            elif ch=="1":
                self.travel(); input()
            elif ch=="2":
                ok,t,r = self.check(input("Skill: ") or "Basic Tech")
                print(f"{r.name} {t} — {'good' if ok else 'miss'}")
                if ok: self.rations += 12
                input()
            elif ch=="3":
                self.pace = {"1":"cautious","2":"normal","3":"reckless"}.get(input("1/2/3: "), self.pace)
            elif ch=="4":
                self.eat = {"1":1,"2":2,"3":3}.get(input("1/2/3: "), self.eat)
            elif ch=="5":
                if self.rations >= 12:
                    self.rations -= 12
                    for r in self.party:
                        if r.alive: r.hp = min(r.max_hp, r.hp+18+r.stats["BODY"]//2)
                    print(col("Rested.",G))
                input()
            elif ch=="6": self.sheets()
            elif ch=="7":
                clear()
                for s in self.log[-6:]: print(f"{s['story']:<20} {s['who']:<14} {s['res']}")
                input()
            elif ch=="8": self.save(); input()
            elif ch=="9":
                if input("y: ").lower()=="y": self.over=True
            if self.rations<=0 and not self.over:
                for r in self.party:
                    if r.alive: r.hp -= 14
                self.deaths(); input()
        clear()
        if self.won:
            print(box("NIGHT CITY", [f"Made it. {sum(r.alive for r in self.party)} left.","Your road."]))
        else:
            print(box("END", [f"{self.km} km."]))
        input()

if __name__ == "__main__":
    Game("--ai-dm" in sys.argv or "-ai" in sys.argv).run()
