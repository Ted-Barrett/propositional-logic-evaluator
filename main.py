import argparse
import re
from tabulate import tabulate
import csv


def con_and(a, b):
    return a and b


def con_or(a, b):
    return a or b


def con_impl(a, b):
    return (not a) or b


def con_biim(a, b):
    return a == b


def con_xor(a, b):
    return (a and (not b)) or ((not a) and b)


CONNECTIVES = {
    "&": con_and,
    "|": con_or,
    "=>": con_impl,
    "<=>": con_biim,
    "<+>": con_xor,
}


class variable:
    def __init__(self, character: str, negated: bool):
        self.character = character
        self.negated = negated

    def __str__(self):
        return ("~" if self.negated else "") + self.character

    def evaluate(self, values_dict):
        if self.negated:
            return not values_dict[self.character]
        return values_dict[self.character]


class expression:
    def __init__(self, op: str, left, right, negated = False):
        self.op = op
        self.left = left
        self.right = right
        self.negated = negated

    def __str__(self):
        return ("~" if self.negated else "") + "(" + str(self.left) + " " + self.op + " " + str(self.right) + ")"

    def evaluate(self, values_dict):
        value = CONNECTIVES[self.op](
            self.left.evaluate(values_dict), self.right.evaluate(values_dict)
        )
        if self.negated:
            value = not value
        return value

    @staticmethod
    def parse(expr_string: str):
        negated = False
        if expr_string[0] == "~":
            negated = True
            expr_string = expr_string[1:]
        if re.match(r"[A-Z]", expr_string):
            return variable(
                re.match(r"[A-Z]", expr_string).group(),
                negated
            )

        expr_string = expr_string[1:-1]
        if expr_string.count("(") == 0:
            left, op, right = expr_string.split()
            if op not in CONNECTIVES:
                raise ValueError("Invalid connective:", op)
            return expression(op, expression.parse(left), expression.parse(right), negated)

        left, right = get_bracket(expr_string), get_bracket(expr_string, "right")
        op = expr_string[len(left) + 1 : -len(right) - 1]
        if op not in CONNECTIVES:
            raise ValueError("Invalid connective:", op)

        return expression(op, expression.parse(left), expression.parse(right), negated)


def get_bracket(s, direction="left"):
    if not direction in ("left", "right"):
        raise ValueError("Invalid direction:", direction)
    indices = range(len(s))
    if direction == "left":
        if s[0] != "(":
            return s.split()[0]
    if direction == "right":
        if s[-1] != ")":
            return s.split()[-1]
        indices = reversed(indices)
    n = 0
    for i in indices:
        c = s[i]
        if c == "(":
            n += 1
        elif c == ")":
            n -= 1
        if n == 0:
            if direction == "right":
                return s[i:]
            return s[: i + 1]


def get_variables(expr):
    return set(re.findall(r"[A-Z]", expr))


def get_all_variables(exprs):
    variables = set()

    for expr in args.expressions:
        variables.update(get_variables(expr))

    return sorted(list(variables))


def gen_truth_table(variables, expressions):
    out = []
    for i in range(2 ** len(variables)):
        assignments = [bool(int(j)) for j in bin(i)[2:].rjust(len(variables), "0")]

        d = {
            character: assignment
            for (character, assignment) in zip(variables, assignments)
        }

        out.append(assignments)
        out[-1].append("|")

        for e in expressions:
            out[-1].append(e.evaluate(d))
    return out

def pretty_truth_table(variables, expressions, digits = False, headers = True):
    t = gen_truth_table(variables, expressions)
    if digits:
        for x in range(len(t)):
            for y in range(len(t[0])):
                cell = t[x][y]
                if type(cell) == bool:
                    if cell:
                        t[x][y] = "1"
                    else:
                        t[x][y] = "0"
    if headers:
        return tabulate(
            t,
            headers=variables + ["|"] + [str(e) for e in expressions]
        )
    return tabulate(t)

def save_truth_table_csv(variable, expressions, digits = True):
    t = gen_truth_table(variables, expressions)
    if digits:
        for x in range(len(t)):
            for y in range(len(t[0])):
                cell = t[x][y]
                if type(cell) == bool:
                    if cell:
                        t[x][y] = "1"
                    else:
                        t[x][y] = "0"
    with open("truth_table.csv", "w", newline="") as csvFile:
        csv_writer = csv.writer(csvFile)
        csv_writer.writerow(variables + ["|"] + [str(e) for e in expressions])
        csv_writer.writerows(t)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Truth Table Calculator")
    parser.add_argument("expressions", nargs="+")

    args = parser.parse_args()

    variables = get_all_variables(args.expressions)
    expressions = [expression.parse(e) for e in args.expressions]

    save_truth_table_csv(variables, expressions)
    print(pretty_truth_table(variables, expressions, digits=True))

