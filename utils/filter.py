def is_target_role(title: str) -> bool:
    title = title.lower()

    internship_keywords = [
        "intern", "internship", "trainee", "attachment"
    ]

    junior_keywords = [
        "junior", "entry", "graduate", "associate", "fresh"
    ]

    for word in internship_keywords + junior_keywords:
        if word in title:
            return True

    return False
