
def rule_based(score, documents_complete):
    """Decide whether an application should be reviewed using fixed rules."""
    if documents_complete and score >= 70:
        return "Review"
    return "Hold"


def probability_based(probability):
    """Flag an application for review when its probability is at least 0.70."""
    if probability >= 0.70:
        return "Review"
    return "Hold"


print("Rule-based and probability-based comparison")
print("-" * 58)

cases = [
    ("complete_high", 82, True, 0.81),
    ("complete_low", 68, True, 0.74),
    ("incomplete_high", 91, False, 0.88),
    ("boundary", 70, True, 0.70),
]

print("case | symbolic | threshold | disagreement")

for name, score, documents_complete, probability in cases:
    symbolic_result = rule_based(score, documents_complete)
    threshold_result = probability_based(probability)
    disagreement = symbolic_result != threshold_result

    print(
        name, "|", symbolic_result, "|",
        threshold_result, "|", disagreement
    )
