# String Matching Benchmarking Engine

A Python-based pattern-matching engine that runs Naive, Rabin-Karp, Finite Automata, and Knuth-Morris-Pratt algorithms on strings to identify pre-defined substrings and benchmarks their performance.

Run the interactive CLI with Python 3.10 or newer. It uses only the standard library.

```sh
python main.py
```

The engine runs Naive, Rabin-Karp, Finite Automata, or Knuth-Morris-Pratt. Choose **Run and benchmark all** to compare them on the same input, or **Benchmark a random demo** to try all four on a built-in example.

Runtime prompts are the default. To use a file, select the file input option in **Settings** and create a text file named exactly `input.txt` next to `main.py`.

Use one line for each value in the text file:
```text
T=bananabananabandana
P=banana
```

Matching is case-sensitive and includes overlapping matches. Positions are zero-based. Spaces and any additional equals signs after the first equals sign are part of the value. Empty values are accepted. An empty pattern matches at every text boundary.

The benchmark ranks algorithms by total time, including preprocessing. It reports preprocessing and search time separately and calculates throughput in text characters per search second. The comparison count includes text-to-pattern comparisons during search. Finite Automata reports table lookups, and Rabin-Karp reports hash hits rejected during verification.
