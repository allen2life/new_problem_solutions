#!/usr/bin/env python3
import random


def main():
    random.seed()
    # TODO: generate input for this problem.


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import random

n = random.randint(1, 8)
print(n)

values = []
for _ in range(n):
    values.append(random.randint(1, 10))
print(*values)
