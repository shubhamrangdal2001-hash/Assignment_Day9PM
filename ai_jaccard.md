# Part D — AI-Augmented Task: Jaccard Similarity

---

## Step 1: Exact Prompt Used

> "Write a Python function that calculates the Jaccard similarity between two sets of strings. Explain what Jaccard similarity is and where it is used in industry."

---

## Step 2: AI-Generated Output

**Explanation from AI:**
Jaccard similarity is a metric that measures how similar two sets are. It is calculated as the size of the intersection divided by the size of the union of the two sets. The result is always between 0 (completely different) and 1 (identical).

Formula: `J(A, B) = |A ∩ B| / |A ∪ B|`

**AI-generated code:**
```python
def jaccard_similarity(set_a, set_b):
    intersection = set_a & set_b
    union = set_a | set_b
    if len(union) == 0:
        return 0.0
    return len(intersection) / len(union)
```

---

## Step 3: Testing the AI Code

**Test 1:**
```python
set_a = {'python', 'java', 'sql'}
set_b = {'python', 'sql', 'docker', 'aws'}

jaccard_similarity(set_a, set_b)
# intersection: {'python', 'sql'}  -> size 2
# union: {'python','java','sql','docker','aws'} -> size 5
# Result: 2/5 = 0.4
```
Output: `0.4` — correct.

**Test 2 (edge case — empty sets):**
```python
jaccard_similarity(set(), set())
# union is empty -> returns 0.0 (handled correctly)
```
Output: `0.0` — handled correctly.

**Is the formula correct?** Yes. The AI used the standard definition: `|intersection| / |union|`.

**Does it handle edge cases?** Yes, the `if len(union) == 0` guard prevents division by zero when both sets are empty.

One small thing I noticed: if `set_a` is empty but `set_b` is not, the function still works correctly (returns 0.0), which is the right answer mathematically since intersection is empty.

---

## Industry Use Cases for Jaccard Similarity

Jaccard similarity is widely used in recommendation systems to measure overlap between users' purchase or viewing histories — two users with high Jaccard similarity are likely to enjoy the same products. In natural language processing, it is applied to measure document or sentence similarity by treating each document as a bag of words or shingles. Plagiarism detection tools use Jaccard similarity to compare sets of word sequences (n-grams) between documents and flag those with high overlap. It also appears in e-commerce deduplication pipelines to identify near-duplicate product listings by comparing sets of product attributes or description tokens.

---

## Improved Version

The AI code is already clean and correct. I made two small additions: a docstring and a check that raises an error if non-set types are passed.

```python
def jaccard_similarity(set_a, set_b):
    """
    Returns Jaccard similarity between two sets.
    Range: 0.0 (no overlap) to 1.0 (identical).
    """
    if not isinstance(set_a, set) or not isinstance(set_b, set):
        raise TypeError("Both inputs must be sets.")
    intersection = set_a & set_b
    union = set_a | set_b
    if len(union) == 0:
        return 0.0
    return round(len(intersection) / len(union), 4)


# Demo
if __name__ == "__main__":
    set_a = {'python', 'java', 'sql'}
    set_b = {'python', 'sql', 'docker', 'aws'}
    print(jaccard_similarity(set_a, set_b))   # 0.4

    # Identical sets
    print(jaccard_similarity({'a', 'b'}, {'a', 'b'}))  # 1.0

    # No overlap
    print(jaccard_similarity({'a', 'b'}, {'c', 'd'}))  # 0.0

    # Both empty
    print(jaccard_similarity(set(), set()))             # 0.0
```
