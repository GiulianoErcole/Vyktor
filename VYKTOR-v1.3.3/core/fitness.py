import math

DEFAULT_PROFILE = {
    "accuracy": 0.5,
    "efficiency": 0.3,
    "entropy": 0.1,
    "stability": 0.1
}

def _safe(v, lo=0.0, hi=1.0):
    try:
        x = float(v)
    except Exception:
        x = 0.0
    return max(lo, min(hi, x))

def combine(metrics: dict, profile: dict | None = None) -> float:
    """Combine a metrics dict into a single fitness score in [0,1].
    Expected metrics keys (fallbacks applied):
    - ok (0/1) => accuracy
    - runtime (seconds) => efficiency (mapped via 1/(1+rt))
    - entropy (0..1) => entropy
    - stability (0..1)
    - length (chars) => mild length penalty mapped into stability
    """
    profile = {**DEFAULT_PROFILE, **(profile or {})}

    accuracy = _safe(metrics.get("ok", 0.0))
    rt = metrics.get("runtime", None)
    efficiency = 1.0/(1.0 + max(0.0, float(rt))) if rt is not None else 0.5

    entropy = _safe(metrics.get("entropy", 0.5))
    stability = _safe(metrics.get("stability", 0.5))

    # Small code length regularizer (discourage bloat slightly)
    length = float(metrics.get("length", 0.0) or 0.0)
    if length > 0:
        stability *= 1.0/(1.0 + 0.0005*length)

    score = (
        profile["accuracy"]  * accuracy +
        profile["efficiency"]* efficiency +
        profile["entropy"]   * entropy +
        profile["stability"] * stability
    )
    # keep inside [0,1]
    return _safe(score)
