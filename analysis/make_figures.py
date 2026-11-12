"""
Figures for the verification-theater experiment, drawn from SIMULATED data.
They show that the analysis pipeline runs end to end; they are not findings.
  Fig 1  Trust in the AI by citation condition (H1, H2)
  Fig 2  Adoption of the incorrect recommendation (H3)
  Fig 3  Perceived verifiability and source clicks
"""
NOTE = "Simulated data for pipeline validation. Not participant results."
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
ax.set_title("Trust in the AI by citation condition (simulated data)",fontweight="bold",fontsize=12)
fig.text(0.5,0.01,NOTE,ha="center",fontsize=8.5,color="#555",style="italic")
plt.tight_layout(rect=(0,0.04,1,1)); plt.savefig("analysis/fig1_trust.png",dpi=150); plt.close()

# ---- Fig 2: Adoption of wrong rec ----
fig,ax=plt.subplots(figsize=(6,4.2))
rates=[adopt[m].mean() for m in masks]
se=[np.sqrt(r*(1-r)/m.sum()) for r,m in zip(rates,masks)]
ax.bar(labels,[r*100 for r in rates],yerr=[s*100 for s in se],capsize=5,
       color=colors,edgecolor="black",linewidth=0.6)
ax.set_ylabel("Adopted the incorrect recommendation (%)"); ax.set_ylim(0,80)
ax.set_title("Adoption of the incorrect recommendation (simulated data)",fontweight="bold",fontsize=12)
ax.axhline(50,ls="--",color="#aaa",lw=0.8)
for i,r in enumerate(rates): ax.text(i,r*100+2,f"{r*100:.0f}%",ha="center",fontweight="bold")
fig.text(0.5,0.01,NOTE,ha="center",fontsize=8.5,color="#555",style="italic")
plt.tight_layout(rect=(0,0.04,1,1)); plt.savefig("analysis/fig2_adoption.png",dpi=150); plt.close()

# ---- Fig 3: perceived verifiability + click-through ----
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(9,4.2))
vmeans=[m_se(verif,m)[0] for m in masks]; vses=[m_se(verif,m)[1] for m in masks]
ax1.bar(labels,vmeans,yerr=vses,capsize=5,color=colors,edgecolor="black",linewidth=0.6)
ax1.set_ylabel("Perceived verifiability (1–7)"); ax1.set_ylim(0,7)
ax1.set_title("Perceived verifiability",fontweight="bold",fontsize=11)
crates=[click[m].mean() for m in masks]
ax2.bar(labels,[c*100 for c in crates],color=colors,edgecolor="black",linewidth=0.6)
ax2.set_ylabel("Clicked a source (%)"); ax2.set_ylim(0,60)
ax2.set_title("Source clicks",fontweight="bold",fontsize=11)
for i,c in enumerate(crates): ax2.text(i,c*100+1.5,f"{c*100:.0f}%",ha="center",fontweight="bold")
fig.suptitle("Perceived verifiability and source clicks (simulated data)",fontsize=13,fontweight="bold")
fig.text(0.5,0.01,NOTE,ha="center",fontsize=8.5,color="#555",style="italic")
plt.tight_layout(rect=(0,0.04,1,1)); plt.savefig("analysis/fig3_verification.png",dpi=150); plt.close()
print("Saved fig1_trust.png, fig2_adoption.png, fig3_verification.png")
