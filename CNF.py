class Expr:
    pass

class Var(Expr):
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name

class Not(Expr):
    def __init__(self, expr):
        self.expr = expr
        
    def __repr__(self):
        return f"~{self.expr}"

class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"

class Or(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

class Impl(Expr):     # A → B
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
class Iff(Expr):      # A ↔ B
    def __init__(self, left, right):
        self.left = left
        self.right = right


# ---------------------------------------
# 1. Eliminate → and ↔
# ---------------------------------------
def eliminate_implications(expr):
    if isinstance(expr, Var):
        return expr
    
    if isinstance(expr, Not):
        return Not(eliminate_implications(expr.expr))
    
    if isinstance(expr, And):
        return And(eliminate_implications(expr.left),
                   eliminate_implications(expr.right))
    
    if isinstance(expr, Or):
        return Or(eliminate_implications(expr.left),
                  eliminate_implications(expr.right))
    
    if isinstance(expr, Impl):   # A → B  becomes  ~A ∨ B
        return Or(Not(eliminate_implications(expr.left)),
                  eliminate_implications(expr.right))
    
    if isinstance(expr, Iff):    # A ↔ B  becomes  (A→B) ∧ (B→A)
        left_imp = Impl(expr.left, expr.right)
        right_imp = Impl(expr.right, expr.left)
        return And(eliminate_implications(left_imp),
                   eliminate_implications(right_imp))


# ---------------------------------------
# 2. Move NOT inward using DeMorgan
# ---------------------------------------
def move_not(expr):
    if isinstance(expr, Var):
        return expr
    
    if isinstance(expr, Not):
        inner = expr.expr
        
        if isinstance(inner, Var):
            return expr
        
        if isinstance(inner, Not):
            return move_not(inner.expr)
        
        if isinstance(inner, And):
            return Or(move_not(Not(inner.left)),
                      move_not(Not(inner.right)))
        
        if isinstance(inner, Or):
            return And(move_not(Not(inner.left)),
                       move_not(Not(inner.right)))
    
    if isinstance(expr, And):
        return And(move_not(expr.left), move_not(expr.right))
    
    if isinstance(expr, Or):
        return Or(move_not(expr.left), move_not(expr.right))


# ---------------------------------------
# 3. Distribute OR over AND
# ---------------------------------------
def distribute(expr):
    if isinstance(expr, Var) or isinstance(expr, Not):
        return expr
    
    if isinstance(expr, And):
        return And(distribute(expr.left), distribute(expr.right))
    
    if isinstance(expr, Or):
        left = distribute(expr.left)
        right = distribute(expr.right)
        
        if isinstance(left, And):
            return And(distribute(Or(left.left, right)),
                       distribute(Or(left.right, right)))
        
        if isinstance(right, And):
            return And(distribute(Or(left, right.left)),
                       distribute(Or(left, right.right)))
        
        return Or(left, right)


# ---------------------------------------
# MAIN CNF CONVERTER
# ---------------------------------------
def to_cnf(expr):
    step1 = eliminate_implications(expr)
    step2 = move_not(step1)
    step3 = distribute(step2)
    return step3


# ---------------------------------------
# EXAMPLE
# ---------------------------------------

# Convert (A → (B ∧ C))
A = Var("A")
B = Var("B")
C = Var("C")

formula = Impl(A, And(B, C))
print("Original:", formula)

cnf = to_cnf(formula)
print("CNF:", cnf)
