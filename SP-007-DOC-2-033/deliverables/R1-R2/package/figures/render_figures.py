#!/usr/bin/env python3
"""Deterministically render the two package figures from frozen JSON only.
No scientific scoring, filtering, ranking, inference, or new analysis.
Requires matplotlib 3.10.9. Run from any directory.
"""
import hashlib, json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "frozen", "deliverables", "results")
OUT = os.path.join(ROOT, "figures")
def sha(path):
    with open(path, "rb") as fh: return hashlib.sha256(fh.read()).hexdigest()
def card_counts():
    src=os.path.join(RESULTS,"review_queue_summary.json"); d=json.load(open(src,encoding="utf-8"))
    vals=[d["classes"]["perturbation-supported"],d["classes"]["association-only_total"],d["classes"]["reference-discordant"]]
    labs=["Perturbation-supported","Association-only","Reference-discordant"]
    fig,ax=plt.subplots(figsize=(8,4.5)); ax.bar(labs,vals,color=["#315b91","#769ac5","#b9cae1"])
    ax.set_ylabel("Frozen card count"); ax.set_title("R1 frozen review-card classes"); ax.spines[["top","right"]].set_visible(False)
    for i,v in enumerate(vals): ax.text(i,v+max(vals)*.015,f"{v:,}",ha="center",fontsize=10)
    fig.text(.01,.01,"Source SHA-256: "+sha(src),fontsize=6); fig.tight_layout(rect=(0,.04,1,1))
    fig.savefig(os.path.join(OUT,"r1_card_counts.png"),dpi=180,metadata={"SourceSHA256":sha(src)})
    plt.close(fig); open(os.path.join(OUT,"r1_card_counts.SOURCE.sha256"),"w",encoding="utf-8").write(sha(src)+"  frozen/deliverables/results/review_queue_summary.json\n")
def transport():
    src=os.path.join(RESULTS,"r2_transport_evaluation.json"); d=json.load(open(src,encoding="utf-8"))
    labels=["Sign agreement","Rank correlation","Supported precision"]
    values=[d["sign_agreement"]["value"],d["rank_correlation_median"]["value"],d["supported_overlap"]["precision_mean"]]
    nulls=[d["sign_agreement"]["target_permuted_null_p95"],d["rank_correlation_median"]["target_permuted_null_p95"],d["supported_overlap"]["target_permuted_null_precision_p95"]]
    fig,axs=plt.subplots(1,3,figsize=(9,3.6))
    for ax,lab,v,n in zip(axs,labels,values,nulls):
        ax.bar(["Observed","Null p95"],[v,n],color=["#315b91","#b9cae1"]); ax.set_title(lab,fontsize=9); ax.set_ylim(0,max(v,n)*1.25); ax.spines[["top","right"]].set_visible(False)
        for i,x in enumerate([v,n]): ax.text(i,x+max(v,n)*.03,f"{x:.4f}",ha="center",fontsize=8)
    fig.suptitle("R2 cross-cell-line transport metrics (frozen)"); fig.text(.01,.01,"Source SHA-256: "+sha(src),fontsize=6); fig.tight_layout(rect=(0,.05,1,.93))
    fig.savefig(os.path.join(OUT,"r2_transport_metrics.png"),dpi=180,metadata={"SourceSHA256":sha(src)})
    plt.close(fig); open(os.path.join(OUT,"r2_transport_metrics.SOURCE.sha256"),"w",encoding="utf-8").write(sha(src)+"  frozen/deliverables/results/r2_transport_evaluation.json\n")
if __name__=="__main__": card_counts(); transport()
