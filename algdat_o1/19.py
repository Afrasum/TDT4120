#!/usr/bin/python3
# coding=utf-8
import random

# Testsettet pÃ¥ serveren er stÃ¸rre og mer omfattende enn dette.
# Hvis programmet ditt fungerer lokalt, men ikke nÃ¥r du laster det opp,
# er det gode sjanser for at det er tilfeller du ikke har tatt hÃ¸yde for.

# De lokale testene bestÃ¥r av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for Ã¥ generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved Ã¥ juste pÃ¥ verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall verdier i generert instans.
n_lower = 3
# HÃ¸yest mulig antall verdier i generert instans.
n_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0
# Kontrollerer om resultatet av tester som feiler skal skrives ut i kompakt
# eller detaljert format.
compact_print = False


def sort(stack1, stack2, stack3):
    """
    Naturlig 2-veis merge med 3 stakker.
    Flyt:
      1) split s1 -> s2/s3 i naturlige fallende runs (minste på topp i mål).
      2) while total_runs > 1:
           - merge s2 + s3 -> s1 (bruk lagrede run-lengder; minimale peeks)
           - hvis fortsatt flere enn 1 run: split s1 -> s2/s3 igjen (kun etter fullført merge)
      3) til slutt ligger sortert (minste på topp) i s1.
    """

    s1, s2, s3 = stack1, stack2, stack3

    # ---------- små util ----------

    def safe_peek(S):
        # kall peek kun hvis ikke tom
        return S.peek() if not S.empty() else None

    def move_k(src, dst, k):
        # flytt nøyaktig k elementer fra src til dst
        for _ in range(k):
            dst.push(src.pop())

    def move_all(src, dst):
        while not src.empty():
            dst.push(src.pop())

    # ---------- split til naturlige fallende runs ----------
    def split_into_natural_runs(src, dstA, dstB):
        runsA, runsB = [], []
        toA = True
        while not src.empty():
            cur_len = 0
            last = src.pop()
            (dstA if toA else dstB).push(last)
            cur_len += 1
            while not src.empty():
                nxt = safe_peek(src)  # 1 peek
                # fallende på src => <= last for å fortsette run
                if nxt is not None and nxt <= last:
                    last = src.pop()
                    (dstA if toA else dstB).push(last)
                    cur_len += 1
                else:
                    break
            if toA:
                runsA.append(cur_len)
            else:
                runsB.append(cur_len)
            toA = not toA
        return runsA, runsB

    # ---------- merge ett par runs (lenA fra A, lenB fra B) til D ----------
    def merge_one_pair(lenA, lenB, A, B, D):
        a_left = lenA
        b_left = lenB
        a_top = safe_peek(A) if a_left > 0 else None
        b_top = safe_peek(B) if b_left > 0 else None
        while a_left > 0 and b_left > 0:
            # velg minste topp
            if a_top is not None and b_top is not None and a_top <= b_top:
                D.push(A.pop())
                a_left -= 1
                a_top = safe_peek(A) if a_left > 0 else None
            else:
                D.push(B.pop())
                b_left -= 1
                b_top = safe_peek(B) if b_left > 0 else None
        # dump resten
        while a_left > 0:
            D.push(A.pop())
            a_left -= 1
        while b_left > 0:
            D.push(B.pop())
            b_left -= 1
        return lenA + lenB

    # ---------- merge en hel pass (bruker run-lister) ----------
    def merge_pass(runsA, runsB, A, B, D):
        runsD = []
        iA = len(runsA) - 1
        iB = len(runsB) - 1
        while iA >= 0 and iB >= 0:
            la = runsA[iA]
            lb = runsB[iB]
            iA -= 1
            iB -= 1
            merged = merge_one_pair(la, lb, A, B, D)
            runsD.append(merged)
        # hvis ulikt antall runs: flytt de resterende runene i samme rekkefølge til D
        while iA >= 0:
            la = runsA[iA]
            iA -= 1
            move_k(A, D, la)
            runsD.append(la)
        while iB >= 0:
            lb = runsB[iB]
            iB -= 1
            move_k(B, D, lb)
            runsD.append(lb)
        return runsD

    # ---------- redistribuer runs fra D til A/B for neste merge ----------
    def redistribute_runs_from(D, A, B, runsD):
        # runsD beskriver run-lengdene på D (øverste run sist i lista).
        # Vi fordeler annenhver run tilbake til A og B ved å flytte k elementer per run.
        toA = True
        i = len(runsD) - 1
        while i >= 0:
            k = runsD[i]
            i -= 1
            if toA:
                move_k(D, A, k)
            else:
                move_k(D, B, k)
            toA = not toA

    # 1) første split
    runs2, runs3 = split_into_natural_runs(s1, s2, s3)
    total_runs = len(runs2) + len(runs3)

    if total_runs <= 1:
        # alt er allerede ett run – flytt hjem hvis nødvendig
        if not s2.empty():
            move_all(s2, s1)
        elif not s3.empty():
            move_all(s3, s1)
        return

    # 2) gjenta merge + redistribusjon til vi har kun ett run
    while total_runs > 1:
        # flett s2+s3 -> s1
        runs1 = merge_pass(runs2, runs3, s2, s3, s1)
        total_runs = len(runs1)
        if total_runs <= 1:
            # ferdig – s1 har ett run (minste på topp)
            break
        # redistribuer s1 -> s2/s3 for neste pass
        runs2, runs3 = [], []
        redistribute_runs_from(s1, s2, s3, runs1)
        # når vi fordeler annenhver, blir run-lister balansert igjen:
        # oppbygg samme lister i samme forløp:
        toA = True
        for r in reversed(runs1):
            if toA:
                runs2.append(r)
            else:
                runs3.append(r)
            toA = not toA
        total_runs = len(runs2) + len(runs3)

    # 3) s1 inneholder sortert med minste på topp
    # (Ingen ekstra “flip” nødvendig, siden vi alltid holder runene fallende på kilder
    #  og fletting produserer konsekvent riktig topp-orientering for neste steg.)

    # --- Sørg for korrekt topp: minste skal ligge øverst i s1 ---
    if not s1.empty():
        top1 = s1.pop()
        if not s1.empty():
            top2 = s1.pop()
            # legg tilbake i samme rekkefølge
            s1.push(top2)
            s1.push(top1)
            # Hvis nest øverste < øverste, så er største øverst -> vi må reversere hele stakken
            if top2 < top1:
                # Enkelt hel-revers med to hjelpe-stakker (odd antall reverseringer = reversert)
                while not s1.empty():
                    s2.push(s1.pop())
                while not s2.empty():
                    s3.push(s2.pop())
                while not s3.empty():
                    s1.push(s3.pop())
    return


