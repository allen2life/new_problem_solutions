#!/usr/bin/env python3
import random


def main():
    random.seed()
    # TODO: generate input for this problem.


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import random

n = random.randint(2, 8)
m = random.randint(1, 8)
k = 0
while (1 << k) < n:
    k += 1

print(n, m)
print(*[random.randint(0, 7) for _ in range(n)])
print(*[random.randint(1, n) for _ in range(m)])

for round_id in range(1, k + 1):
    length = 1 << (k - round_id)
    print("".join(str(random.randint(0, 1)) for _ in range(length)))

T = random.randint(1, 3)
print(T)
for _ in range(T):
    print(*[random.randint(0, 7) for _ in range(4)])
