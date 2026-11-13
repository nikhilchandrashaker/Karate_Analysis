import re,json,math,os,shutil
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle,Rectangle,Patch
OUT="/mnt/user-data/outputs/biomechanics"; os.makedirs(OUT,exist_ok=True)
src=open("/mnt/user-data/outputs/karate-showdown.html",encoding="utf-8").read()
C=json.loads(re.search(r"var C=(\[.*?\n\]);",src,re.S).group(1))
PR=json.loads(re.search(r"var P=(\[.*?\]\]);",src).group(1))
SHOW=["Cobra Kai","Kickin’ It"];COL=["#E6B000","#6AAD1D"];DK=["#8A6500","#3F7A0C"];INK="#1d1b17";BG="#f3f5f8"
def v(a):
    r=math.radians(a);return np.array([math.sin(r),-math.cos(r)])
def mid(a,b):return (a+b)/2
def model(c):
    name,sh,st,s0,s1,bl=c;tech,spd,pw,strat,dis,res=st
    phi=55+8*tech;ext=min(180,118+6.2*tech);flex=180-ext
    lean=math.radians(6+.22*(phi-55)+1.8*(10-dis))
    P=np.array([0,.531]);ks=np.array([0,.286]);As=np.array([0,.04]);ts=np.array([.105,0.]);heel=np.array([-.04,0.])
    kn=P+.245*v(phi);ad=phi-flex;an=kn+.246*v(ad);toe=an+.11*v(ad)
    u=np.array([-math.sin(lean),math.cos(lean)]);S=P+.288*u;hd=S+.09*u
    eL=S+.186*v(30);hL=eL+.2*v(min(160,70+8*dis));eR=S+.186*v(-25);hR=eR+.2*v(40+6*dis)
    sg=[(.497,mid(P,S)),(.081,hd),(.028,mid(S,eL)),(.022,mid(eL,hL)),(.028,mid(S,eR)),(.022,mid(eR,hR)),(.1,mid(P,ks)),(.0465,mid(ks,As)),(.0145,mid(As,ts)),(.1,mid(P,kn)),(.0465,mid(kn,an)),(.0145,mid(an,toe))]
    com=sum(m*p for m,p in sg)/sum(m for m,p in sg)
    vf=4.5+.7*spd+.3*tech
    return dict(name=name,sh=sh,st=st,s0=s0,s1=s1,bl=bl,phi=phi,ext=ext,lean=math.degrees(lean),
      J=dict(P=P,S=S,hd=hd,kn=kn,an=an,toe=toe,ks=ks,As=As,ts=ts,heel=heel,eL=eL,hL=hL,eR=eR,hR=hR),com=com,
      bal=max(0,1-abs(com[0]-.0325)/.145)*100,vf=vf,imp=(.5+.1*pw)*vf**2,eff=100*(.35+.065*tech),dl=10+3.5*tech,toeh=toe[1]*100)
M=[model(c) for c in C];IDX={m["name"]:i for i,m in enumerate(M)}
im=max(m["imp"] for m in M)
for m in M:m["impn"]=100*m["imp"]/im
mxT=max(m["toeh"] for m in M);mxV=max(m["vf"] for m in M)
def fr(m):return [m["toeh"]/mxT,m["vf"]/mxV,m["impn"]/100,m["bal"]/100,m["eff"]/100]
MEAN=np.mean([fr(m) for m in M],axis=0)
def seg(ax,pts,col,alpha,lw):
    p=np.array(pts);ax.plot(p[:,0],p[:,1],color=col,lw=lw,alpha=alpha,solid_capstyle="round",solid_joinstyle="round",path_effects=[pe.Stroke(linewidth=lw+2.4,foreground=INK),pe.Normal()])
