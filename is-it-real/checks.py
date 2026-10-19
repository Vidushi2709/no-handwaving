"""Reusable checks for the is-it-real skill. numpy + scipy only; no LLM calls.

One-liners you don't need a helper for:
    Wilson CI:      scipy.stats.binomtest(k, n).proportion_ci(method="wilson")
    McNemar exact:  scipy.stats.binomtest(min(b, c), b + c).pvalue
    t-interval:     scipy.stats.t.interval(0.95, len(x) - 1, np.mean(x), scipy.stats.sem(x))
    text baseline:  make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000))
    train/test leak: set(train_keys) & set(test_keys)   # keys = ids, normalised text, or group ids
"""

import numpy as np
from scipy.stats import binomtest, rankdata


def paired(a, b, groups=None, n_boot=2000, seed=0):
    """Compare two systems scored 0/1 on the same items. a, b: aligned arrays.

    Bootstrap resamples whole groups when given (e.g. paraphrases of one request),
    otherwise single items. Returns b - a with a 95% interval and McNemar's p.
    """
    a, b = np.asarray(a, float), np.asarray(b, float)
    groups = np.arange(len(a)) if groups is None else np.asarray(groups)
    _, g = np.unique(groups, return_inverse=True)
    d = np.bincount(g, b - a)  # per-group sum of differences
    c = np.bincount(g)  # per-group item count
    idx = np.random.default_rng(seed).integers(0, len(c), (n_boot, len(c)))
    diffs = d[idx].sum(1) / c[idx].sum(1)
    b_only, a_only = int(((b == 1) & (a == 0)).sum()), int(((a == 1) & (b == 0)).sum())
    p = binomtest(min(b_only, a_only), b_only + a_only).pvalue if b_only + a_only else 1.0
    return {
        "n": len(a),
        "diff": b.mean() - a.mean(),
        "ci": tuple(np.percentile(diffs, [2.5, 97.5])),
        "b_only": b_only,
        "a_only": a_only,
        "p_mcnemar": p,
    }


def auroc(scores, y):
    """P(random positive scores above random negative), ties count half."""
    scores, y = np.asarray(scores, float), np.asarray(y, bool)
    r = rankdata(scores)
    n1, n0 = y.sum(), (~y).sum()
    return (r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def auroc_ci(scores, y, n_boot=2000, seed=0):
    """AUROC with a 95% bootstrap interval, resampling positives and negatives separately."""
    scores, y = np.asarray(scores, float), np.asarray(y, bool)
    pos, neg = scores[y], scores[~y]
    rng = np.random.default_rng(seed)
    labels = np.r_[np.ones(len(pos), bool), np.zeros(len(neg), bool)]
    boots = [
        auroc(np.r_[rng.choice(pos, len(pos)), rng.choice(neg, len(neg))], labels)
        for _ in range(n_boot)
    ]
    return auroc(scores, y), tuple(np.percentile(boots, [2.5, 97.5]))


def probe_nulls(X, y, train_idx, test_idx, n=200, seed=0):
    """Test AUROCs of directions that shouldn't work, for a difference-of-means probe.

    'random': Gaussian directions. 'shuffled': diff-of-means on shuffled train labels.
    A real probe should beat the 95th percentile of both.
    """
    X, y = np.asarray(X, float), np.asarray(y, bool)
    rng = np.random.default_rng(seed)
    Xtr, ytr, Xte, yte = X[train_idx], y[train_idx], X[test_idx], y[test_idx]
    rand = [auroc(Xte @ rng.standard_normal(X.shape[1]), yte) for _ in range(n)]
    shuf = []
    for _ in range(n):
        s = rng.permutation(ytr)
        shuf.append(auroc(Xte @ (Xtr[s].mean(0) - Xtr[~s].mean(0)), yte))
    return {"random": np.array(rand), "shuffled": np.array(shuf)}


def judge_audit(judge, pairs):
    """Feed a judge answers whose right verdict is known; count its mistakes per kind.

    judge(answer, reference) -> truthy if graded correct.
    pairs: [(reference, a_wrong_value), ...], ideally 10+ from the real data.
    """
    kinds = {
        "correct": (lambda r, w: r, True),
        "reworded": (lambda r, w: f"The answer is {r}.", True),
        "hedged": (lambda r, w: f"{r}, but I may be wrong about this.", True),
        "wrong": (lambda r, w: w, False),
        "empty": (lambda r, w: "", False),
        "refusal": (lambda r, w: "I don't know.", False),
        "no_info": (lambda r, w: "I don't have enough information to answer that.", False),
        "off_topic": (lambda r, w: "Bananas are usually yellow.", False),
    }
    out = {}
    for kind, (make, expected) in kinds.items():
        bad = [make(r, w) for r, w in pairs if bool(judge(make(r, w), r)) != expected]
        out[kind] = {"errors": len(bad), "n": len(pairs), "examples": bad[:3]}
    return out
