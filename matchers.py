"""Exact string matchers with zero-based positions and overlapping matches."""

from dataclasses import dataclass


@dataclass
class MatchResult:
    positions: list[int]
    comparisons: int = 0
    lookups: int | None = None
    spurious_hits: int | None = None


def naive_match(text, pattern):
    result = MatchResult([])
    for start in range(len(text) - len(pattern) + 1):
        for index, character in enumerate(pattern):
            result.comparisons += 1
            if text[start + index] != character:
                break
        else:
            result.positions.append(start)
    return result


def rabin_karp_setup(pattern, base=256, modulus=101):
    pattern_hash = 0
    for character in pattern:
        pattern_hash = (base * pattern_hash + ord(character)) % modulus
    high_digit = pow(base, max(0, len(pattern) - 1), modulus)
    return pattern_hash, high_digit


def rabin_karp_match(text, pattern, setup, base=256, modulus=101):
    result = MatchResult([], spurious_hits=0)
    width = len(pattern)
    if width == 0:
        result.positions = list(range(len(text) + 1))
        return result
    if width > len(text):
        return result

    pattern_hash, high_digit = setup
    window_hash = 0
    for index in range(width):
        window_hash = (base * window_hash + ord(text[index])) % modulus

    # Verify matching hashes before recording a position.
    last_start = len(text) - width
    for start in range(last_start + 1):
        if window_hash == pattern_hash:
            for index, character in enumerate(pattern):
                result.comparisons += 1
                if text[start + index] != character:
                    result.spurious_hits += 1
                    break
            else:
                result.positions.append(start)

        if start < last_start:
            outgoing = ord(text[start]) * high_digit
            incoming = ord(text[start + width])
            window_hash = (base * (window_hash - outgoing) + incoming) % modulus
    return result


def prefix_table(pattern):
    table = [0] * len(pattern)
    matched = 0
    for index in range(1, len(pattern)):
        while matched > 0 and pattern[index] != pattern[matched]:
            matched = table[matched - 1]
        if pattern[index] == pattern[matched]:
            matched += 1
        table[index] = matched
    return table


def kmp_match(text, pattern, table):
    if not pattern:
        return MatchResult(list(range(len(text) + 1)))

    result = MatchResult([])
    matched = 0
    for index, character in enumerate(text):
        # Try shorter prefixes until this character matches or no prefix remains.
        while True:
            result.comparisons += 1
            if character == pattern[matched]:
                matched += 1
                break
            if matched == 0:
                break
            matched = table[matched - 1]

        if matched == len(pattern):
            result.positions.append(index - len(pattern) + 1)
            matched = table[matched - 1]
    return result


def transition_table(pattern):
    if not pattern:
        return [{}]

    alphabet = set(pattern)
    table = [dict.fromkeys(alphabet, 0)]
    table[0][pattern[0]] = 1
    fallback = 0

    # Reuse the transitions from the longest proper prefix that is also a suffix.
    for state in range(1, len(pattern)):
        row = table[fallback].copy()
        character = pattern[state]
        fallback = row[character]
        row[character] = state + 1
        table.append(row)
    table.append(table[fallback].copy())
    return table


def automata_match(text, pattern, table):
    result = MatchResult([], lookups=len(text))
    state = 0
    width = len(pattern)
    if width == 0:
        result.positions.append(0)

    for index, character in enumerate(text):
        state = table[state].get(character, 0)
        if state == width:
            result.positions.append(index - width + 1)
    return result
