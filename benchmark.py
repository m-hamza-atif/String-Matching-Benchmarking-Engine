"""Benchmark timing and terminal output."""

from dataclasses import dataclass
from time import perf_counter_ns

from matchers import (
    MatchResult,
    automata_match,
    kmp_match,
    naive_match,
    prefix_table,
    rabin_karp_match,
    rabin_karp_setup,
    transition_table,
)


ALGORITHMS = {
    "1": ("Naive", naive_match, None),
    "2": ("Rabin-Karp", rabin_karp_match, rabin_karp_setup),
    "3": ("Finite Automata", automata_match, transition_table),
    "4": ("Knuth-Morris-Pratt", kmp_match, prefix_table),
}


@dataclass
class Benchmark:
    name: str
    result: MatchResult
    setup_ns: int
    search_ns: int

    @property
    def total_ns(self):
        return self.setup_ns + self.search_ns


def benchmark(algorithm, text, pattern):
    name, search, prepare = algorithm
    setup_ns = 0
    if prepare is None:
        start = perf_counter_ns()
        result = search(text, pattern)
    else:
        start = perf_counter_ns()
        prepared = prepare(pattern)
        setup_ns = perf_counter_ns() - start

        start = perf_counter_ns()
        result = search(text, pattern, prepared)
    search_ns = perf_counter_ns() - start
    return Benchmark(name, result, setup_ns, search_ns)


def print_results(benchmarks, text_length, pattern_length):
    ranked = sorted(benchmarks, key=lambda row: row.total_ns)
    print(f"\nText length: {text_length:,} | Pattern length: {pattern_length:,}")
    print(
        f"{'Algorithm':<19} {'Matches':>9} {'Comparisons':>12} {'Lookups':>9} "
        f"{'Prep (ms)':>11} {'Search (ms)':>12} {'Total (ms)':>11} {'Chars/s':>15}"
    )
    for row in ranked:
        result = row.result
        lookups = "-" if result.lookups is None else f"{result.lookups:,}"
        throughput = f"{text_length * 1_000_000_000 / row.search_ns:,.0f}" if row.search_ns else "-"
        print(
            f"{row.name:<19} {len(result.positions):>9,} {result.comparisons:>12,} "
            f"{lookups:>9} {row.setup_ns / 1e6:>11.6f} {row.search_ns / 1e6:>12.6f} "
            f"{row.total_ns / 1e6:>11.6f} {throughput:>15}"
        )

    print("\nComparisons and lookups count search work. Chars/s uses search time.")
    if len(ranked) > 1:
        print("Ranked by total time (preprocessing + search).")

    # Show a shared list when every matcher found the same positions.
    positions = ranked[0].result.positions
    if all(row.result.positions == positions for row in ranked):
        print(f"Match positions (zero-based): {positions}")
    else:
        for row in ranked:
            print(f"{row.name} positions (zero-based): {row.result.positions}")

    for row in ranked:
        if row.result.spurious_hits is not None:
            print(f"Rabin-Karp spurious hits: {row.result.spurious_hits:,}")
