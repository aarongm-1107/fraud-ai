def grade(action, correct):
    if action == correct:
        return 1.0
    elif action == "flag":
        return 0.3  
    else:
        return -1.0  