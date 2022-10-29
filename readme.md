## Instructions
### Linux:
```shell
git clone https://github.com/Ted-Barrett/propositional-logic-evaluator.git
cd propositional-logic-evaluator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py "(P | Q)"
```
### Windows:
```shell
git clone https://github.com/Ted-Barrett/propositional-logic-evaluator.git
cd propositional-logic-evaluator
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py "(P | Q)"
```

The program will print the results and also write them to a csv, `truth_table.csv`.
Note that truth_table.csv will be overwritten each time the program is run.

### Example
```
$ python3 main.py "((P => Q) => R)" "(Q <+> R)"
  P    Q    R  |      ((P => Q) => R)    (Q <+> R)
---  ---  ---  ---  -----------------  -----------
  0    0    0  |                    0            0
  0    0    1  |                    1            1
  0    1    0  |                    0            1
  0    1    1  |                    1            0
  1    0    0  |                    1            0
  1    0    1  |                    1            1
  1    1    0  |                    0            1
  1    1    1  |                    1            0
```

### Arguments
The calculator takes in as many propositional logic statements as you want.
Each must be contained within brackets and quotes, and separated by a space.
The following are all valid commands:
```shell
python3 main.py "(P | Q)"
python3 main.py "(P => Q)" "((P => ~Q) | R)" "(P | Q)"
python3 main.py "(((P <=> Q) => R) & S)"
```

Valid connectives are:

`&`: And
<br>
`|`: Or
<br>
`=>`: Implication
<br>
`<=>`: Biimplication
<br>
`<+>`: Exclusive Or

To negate an expression or variable, put an ~ in front of it. You should not include more brackets than necessary,
as this will break the program.

### Conditions of use
Please note that this project was made for hobby purposes and therefore there is no guarantee for
the accuracy of the results produced.