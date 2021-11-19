# rootnum
A python module for accurate square root operations

# Usage

## installation
```
pip install rootnum
```

## import

```py
from rootnum import Rootnum
```

## creating s square root

```py
num = Rootnum([(1, 1), (1, 5)], 2)
print(num)
```
outputs
```
(1 + √5) / 2
```

## math

```py
a = num + (1, 2)
b = 1 / num
print(a)
print(b)
```
outputs
```
(1 + 2√2 + √5) / 2
(-1 + √5) / 2
```
