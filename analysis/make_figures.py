"""
Figures for the verification-theater experiment (from simulated data).
Three panels map onto the three core findings:
  Fig 1  Trust:  H1 (cites > none) + H2 (fake ~ real)  -> "the theater works"
  Fig 2  Adoption of the wrong recommendation: H3       -> "the cost"
  Fig 3  Perceived verifiability + actual click-through  -> "verifiable != verified"
"""
import csv, numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# load
cond, trust, verif, adopt, click = [], [], [], [], []
with open("data/simulated_data.csv") as f:
    for row in csv.DictReader(f):
        cond.append(row["condition"]); trust.append(float(row["trust"]))
        verif.append(float(row["perceived_verif"])); adopt.append(int(row["adopt_wrong"]))
        click.append(int(row["clicked_source"]))
cond=np.array(cond); trust=np.array(trust); verif=np.array(verif)
adopt=np.array(adopt); click=np.array(click)
order=["C1_none","C2_fake","C3_real"]
labels=["No citation","Fake citation\n(unverifiable)","Real citation\n(verifiable)"]
colors=["#9aa5b1","#e07a5f","#3d5a80"]

def m_se(x, mask):
    v=x[mask]; return v.mean(), v.std(ddof=1)/np.sqrt(len(v))
masks=[cond==c for c in order]

plt.rcParams.update({"font.size":11,"axes.spines.top":False,"axes.spines.right":False})

# ---- Fig 1: Trust ----
fig,ax=plt.subplots(figsize=(6,4.2))
means=[m_se(trust,m)[0] for m in masks]; ses=[m_se(trust,m)[1] for m in masks]
bars=ax.bar(labels,means,yerr=ses,capsize=5,color=colors,edgecolor="black",linewidth=0.6)
ax.set_ylabel("Trust in AI (1–7)"); ax.set_ylim(0,7)
ax.set_title("Trust: fake citations work as well as real ones",fontweight="bold",fontsize=12)
# annotate H2 (fake vs real = ns)
y=max(means[1],means[2])+0.6
ax.plot([1,2],[y,y],color="black",lw=1)
ax.text(1.5,y+0.05,"n.s. (H2)",ha="center",fontsize=10,style="italic")
ax.annotate("H1: citations lift trust",xy=(0.5,means[0]+0.3),fontsize=9,color="#555")
plt.tight_layout(); plt.savefig("analysis/fig1_trust.png",dpi=150); plt.close()

# ---- Fig 2: Adoption of wrong rec ----
fig,ax=plt.subplots(figsize=(6,4.2))
rates=[adopt[m].mean() for m in masks]
se=[np.sqrt(r*(1-r)/m.sum()) for r,m in zip(rates,masks)]
ax.bar(labels,[r*100 for r in rates],yerr=[s*100 for s in se],capsize=5,
       color=colors,edgecolor="black",linewidth=0.6)
ax.set_ylabel("Adopted the WRONG recommendation (%)"); ax.set_ylim(0,80)
ax.set_title("The cost: fake citations drive the most bad decisions",fontweight="bold",fontsize=12)
ax.axhline(50,ls="--",color="#aaa",lw=0.8)
for i,r in enumerate(rates): ax.text(i,r*100+2,f"{r*100:.0f}%",ha="center",fontweight="bold")
plt.tight_layout(); plt.savefig("analysis/fig2_adoption.png",dpi=150); plt.close()

# ---- Fig 3: perceived verifiability + click-through ----
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(9,4.2))
vmeans=[m_se(verif,m)[0] for m in masks]; vses=[m_se(verif,m)[1] for m in masks]
ax1.bar(labels,vmeans,yerr=vses,capsize=5,color=colors,edgecolor="black",linewidth=0.6)
ax1.set_ylabel("Perceived verifiability (1–7)"); ax1.set_ylim(0,7)
ax1.set_title("Fake sources feel checkable",fontweight="bold",fontsize=11)
crates=[click[m].mean() for m in masks]
ax2.bar(labels,[c*100 for c in crates],color=colors,edgecolor="black",linewidth=0.6)
ax2.set_ylabel("Actually clicked the source (%)"); ax2.set_ylim(0,60)
ax2.set_title("But almost nobody checks",fontweight="bold",fontsize=11)
for i,c in enumerate(crates): ax2.text(i,c*100+1.5,f"{c*100:.0f}%",ha="center",fontweight="bold")
fig.suptitle("Verifiable ≠ verified",fontsize=13,fontweight="bold")
plt.tight_layout(); plt.savefig("analysis/fig3_verification.png",dpi=150); plt.close()
print("Saved fig1_trust.png, fig2_adoption.png, fig3_verification.png")
