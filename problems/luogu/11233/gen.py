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
n = random.randint(2, 12)

print(T)
print(n)
print(*[random.randint(1, 8) for _ in range(n)])
