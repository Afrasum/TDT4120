def take_pieces(n):
    """
    Returnerer antall fyrstikker å ta for å garantere seier.
    Hvis seier ikke kan garanteres, returner et gyldig antall (1-7).

    Regler:
    - Må ta minst 1, maksimalt 7 fyrstikker
    - Den som tar den siste fyrstikken taper
    """
    # Skriv koden din her
    x = (n - 1) % 8
    return max(n - 1, 1) if n <= 9 else max(x, 1)


# Test cases
test_cases = [
    {
        "n_pieces": 1,
        "expected_can_win": False,
        "description": "1 fyrstikk igjen - må tape",
    },
    {
        "n_pieces": 8,
        "expected_can_win": True,
        "description": "8 fyrstikker - perfekt posisjon",
    },
    {
        "n_pieces": 15,
        "expected_can_win": False,
        "description": "15 fyrstikker - kan ikke garantere seier",
    },
    {
        "n_pieces": 16,
        "expected_can_win": True,
        "description": "16 fyrstikker - perfekt posisjon",
    },
    {
        "n_pieces": 23,
        "expected_can_win": False,
        "description": "23 fyrstikker - kan ikke garantere seier",
    },
    {
        "n_pieces": 24,
        "expected_can_win": True,
        "description": "24 fyrstikker - perfekt posisjon",
    },
    {
        "n_pieces": 10,
        "expected_can_win": False,
        "description": "10 fyrstikker - kan ikke garantere seier",
    },
    {"n_pieces": 7, "expected_can_win": False, "description": "7 fyrstikker - må tape"},
    {
        "n_pieces": 2,
        "expected_can_win": False,
        "description": "2 fyrstikker - kan ikke garantere seier",
    },
    {
        "n_pieces": 100,
        "expected_can_win": False,
        "description": "100 fyrstikker - kan ikke garantere seier",
    },
]


def can_guarantee_win(n_pieces, taken):
    """
    Sjekker om et trekk garanterer seier ved å se om motstanderen
    kommer i en tapende posisjon.
    """
    remaining = n_pieces - taken
    if remaining == 0:
        return False  # Vi tar siste fyrstikk = vi taper

    # Sjekk om motstanderen er i en tapende posisjon
    # Tapende posisjoner er 1, 2, 3, 4, 5, 6, 7 (må ta siste)
    # og alle tall som er 8k + (1-7) hvor k >= 0
    return remaining % 8 == 0 and remaining > 0


def run_tests():
    print("Testing take_pieces function:")
    print("=" * 50)

    correct = 0
    total = len(test_cases)

    for i, test_case in enumerate(test_cases, 1):
        n_pieces = test_case["n_pieces"]
        expected_can_win = test_case["expected_can_win"]
        description = test_case["description"]

        result = take_pieces(n_pieces)

        # Sjekk at resultatet er gyldig (1-7)
        valid_range = 1 <= result <= 7

        # Sjekk om trekket garanterer seier
        can_win = can_guarantee_win(n_pieces, result) if valid_range else False

        # Sammenlign med forventet resultat
        test_passed = (can_win == expected_can_win) and valid_range

        if test_passed:
            correct += 1

        print(f"Test {i}: {description}")
        print(f"  Input: {n_pieces} fyrstikker")
        print(f"  Output: Ta {result} fyrstikker")
        print(f"  Valid range (1-7): {'✓' if valid_range else '✗'}")
        print(f"  Can guarantee win: {'✓' if can_win else '✗'}")
        print(f"  Expected can win: {'✓' if expected_can_win else '✗'}")
        print(f"  Result: {'✓ RIKTIG' if test_passed else '✗ FEIL'}")

        if valid_range:
            remaining = n_pieces - result
            print(f"  Gjenstående etter trekk: {remaining}")

        print()

    print("=" * 50)
    print(f"Resultat: {correct}/{total} tester riktig")
    print(f"Score: {correct/total*100:.1f}%")


if __name__ == "__main__":
    run_tests()
