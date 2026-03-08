# Part C — Interview Answers

---

## Q1 — Tuple Immutability Trap

**The code in question:**
```python
t = ([1, 2], [3, 4])
t[0][0] = 99
```

**Does it work?**
Yes, it works without any error. After running it, `t` becomes `([99, 2], [3, 4])`.

**Why does it work, even though tuples are immutable?**

The tuple `t` holds references to two list objects, not the values directly. Tuple immutability means you cannot change which objects the tuple points to — you cannot do `t[0] = something_else`. However, the list object that `t[0]` points to is mutable. So you can modify the contents of that list freely. The tuple's reference to the list never changed; only the list's internal content changed.

Think of it this way: the tuple is like a sealed box with two address labels pointing to two houses. You cannot swap the address labels (that would be changing the tuple). But you can walk into the house (the list) and rearrange the furniture inside.

**What this reveals about tuple immutability:**

Tuple immutability is shallow. The tuple only guarantees that its own slots — the references it holds — cannot be reassigned. It says nothing about what those references point to. If they point to mutable objects like lists or dicts, those objects remain fully mutable. This is a classic Python interview trap because most people assume "immutable tuple" means "nothing inside can change," which is incorrect.

---

## Q2 — Duplicate Detection Using Sets

**Function:**
```python
def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return duplicates
```

**How it works:**

We use two sets: `seen` tracks elements encountered so far, `duplicates` collects elements we encounter a second time. One pass through the list gives us all duplicates. No Counter, no nested loops.

**Time Complexity:** O(n) — single loop, and set lookup/insert are O(1) on average.

**Example:**
```python
find_duplicates([1, 2, 3, 2, 4, 1, 5])
# Returns: {1, 2}

find_duplicates(['a', 'b', 'a', 'c', 'b', 'b'])
# Returns: {'a', 'b'}
```

---

## Q3 — Debug Problem

**The buggy function:**
```python
def unique_to_each(a, b):
    result = set(a) - set(b)
    return list(result)
```

**Test:**
```python
unique_to_each([1, 2, 3], [3, 4, 5])
# Returns: [1, 2]   (wrong — expected [1, 2, 4, 5])
```

**Why the bug happens:**

`set(a) - set(b)` only returns elements that are in `a` but not in `b`. It completely ignores elements that are in `b` but not in `a` — so `4` and `5` never show up. The operation needed here is symmetric difference (elements unique to either side), not one-sided difference.

**Fixed function:**
```python
def unique_to_each(a, b):
    result = set(a).symmetric_difference(set(b))
    return list(result)

# Or equivalently using the ^ operator:
def unique_to_each(a, b):
    return list(set(a) ^ set(b))
```

**Verification:**
```python
unique_to_each([1, 2, 3], [3, 4, 5])
# Returns: [1, 2, 4, 5]   correct
```

The `^` operator (symmetric difference) returns elements that are in either set but not in both — which is exactly "unique to each."