# Hardkodetetester, hÃ¸yre side blir toppen av stakken
tests = [
    [4, 3, 2, 1],
    [1, 2, 3, 4],
    [4, 2, 1, 7],
    [1, 1, 1, 1],
    [7, 3, 9, 2, 0, 1, 3, 4],
    [7, 3, 0, 13, 48, 49, 233, 9, 2, 0, 1, 3, 4],
]


# Genererer k tilfeldige tester, hver med et tilfeldig antall elementer plukket
# uniformt fra intervallet [nl, nu].
def gen_examples(k, nl, nu):
    for _ in range(k):
        yield [random.randint(-99, 99) for _ in range(random.randint(nl, nu))]


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(random_tests, n_lower, n_upper))


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1

    def get_value(self):
        return self.value


class Stack:
    def __init__(self, operation_counter, element_counter, initial=None):
        self.stack = []
        if initial is not None:
            self.stack = initial

        self.element_counter = element_counter
        self.operation_counter = operation_counter

    def push(self, value):
        if self.element_counter.get_value() <= 0:
            raise RuntimeError(
                "Du kan ikke ta vare pÃ¥ flere elementer pÃ¥ "
                "stakkene enn det fantes originalt."
            )
        self.stack.append(value)
        self.element_counter.decrement()
        self.operation_counter.increment()

    def pop(self):
        if self.element_counter.get_value() >= 2:
            raise RuntimeError(
                "Du kan ikke ha mer enn 2 elementer i minnet " "av gangen."
            )
        self.element_counter.increment()
        self.operation_counter.increment()
        return self.stack.pop()

    def peek(self):
        self.operation_counter.increment()
        return self.stack[-1]

    def empty(self):
        return len(self.stack) == 0


failed = False
first = True

for test in tests:
    counter1 = Counter()
    counter2 = Counter()
    stack1 = Stack(counter1, counter2, initial=test[:])
    stack2, stack3 = Stack(counter1, counter2), Stack(counter1, counter2)

    sort(stack1, stack2, stack3)

    result = []
    counter2.value = float("-inf")
    while not stack1.empty():
        result.append(stack1.pop())

    if not first:
        print("-" * 50)

    if result != sorted(test) and compact_print:
        print(
            f"""
Koden feilet for fÃ¸lgende instans:
Start (stack1, fra topp til bunn): {test[::-1]}

Ditt svar (stack1, fra topp til bunn): {result}
Forventet svar: {sorted(test)}
"""
        )
        failed = True
    elif result != sorted(test):
        result2 = []
        while not stack2.empty():
            result2.append(stack2.pop())

        result3 = []
        while not stack3.empty():
            result3.append(stack3.pop())
        print(
            f"""
Koden feilet for fÃ¸lgende instans.
---------------
 Starttilstand
---------------

--------
Stack 1:
--------
{chr(10).join(map(str, test[::-1])) or "ingen elementer i stakken"}

--------------
 Sluttilstand
--------------

--------
Stack 1:
--------
{chr(10).join(map(str, result)) or "ingen elementer i stakken"}

--------
Stack 2:
--------
{chr(10).join(map(str, result2)) or "ingen elementer i stakken"}

--------
Stack 3:
--------
{chr(10).join(map(str, result3)) or "ingen elementer i stakken"}
"""
        )
        failed = True
    else:
        print(
            f"""
Koden brukte {counter1.get_value() - len(result)} operasjoner pÃ¥ sortering av
{test[::-1]}
"""
        )

    first = False

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")
