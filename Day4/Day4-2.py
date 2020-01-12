
def is_possible_password(value):
    s = str(value)

    t = 1
    has_doubles = 0

    for i in range(1, len(s)):
        if s[i] < s[i-1]:
            return 0

        if s[i] == s[i-1]:
            t += 1
        else:
            if t == 2:
                has_doubles = 1
            t = 1

    if t == 2:
        has_doubles = 1

    return has_doubles


print(sum(map(is_possible_password, range(254032, 789860))))
