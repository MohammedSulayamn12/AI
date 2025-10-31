from itertools import product

# Define propositional sentences as functions
def Q_implies_P(P, Q, R):
    return (not Q) or P

def P_implies_notQ(P, Q, R):
    return (not P) or (not Q)

def Q_or_R(P, Q, R):
    return Q or R

# Knowledge Base: all must be True
def KB(P, Q, R):
    return Q_implies_P(P, Q, R) and P_implies_notQ(P, Q, R) and Q_or_R(P, Q, R)

# Queries:
def query_R(P, Q, R):
    return R

def query_R_implies_P(P, Q, R):
    return (not R) or P

def query_Q_implies_R(P, Q, R):
    return (not Q) or R

# All symbols
symbols = ['P', 'Q', 'R']

print(f"{'P':>2} {'Q':>2} {'R':>2} | KB | R | R→P | Q→R")
print("-" * 27)

models_where_KB_true = []

for values in product([True, False], repeat=3):
    P, Q, R = values
    kb_val = KB(P, Q, R)
    if kb_val:
        models_where_KB_true.append(values)
    r_val = query_R(P, Q, R)
    r_implies_p_val = query_R_implies_P(P, Q, R)
    q_implies_r_val = query_Q_implies_R(P, Q, R)
    print(f"{str(P)[0]:>2} {str(Q)[0]:>2} {str(R)[0]:>2} | {str(kb_val)[0]:>2} | {str(r_val)[0]:>2} | {str(r_implies_p_val)[0]:>3} | {str(q_implies_r_val)[0]:>3}")

# Now check entailments by checking if in all KB-true models, query is true
def check_entailment(query_func):
    for model in models_where_KB_true:
        if not query_func(*model):
            return False
    return True

print("\nEntailment Results:")
print(f"KB ⊨ R : {check_entailment(query_R)}")
print(f"KB ⊨ R → P : {check_entailment(query_R_implies_P)}")
print(f"KB ⊨ Q → R : {check_entailment(query_Q_implies_R)}")
