def rule_based(score, documents_complete, eligible, deadline_met):
    """Check an application using four clear conditions."""
    if documents_complete and score >= 70 and eligible and deadline_met:
        return "Review"
    return "Hold"

cases = [
    {
        "name": "Pass",
        "score": 80,
        "documents_complete": True,
        "eligible": True,
        "deadline_met": True,
        "expected": "Review",
        "reason": "All four conditions are satisfied."
    },
    {
        "name": "Eligibility failure",
        "score": 80,
        "documents_complete": True,
        "eligible": False,
        "deadline_met": True,
        "expected": "Hold",
        "reason": "The student does not meet the eligibility condition."
    },
    {
        "name": "Deadline failure",
        "score": 80,
        "documents_complete": True,
        "eligible": True,
        "deadline_met": False,
        "expected": "Hold",
        "reason": "The application was not submitted by the deadline."
    },
    {
        "name": "Threshold boundary",
        "score": 70,
        "documents_complete": True,
        "eligible": True,
        "deadline_met": True,
        "expected": "Review",
        "reason": "A score of exactly 70 meets the score >= 70 rule."
    }
]

print("Modified scholarship screening rules")
print("Threshold: score >= 70 (a synthetic lab assumption)")
print("-" * 100)

for case in cases:
    actual = rule_based(
        case["score"],
        case["documents_complete"],
        case["eligible"],
        case["deadline_met"]
    )

    print("Case:", case["name"])
    print(
        "Input: score =", case["score"],
        ", documents_complete =", case["documents_complete"],
        ", eligible =", case["eligible"],
        ", deadline_met =", case["deadline_met"]
    )
    print("Expected result:", case["expected"])
    print("Actual result:  ", actual)
    print("Reason:", case["reason"])
    print("Test passed:", actual == case["expected"])
    print("-" * 100)
