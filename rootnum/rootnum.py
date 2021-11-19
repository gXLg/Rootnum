def simple(num):
  p = {}
  i = 2
  while num > 1:
    if not num % i:
      if i in p:
        p[i] += 1
      else:
        p[i] = 1
      num /= i
    else:
      i += 1
  q = {}
  for i in p:
    n = p[i]
    p[i] = n % 2
    q[i] = n // 2
  pp = qq = 1
  for i in p:
    pp *= i ** p[i]
    qq *= i ** q[i]
  return qq, pp


def gcd(a, b):
  while b:
    a, b = b, a % b
  return a


class Rootnum:
  def __init__(self, r = [(1, 1)], d = 1):
    if isinstance(r, float) or isinstance(r, int):
      if r % 1:
        raise TypeError("Cannot convert non-integer to a root number")
      r = [(r, 1)]
    elif isinstance(r, tuple):
      if r[0] % 1 or r[1] % 1:
        raise TypeError("Cannot convert non-integer to a root number")
      r = [r]

    # Pressing root values
    #  e.g. 5√12 becomes 10√3, 'cuz 12 = 4 * 3
    roots = {}
    for i in r:
      if i[0] % 1 or i[1] % 1:
        raise TypeError("One of the given numbers is not an integer")
      if i[1] < 0:
        raise TypeError("Cannot have a root of a negative number")
      a, b = simple(i[1])
      if b in roots:
        roots[b] += a * i[0]
      else:
        roots[b] = a * i[0]

    roots = [(roots[i], i) for i in sorted(roots) if roots[i]]

    # Shortening the divisor
    #  e.g. (10√3)/15 becomes (2√3)/3
    g = d
    for i in roots:
      g = gcd(i[0], g)

    self.d = d // g
    self.roots = [(i[0] // g, i[1]) for i in roots]
    if self.roots == []:
      self.roots = [(0, 0)]
    if self.d == 0:
      raise ZeroDivisionError("Root number with a zero as divisor")

  def __str__(self):
    res = " + ".join(str(i[0]) + "√" + str(i[1]) for i in self.roots)
    res = "( " + res + " ) / " + str(self.d)
    res = res.replace("√1 ", " ")
    res = res.replace("√0 ", " ")
    res = res.replace(" 1√", " √")
    res = res.replace(" -1√", " -√")
    res = res.replace("+ -", "- ")
    res = res.replace("( ", "(")
    res = res.replace(" )", ")")
    if self.d == 1:
      res = res.split("/")[0].strip()
    return res

  def __add__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    # Finding the common divisor for two root numbers
    g = gcd(self.d, x.d)
    d = self.d * x.d // g

    self_roots = [(i[0] * x.d // g, i[1]) for i in self.roots]
    x_roots = [(i[0] * self.d // g, i[1]) for i in x.roots]
    return Rootnum(self_roots + x_roots, d)

  def __radd__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    g = gcd(self.d, x.d)
    d = self.d * x.d // g
    self_roots = [(i[0] * x.d // g, i[1]) for i in self.roots]
    x_roots = [(i[0] * self.d // g, i[1]) for i in x.roots]
    return Rootnum(self_roots + x_roots, d)

  def __sub__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    g = gcd(self.d, x.d)
    d = self.d * x.d // g
    self_roots = [(i[0] * x.d // g, i[1]) for i in self.roots]
    x_roots = [(-i[0] * self.d // g, i[1]) for i in x.roots]
    return Rootnum(self_roots + x_roots, d)

  def __rsub__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    g = gcd(self.d, x.d)
    d = self.d * x.d // g
    self_roots = [(-i[0] * x.d // g, i[1]) for i in self.roots]
    x_roots = [(i[0] * self.d // g, i[1]) for i in x.roots]
    return Rootnum(self_roots + x_roots, d)

  def __neg__(self):
    return Rootnum(self.roots, -self.d)

  def __mul__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    # Multiplying the divisors
    d = self.d * x.d

    # Multiplying all the roots of self and x
    roots = []
    for i in self.roots:
      for j in x.roots:
        roots.append((i[0] * j[0], i[1] * j[1]))
    return Rootnum(roots, d)

  def __rmul__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    d = self.d * x.d
    roots = []
    for i in self.roots:
      for j in x.roots:
        roots.append((i[0] * j[0], i[1] * j[1]))
    return Rootnum(roots, d)

  def __pow__(self, x, y = None):
    # Square powering which performs faster
    if x % 1:
      raise TypeError("Cannot use non-integer for power")
    if x < 0:
      self = 1 / self
      x = abs(x)
    if y:
      self %= y
    res = Rootnum(1)
    while True:
      if x % 2:
        res *= self
      x //= 2
      if not x:
        break
      self *= self
    if y:
      res %= y
    return res

  def __float__(self):
    # The actual value of the root number
    # Though not recommended since float precision is awful
    res = 0
    for i in self.roots:
      res += i[0] * (i[1] ** 0.5)
    return res / self.d

  def __int__(self):
    # The horribly rounded value of the root number
    # Use only for algorithms where you know the result is an integer
    res = 0
    for i in self.roots:
      res += i[0] * int(i[1] ** 0.5)
    return res // self.d

  def __truediv__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)

    # Difficult process
    # 1) Cross multiplication,
    #  like it's tought in school;
    #  (a/b) / (c/d) = (a/b) * (d/c)
    # 2) 3. polynomial formula multiplication,
    #  until all roots in the divisor gone;
    #  ( a + b + c + d + ... ) * ( a - b + c - d + ... )
    #  - will always produce one root less
    a = Rootnum(self.roots) * x.d
    b = Rootnum(x.roots) * self.d
    while len(b.roots) > 1 or not b.roots[0][1] == 1:
      c = []
      n = 0
      for i in b.roots:
        c.append(((-i[0] if n else i[0]), i[1]))
        n ^= 1
      a *= Rootnum(c)
      b *= Rootnum(c)

    return Rootnum(a.roots, b.roots[0][0])

  def __rtruediv__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    self, x = x, self
    a = Rootnum(self.roots) * x.d
    b = Rootnum(x.roots) * self.d
    while len(b.roots) > 1 or not b.roots[0][1] == 1:
      c = []
      n = 0
      for i in b.roots:
        c.append(((-i[0] if n else i[0]), i[1]))
        n ^= 1
      a *= Rootnum(c)
      b *= Rootnum(c)

    return Rootnum(a.roots, b.roots[0][0])

  def __lt__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)

    # Algorithm by Ashot#6755
    # Uses the idea that
    # geometrical mean < arithmetical mean < root square mean
    # If it fails: uses awful float transformation
    a = self - x
    if a.roots[0][0] == 0:
      return False
    left = [i for i in a.roots if i[0] > 0]
    right = [(abs(i[0]), i[1]) for i in a.roots if i[0] < 0]
    left = [(i[0] * len(right), i[1]) for i in left]
    right = [(i[0] * len(left), i[1]) for i in right]

    if not left:
      return True
    if not right:
      return False

    mean_left = Rootnum(1)
    left_n = 0
    for i in left:
      mean_left *= Rootnum(i)
      left_n += 1
    mean_right = Rootnum(0)
    right_n = 2
    for i in right:
      mean_right += Rootnum(i) ** 2
    mean_right /= len(right)

    mean_left = mean_left ** right_n
    mean_right = mean_right ** left_n
    mean_left = mean_left.roots[0][0]
    mean_right = mean_right.roots[0][0]

    if mean_left >= mean_right:
      return False

    mean_right = Rootnum(1)
    right_n = 0
    for i in right:
      mean_right *= Rootnum(i)
      right_n += 1
    mean_left = Rootnum(0)
    left_n = 2
    for i in left:
      mean_left += Rootnum(i) ** 2
    mean_left /= len(left)

    mean_left = mean_left ** right_n
    mean_right = mean_right ** left_n
    mean_left = mean_left.roots[0][0]
    mean_right = mean_right.roots[0][0]

    if mean_left <= mean_right:
      return True

    return float(a) < 0

  def __le__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    a = self - x
    if a.roots[0][0] == 0:
      return True
    left = [i for i in a.roots if i[0] > 0]
    right = [(abs(i[0]), i[1]) for i in a.roots if i[0] < 0]
    left = [(i[0] * len(right), i[1]) for i in left]
    right = [(i[0] * len(left), i[1]) for i in right]

    if not left:
      return True
    if not right:
      return False

    mean_left = Rootnum(1)
    left_n = 0
    for i in left:
      mean_left *= Rootnum(i)
      left_n += 1
    mean_right = Rootnum(0)
    right_n = 2
    for i in right:
      mean_right += Rootnum(i) ** 2
    mean_right /= len(right)

    mean_left = mean_left ** right_n
    mean_right = mean_right ** left_n
    mean_left = mean_left.roots[0][0]
    mean_right = mean_right.roots[0][0]

    if mean_left >= mean_right:
      return False

    mean_right = Rootnum(1)
    right_n = 0
    for i in right:
      mean_right *= Rootnum(i)
      right_n += 1
    mean_left = Rootnum(0)
    left_n = 2
    for i in left:
      mean_left += Rootnum(i) ** 2
    mean_left /= len(left)

    mean_left = mean_left ** right_n
    mean_right = mean_right ** left_n
    mean_left = mean_left.roots[0][0]
    mean_right = mean_right.roots[0][0]

    if mean_left <= mean_right:
      return True

    return float(a) < 0

  def __gt__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    a = x - self
    if a.roots[0][0] == 0:
      return False
    left = [i for i in a.roots if i[0] > 0]
    right = [(abs(i[0]), i[1]) for i in a.roots if i[0] < 0]
    left = [(i[0] * len(right), i[1]) for i in left]
    right = [(i[0] * len(left), i[1]) for i in right]

    if not left:
      return True
    if not right:
      return False

    mean_left = Rootnum(1)
    left_n = 0
    for i in left:
      mean_left *= Rootnum(i)
      left_n += 1
    mean_right = Rootnum(0)
    right_n = 2
    for i in right:
      mean_right += Rootnum(i) ** 2
    mean_right /= len(right)

    mean_left = mean_left ** right_n
    mean_right = mean_right ** left_n
    mean_left = mean_left.roots[0][0]
    mean_right = mean_right.roots[0][0]

    if mean_left >= mean_right:
      return False

    mean_right = Rootnum(1)
    right_n = 0
    for i in right:
      mean_right *= Rootnum(i)
      right_n += 1
    mean_left = Rootnum(0)
    left_n = 2
    for i in left:
      mean_left += Rootnum(i) ** 2
    mean_left /= len(left)

    mean_left = mean_left ** right_n
    mean_right = mean_right ** left_n
    mean_left = mean_left.roots[0][0]
    mean_right = mean_right.roots[0][0]

    if mean_left <= mean_right:
      return True

    return float(a) < 0

  def __ge__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    a = x - self
    if a.roots[0][0] == 0:
      return True
    left = [i for i in a.roots if i[0] > 0]
    right = [(abs(i[0]), i[1]) for i in a.roots if i[0] < 0]
    left = [(i[0] * len(right), i[1]) for i in left]
    right = [(i[0] * len(left), i[1]) for i in right]

    if not left:
      return True
    if not right:
      return False

    mean_left = Rootnum(1)
    left_n = 0
    for i in left:
      mean_left *= Rootnum(i)
      left_n += 1
    mean_right = Rootnum(0)
    right_n = 2
    for i in right:
      mean_right += Rootnum(i) ** 2
    mean_right /= len(right)

    mean_left = mean_left ** right_n
    mean_right = mean_right ** left_n
    mean_left = mean_left.roots[0][0]
    mean_right = mean_right.roots[0][0]

    if mean_left >= mean_right:
      return False

    mean_right = Rootnum(1)
    right_n = 0
    for i in right:
      mean_right *= Rootnum(i)
      right_n += 1
    mean_left = Rootnum(0)
    left_n = 2
    for i in left:
      mean_left += Rootnum(i) ** 2
    mean_left /= len(left)

    mean_left = mean_left ** right_n
    mean_right = mean_right ** left_n
    mean_left = mean_left.roots[0][0]
    mean_right = mean_right.roots[0][0]

    if mean_left <= mean_right:
      return True

    return float(a) < 0

  def __eq__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    a = x - self
    if a.roots[0][0] == 0:
      return True
    return False

  def __mod__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    if self > 0:
      self_sign = 1
    else:
      self_sign = -1
      self = -self
    if x > 0:
      x_sign = 1
    else:
      x_sign = -1
      x = -x
    if x:
      while self >= x:
        self = self - x
    return self_sign * x_sign * self

  def __rmod__(self, x):
    if not isinstance(x, Rootnum):
      x = Rootnum(x)
    self, x = x, self
    if self > 0:
      self_sign = 1
    else:
      self_sign = -1
      self = -self
    if x > 0:
      x_sign = 1
    else:
      x_sign = -1
      x = -x
    if x:
      while self >= x:
        self = self - x
    return self_sign * x_sign * self