def skel(ax,m,alpha=1,lw=5):
    J=m["J"];col=COL[m["sh"]];dk=DK[m["sh"]]
    seg(ax,[J["S"],J["eR"],J["hR"]],dk,alpha,lw-1)
    seg(ax,[J["P"],J["S"]],col,alpha,lw+2)
    ax.add_patch(Circle(J["hd"],.062,fc=col,ec=INK,lw=1.8,alpha=alpha,zorder=4))
    seg(ax,[J["heel"],J["As"],J["ts"]],dk,alpha,lw-1)
    seg(ax,[J["P"],J["ks"],J["As"]],dk,alpha,lw)
    seg(ax,[J["P"],J["kn"],J["an"],J["toe"]],col,alpha,lw+1)
    seg(ax,[J["S"],J["eL"],J["hL"]],col,alpha,lw-1)
    for k in ("P","S","kn","an","ks","eL","eR"):ax.plot(*J[k],"o",ms=6,mfc="white",mec=INK,zorder=6)
def fig_char(m,path):
    col,dk=COL[m["sh"]],DK[m["sh"]]
    fig=plt.figure(figsize=(15,6),facecolor=BG)
    gs=fig.add_gridspec(1,3,width_ratios=[1.05,1.15,1.1],left=.03,right=.98,bottom=.12,top=.78,wspace=.22)
    fig.patches.append(Rectangle((0,.9),1,.1,transform=fig.transFigure,fc=col,ec="none"))
    fig.text(.02,.95,m["name"],fontsize=24,fontweight="bold",color=INK,va="center")
    fig.text(.98,.95,SHOW[m["sh"]],fontsize=16,fontweight="bold",color=INK,va="center",ha="right")
    fig.text(.02,.855,m["bl"],fontsize=11,style="italic",color=INK)
    fig.text(.02,.815,"Ratings  technique %d · speed %d · power %d · strategy %d · discipline %d · resolve %d   |   growth %d → %d"%(*m["st"],m["s0"],m["s1"]),fontsize=10,color=INK)
    a=fig.add_subplot(gs[0]);a.set_aspect("equal");a.set_xlim(-.5,.85);a.set_ylim(-.06,1.1);a.axis("off")
    a.axhline(0,color=INK,lw=1.5);a.plot([-.04,.105],[-.014,-.014],color=dk,lw=6,solid_capstyle="butt")
    skel(a,m);c=m["com"]
    a.plot([c[0],c[0]],[0,c[1]],"--",color=INK,lw=1);a.plot(*c,"X",ms=12,mfc=col,mec=INK,zorder=7);a.text(c[0]-.04,c[1],"COM",fontsize=8,ha="right",va="center")
    a.text(-.48,1.08,"Hip flexion %d°\nKnee extension %d°\nTrunk lean %d°"%(m["phi"],m["ext"],m["lean"]),va="top",fontsize=9,bbox=dict(fc="white",ec=INK,boxstyle="round"))
    a.set_title("Kick pose (side view, normalized height)",fontsize=10,y=1.0)
    b=fig.add_subplot(gs[1]);b.set_facecolor(BG);t=np.linspace(0,260,400);tech,spd,pw=m["st"][:3]
    for amp,tp,lab,ls,cc in [(5+.5*pw+.3*spd,60,"Hip","-",dk),(12+1.4*spd,60+m["dl"],"Knee","--",col),(8+.8*spd,60+2*m["dl"],"Ankle",":",INK)]:
        b.plot(t,amp*np.exp(-.5*((t-tp)/20)**2),ls,color=cc,lw=3,label=lab,path_effects=[pe.Stroke(linewidth=5,foreground=INK),pe.Normal()] if cc==col else None)
    b.set_title("Kinetic chain: joint angular velocity (rad/s)",fontsize=10);b.set_xlabel("Time (ms)");b.legend(frameon=False,loc="upper right")
    b.text(.02,.95,"Peak-to-peak lag %.1f ms"%m["dl"],transform=b.transAxes,fontsize=9,va="top")
    for s in("top","right"):b.spines[s].set_visible(False)
    d=fig.add_subplot(gs[2]);d.set_facecolor(BG)
    rows=[("Toe height","%.0f%% of H"%m["toeh"]),("Peak foot speed","%.1f m/s"%m["vf"]),("Impact index","%.0f"%m["impn"]),("Balance index","%.0f"%m["bal"]),("Chain efficiency","%.0f%%"%m["eff"])]
    y=np.arange(5)[::-1];f=fr(m)
    d.barh(y,f,color=col,edgecolor=INK,height=.55);d.scatter(MEAN,y,marker="|",s=900,color=INK,zorder=5,linewidths=2)
    for yi,r,ff in zip(y,rows,f):d.text(1.03,yi,r[1],va="center",fontsize=9)
    d.set_yticks(y);d.set_yticklabels([r[0] for r in rows]);d.set_xlim(0,1.4);d.set_xticks([])
    d.set_title("Metrics vs roster (| = roster mean)",fontsize=10)
    for s in("top","right","bottom"):d.spines[s].set_visible(False)
    fig.text(.02,.03,"Illustrative model: values are computed from editorial 1–10 skill ratings, not motion-capture or force-plate data.",fontsize=9,style="italic",color="#555")
    fig.savefig(path,dpi=140,facecolor=BG);plt.close(fig)
