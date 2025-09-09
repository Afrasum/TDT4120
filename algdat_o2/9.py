# tar inn liste, returnere true om n unike elementer finnes
def unique(A, n):
    s = set(A)
    return len(s) >= n


def verify_ham_cycle(g, cert):
    print("Case")
    # print g matrix nicely
    print("G:")
    for row in g:
        print(row)
    print("cert:", cert)

    n = len(g)

    if n == 1:
        return cert == [0, 0]

    if not len(cert) == len(g) + 1:
        return False

    if cert[0] != cert[-1]:
        return False

    visitet = set(cert)
    if len(visitet) != n:
        return False

    for i in range(len(cert) - 1):
        if cert[i] >= n or cert[i + 1] >= n or cert[i] < 0 or cert[i + 1] < 0:
            return False

        if not g[cert[i]][cert[i + 1]]:
            return False

    return True


# Test cases
test_cases = [
    {
        "G": [
            [0, 1, 1, 0, 0],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 0, 1],
            [0, 1, 0, 0, 1],
            [0, 1, 1, 1, 0],
        ],
        "cert": [1, 2, 4, 5, 3, 1],
        "expected": True,
    },
    {"G": [[0]], "cert": [0, 0], "expected": True},
    {"G": [[1]], "cert": [0, 0], "expected": False},
]


# Run all test cases
def run_tests():
    print("Running test cases for verify_ham_cycle:")
    for i, test_case in enumerate(test_cases, 1):
        G = test_case["G"]
        cert = test_case["cert"]
        expected = test_case["expected"]

        result = verify_ham_cycle(G, cert)
        status = "PASS" if result == expected else "FAIL"

        print(f"Test {i}: {status}")
        print(f"  Graph: {G}")
        print(f"  Certificate: {cert}")
        print(f"  Expected: {expected}, Got: {result}")
        print()


if __name__ == "__main__":
    run_tests()
