#!/usr/bin/env python3
import random


def main():
    random.seed()
    # TODO: generate input for this problem.


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import random

T = 1
L = random.randint(5, 30)
n = random.randint(1, 8)
m = random.randint(1, min(8, L + 1))
V = random.randint(1, 8)

print(T)
print(n, m, L, V)

for _ in range(n):
    d = random.randint(0, L - 1)
    v = random.randint(1, 8)
    a = random.randint(-5, 5)
    print(d, v, a)

positions = sorted(random.sample(range(0, L + 1), m))
print(*positions)