def shifted(m,dx,sg):
    m2=dict(m);m2["J"]={k:np.array([dx+sg*p[0],p[1]]) for k,p in m["J"].items()};return m2
def fig_match():
    fig,axs=plt.subplots(2,5,figsize=(21,9),facecolor=BG);fig.subplots_adjust(top=.85,bottom=.03,left=.01,right=.99,wspace=.03,hspace=.12)
    fig.patches.append(Rectangle((0,.9),.5,.1,transform=fig.transFigure,fc=COL[0],ec="none"));fig.patches.append(Rectangle((.5,.9),.5,.1,transform=fig.transFigure,fc=COL[1],ec="none"))
    fig.text(.5,.95,"Head-to-head kick models",fontsize=26,fontweight="bold",ha="center",va="center",color=INK)
    fig.text(.5,.875,"Cobra Kai (left, gold) vs Kickin’ It (right, green). Illustrative, rating-driven models.",fontsize=12,ha="center",style="italic",color=INK)
    for ax,(lab,an,bn) in zip(axs.flat,PR):
        ma,mb=M[IDX[an]],M[IDX[bn]];ax.set_aspect("equal");ax.set_xlim(-.5,1.85);ax.set_ylim(-.2,1.12);ax.axis("off")
        ax.plot([-.5,1.85],[0,0],color=INK,lw=1.3);skel(ax,ma);skel(ax,shifted(mb,1.35,-1))
        ax.set_title(lab,fontsize=14,fontweight="bold",color=INK)
        ax.text(.675,-.1,"foot speed %.1f vs %.1f m/s\nimpact %.0f vs %.0f · balance %.0f vs %.0f"%(ma["vf"],mb["vf"],ma["impn"],mb["impn"],ma["bal"],mb["bal"]),ha="center",va="center",fontsize=9.5)
    fig.savefig(OUT+"/summary_matchups.png",dpi=110,facecolor=BG);plt.close(fig)
def fig_roster():
    fig,ax=plt.subplots(figsize=(12,8),facecolor=BG);ax.set_facecolor(BG)
    for m in M:
        ax.scatter(m["vf"],m["impn"],s=60+m["eff"]*4,c=COL[m["sh"]],edgecolors=INK,linewidths=1.5,zorder=3)
        ax.text(m["vf"]+.07,m["impn"]+.9,m["name"].split()[0],fontsize=8.5)
    ax.set_xlabel("Estimated peak foot speed (m/s)");ax.set_ylabel("Impact index (roster max = 100)")
    ax.set_title("Roster map: speed vs impact (marker size = kinetic-chain efficiency)",fontsize=14,fontweight="bold")
    ax.grid(color="#d4d9e1",lw=.8);ax.legend(handles=[Patch(fc=COL[0],ec=INK,label="Cobra Kai"),Patch(fc=COL[1],ec=INK,label="Kickin’ It")],loc="lower right",frameon=False)
    for s in("top","right"):ax.spines[s].set_visible(False)
    fig.text(.01,.01,"Illustrative model derived from editorial ratings.",fontsize=8,style="italic");fig.savefig(OUT+"/summary_roster.png",dpi=120,facecolor=BG);plt.close(fig)

HERE=os.path.dirname(os.path.abspath(__file__))
FJ=json.load(open(os.path.join(HERE,"fights.json"),encoding="utf-8"))
FI=[(f["ep"],f["a"],f["b"],f["w"]) for f in FJ]
def pwin(a,b):return 1/(1+math.exp(-(np.mean(a["st"])-np.mean(b["st"]))/1.5))
def fig_fights():
    n=len(FI);cols=4;rows=-(-n//cols);Hh=4.7*rows+1.9
    fig,axs=plt.subplots(rows,cols,figsize=(22,Hh),facecolor=BG);fig.subplots_adjust(top=1-1.6/Hh,bottom=.01,left=.005,right=.995,wspace=.02,hspace=.2)
    bd=.95/Hh
    fig.patches.append(Rectangle((0,1-bd),.5,bd,transform=fig.transFigure,fc=COL[0],ec="none"));fig.patches.append(Rectangle((.5,1-bd),.5,bd,transform=fig.transFigure,fc=COL[1],ec="none"))
    fig.text(.5,1-bd/2,"Documented fights vs model predictions",fontsize=28,fontweight="bold",ha="center",va="center",color=INK)
    fig.text(.5,1-1.3/Hh,"Outcomes paraphrased from episode recaps and fan wikis. Star marks the actual winner.",fontsize=13,ha="center",style="italic",color=INK)
    for ax,(ep,an,bn,w) in zip(axs.flat,FI):
        ma,mb=M[IDX[an]],M[IDX[bn]];pa=pwin(ma,mb);pw=pa if w==an else 1-pa
        mb2=shifted(mb,1.35,-1);ax.set_aspect("equal");ax.set_xlim(-.5,1.85);ax.set_ylim(-.28,1.25);ax.axis("off")
        ax.plot([-.5,1.85],[0,0],color=INK,lw=1.3);skel(ax,ma);skel(ax,mb2)
        hd=(ma if w==an else mb2)["J"]["hd"];ax.text(hd[0],hd[1]+.1,"★ winner",ha="center",fontsize=11,fontweight="bold")
        ax.set_title("%s vs %s"%(an,bn),fontsize=13,fontweight="bold",color=INK)
        ax.text(.675,-.17,"%s\nmodel: %s %.0f%% · %s %.0f%%  →  %s"%(ep,an.split()[0],pa*100,bn.split()[0],(1-pa)*100,"model called it" if pw>.5 else "upset the model missed"),ha="center",va="center",fontsize=9.5)
    for ax in list(axs.flat)[n:]:ax.axis("off")
    fig.savefig(OUT+"/fight_examples.png",dpi=80,facecolor=BG);plt.close(fig)
def extra():
    rows=[];hit=0;br=0;tot=[0,0];hs=[0,0];worst=None
    for ep,an,bn,w in FI:
        ma,mb=M[IDX[an]],M[IDX[bn]];pa=pwin(ma,mb);pw=pa if w==an else 1-pa;ok=pw>.5;sh=1 if ep.startswith("Kick") else 0
        hit+=ok;br+=(1-pw)**2;tot[sh]+=1;hs[sh]+=ok
        if worst is None or pw<worst[0]:worst=(pw,w,bn if w==an else an)
        rows.append("| %s | %s vs %s | %s | %.0f%% | %s |"%(ep,an,bn,w,pw*100,"yes" if ok else "no"))
    n=len(FI)
    return f"""### 3.1 Case studies: documented fights
{n} fights with a clear winner in published recaps were compared with the model. For each fight, P(A wins) = 1 / (1 + exp(−(mean rating A − mean rating B) / 1.5)).

| Episode | Fight | Winner | Model P(winner) | Called? |
|---|---|---|---|---|
{chr(10).join(rows)}

The model called {hit} of {n} winners with a mean Brier score of {br/n:.2f} (a coin flip scores 0.25; lower is better). By show: {hs[0]} of {tot[0]} for *Cobra Kai* fights and {hs[1]} of {tot[1]} for *Kickin’ It* fights. The biggest miss is {worst[1]} over {worst[2]} (the model gave the winner {worst[0]*100:.0f}%). See `fight_examples.png`, and `fights.json` for the data.

**How these were analyzed.** Outcomes and key moments come from published recaps, plot summaries and some fan wikis, paraphrased here. No footage was measured. Fight results are scripted, so this tests whether the ratings track the story, not real combat. The ratings were set with knowledge of these outcomes, so this is not a blind test. Sixteen fights is a small sample, and only three are from *Kickin’ It* because its recaps rarely name winners. Some fights are group brawls, one outcome is implied by the tournament bracket, and one match (Jack vs Eddie in S1E5) was left out because it ended in a forfeit.

**Sources:** [Looper](https://looper.com/249279/why-cobra-kai-fans-have-a-problem-with-the-season-1-finale), [TV Tropes S1E10](https://tvtropes.org/pmwiki/pmwiki.php/Recap/CobraKaiS1E10Mercy), [TV Tropes S4E9](https://tvtropes.org/pmwiki/pmwiki.php/Recap/CobraKaiS4E9TheFall), [IMDb S4E10](https://imdb.com/title/tt14443266/plotsummary), [TV Acute S4E10](https://www.tvacute.com/cobra-kai-season-4-episode-10-recap), [The Cinemaholic](https://thecinemaholic.com/who-wins-the-boys-competition-in-cobra-kai-season-4-spoiler), [Screen Rant](https://screenrant.com/cobra-kai-season-4-ending-explained/), [SlashFilm](https://www.slashfilm.com/1770788/cobra-kai-season-6-part-3-sekai-taikai-tournament-winners), [Heroes Wiki](https://hero.fandom.com/wiki/Robby_Keene), [Antagonists Wiki](https://antagonists.fandom.com/wiki/Johnny_Lawrence), [Karate Kid Wiki (Demetri)](https://thekaratekid.fandom.com/wiki/Demetri_Alexopoulos), [Karate Kid Wiki (Bert)](https://thekaratekid.fandom.com/wiki/Bert), [Wikipedia Kickin’ It episodes](https://en.wikipedia.org/wiki/List_of_Kickin%27_It_episodes), [Kickin’ It Wiki](https://disneyskickinit.fandom.com/wiki/Swords_and_Magic).

"""
import unicodedata
def slug(n):return re.sub(r"[^a-z0-9]+","_",unicodedata.normalize("NFKD",n).encode("ascii","ignore").decode().lower()).strip("_")
[os.remove(OUT+'/'+f) for f in os.listdir(OUT) if f.endswith('.png')]
for m in M:fig_char(m,"%s/%s.png"%(OUT,slug(m["name"])))
fig_match();fig_roster();fig_fights()
# README
def av(sh,k):return np.mean([m[k] for m in M if m["sh"]==sh])
top=sorted(M,key=lambda m:-m["impn"])[:3];bst=sorted(M,key=lambda m:-m["bal"])[:3];gr=sorted(M,key=lambda m:-(m["s1"]-m["s0"]))[:3]
tab="\n".join("| %s | %s | %.0f | %.1f | %.0f | %.0f | %.0f | +%d |"%(m["name"],SHOW[m["sh"]],m["toeh"],m["vf"],m["impn"],m["bal"],m["eff"],m["s1"]-m["s0"]) for m in sorted(M,key=lambda m:-m["impn"]))
R="""# Estimated Kick Biomechanics of Cobra Kai and Kickin’ It Fighters
### A rating-driven kinematic model of 28 fictional karate characters

## Abstract
We build a simple planar (side-view) biomechanical model for 28 characters from *Cobra Kai* (n = 19) and *Kickin’ It* (n = 9). Each character’s six editorial skill ratings (technique, speed, power, strategy, discipline, resolve) are mapped to joint angles, a kinetic-chain timing profile, an estimated peak foot speed, an impact index and a balance index. The Cobra Kai roster averages a higher foot speed (%.1f vs %.1f m/s) and impact index (%.0f vs %.0f) than the Kickin’ It roster. The highest impact scores belong to %s. **These results follow from the mapping we chose and are not measurements.** The project is a visualization and a teaching toy, not a validated model.

## 1. Introduction
Both shows treat karate as central, but they portray it very differently: one as a drama with trained performers and long fight takes, the other as a family sitcom. The goal here is to put the two casts in the same quantitative frame by using the language of biomechanics: segment angles, centre of mass (COM), and proximal-to-distal sequencing in a kick.

## 2. Methods
### 2.1 Subjects and inputs
Each character has six ratings from 1 to 10 plus a "starting" and "peak" skill rating. All ratings are the author’s editorial judgments from general knowledge of the series. No footage was measured and no external dataset was used. Strategy and resolve are shown for context but are not used by the kick model.

### 2.2 Model
A 12-segment planar skeleton (head, trunk, two upper arms, two forearm+hand segments, two thighs, two shanks, two feet) is drawn at normalized body height (H = 1). Segment lengths use conventional anthropometric proportions (thigh 0.245 H, shank 0.246 H, upper arm 0.186 H, trunk 0.288 H). The pose is a front-leg kick from a single support leg. The COM uses Dempster-type segment mass fractions. These constants are textbook-style approximations and should be checked before any serious use.

| Quantity | Mapping |
|---|---|
| Hip flexion φ | 55 + 8 · technique (degrees) |
| Knee extension at impact | min(180, 118 + 6.2 · technique) (degrees) |
| Trunk lean | 6 + 0.22 (φ − 55) + 1.8 (10 − discipline) (degrees) |
| Peak foot speed v | 4.5 + 0.7 · speed + 0.3 · technique (m/s) |
| Impact index | (0.5 + 0.1 · power) · v², rescaled so the roster maximum is 100 |
| Chain peak lag Δ | 10 + 3.5 · technique (ms) between hip, knee and ankle peaks |
| Chain efficiency | 100 · (0.35 + 0.065 · technique) (percent) |
| Balance index | 100 · (1 − distance of COM from centre of support foot / 0.145 H), floored at 0 |

Joint angular velocities are drawn as Gaussian pulses (σ = 20 ms). Hip, knee and ankle peaks are separated by Δ, so a low-technique fighter shows overlapping peaks (poor sequencing).

## 3. Results
| Fighter | Show | Toe height (%% H) | Foot speed (m/s) | Impact | Balance | Chain eff. (%%) | Growth |
|---|---|---|---|---|---|---|---|
%s

**Roster means.** Foot speed %.1f (Cobra Kai) vs %.1f (Kickin’ It). Impact %.0f vs %.0f. Balance %.0f vs %.0f. Chain efficiency %.0f%% vs %.0f%%.

**Highlights.** Highest impact: %s. Best balance: %s. Biggest rated growth: %s.

Figures: `summary_matchups.png` (ten head-to-head models), `summary_roster.png` (speed vs impact for all 28), and one panel per fighter (`<name>.png`).

## 4. Discussion
The model largely re-expresses the ratings: technique drives pose and sequencing, speed and technique drive foot speed, and power scales impact. Correlations between ratings and outputs are therefore built in and should not be read as findings about the shows. The more useful outputs are the cross-roster comparisons and the balance index, which comes from the pose geometry (kick height and lean) and so is not a direct copy of any single rating.

## 5. Limitations
- Ratings are subjective, and the characters are fictional. Fight scenes are performed by actors and stunt performers.
- The model is 2D, uses one kick type, and ignores arm contribution to power, ground reaction forces and opponent contact.
- Foot speeds and indices are illustrative units. They are not validated against motion capture or published kicking data.
- Segment constants are approximations from general knowledge, not checked against a source for this project.

## 6. Reproducibility
`bio.py` regenerates every figure from the character data in the dashboard (`karate-showdown.html`). Changing a rating there and rerunning updates all outputs.
""" % (av(0,"vf"),av(1,"vf"),av(0,"impn"),av(1,"impn"),", ".join(m["name"] for m in top),tab,av(0,"vf"),av(1,"vf"),av(0,"impn"),av(1,"impn"),av(0,"bal"),av(1,"bal"),av(0,"eff"),av(1,"eff"),", ".join("%s (%.0f)"%(m["name"],m["impn"]) for m in top),", ".join("%s (%.0f)"%(m["name"],m["bal"]) for m in bst),", ".join("%s (+%d)"%(m["name"],m["s1"]-m["s0"]) for m in gr))
R=R.replace("## 4. Discussion",extra()+"## 4. Discussion");open(OUT+"/README.md","w",encoding="utf-8").write(R)
shutil.copy("/home/claude/bio.py",OUT+"/bio.py");shutil.copy("/home/claude/fights.json",OUT+"/fights.json")
shutil.make_archive("/mnt/user-data/outputs/biomechanics_models","zip",OUT)
print(len(M),sorted(os.listdir(OUT))[:5],len(os.listdir(OUT)))
