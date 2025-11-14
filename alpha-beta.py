# Alpha–Beta Pruning for Problem 1

# Tree leaves (left → right) labelled as in question
leaves = {
    "A": 21, "B": 5,  "C": 15, "D": 11,
    "E": 12, "F": 8,  "G": 9,  "H": 13,
    "I": 5,  "J": 12, "K": 13, "L": 12,
    "M": 13, "N": 14, "O": 7,  "P": 10
}

# Tree structure (bottom-up)
# Each internal node is defined as: ("NodeName", [children])

tree = (
    "Root", [
        ("MIN_Left", [
            ("MAX_AtoD", [
                ("MIN_AD", ["A", "B"]),
                ("MIN_CD", ["C", "D"])
            ]),
            ("MAX_EtoH", [
                ("MIN_EF", ["E", "F"]),
                ("MIN_GH", ["G", "H"])
            ])
        ]),
        ("MIN_Right", [
            ("MAX_ItoL", [
                ("MIN_IJ", ["I", "J"]),
                ("MIN_KL", ["K", "L"])
            ]),
            ("MAX_MtoP", [
                ("MIN_MN", ["M", "N"]),
                ("MIN_OP", ["O", "P"])
            ])
        ])
    ]
)

visited = []
pruned = []
path_taken = []


def alpha_beta(node, alpha, beta, is_max):
    name, children = node

    # Leaf node → children is a string leaf name
    if isinstance(children, str):
        visited.append(children)
        return leaves[children], [children]

    # MAX node
    if is_max:
        value = float("-inf")
        best_path = []
        for child in children:
            child_value, child_path = alpha_beta(child, alpha, beta, False)
            if child_value > value:
                value = child_value
                best_path = [name] + child_path
            alpha = max(alpha, value)
            if alpha >= beta:      # prune
                # Mark remaining children as pruned
                idx = children.index(child)
                for p in children[idx+1:]:
                    collect_pruned(p)
                break
        return value, best_path

    # MIN node
    else:
        value = float("inf")
        best_path = []
        for child in children:
            child_value, child_path = alpha_beta(child, alpha, beta, True)
            if child_value < value:
                value = child_value
                best_path = [name] + child_path
            beta = min(beta, value)
            if alpha >= beta:     # prune
                idx = children.index(child)
                for p in children[idx+1:]:
                    collect_pruned(p)
                break
        return value, best_path


def collect_pruned(subtree):
    """Record all leaf nodes under a pruned subtree."""
    name, children = subtree
    if isinstance(children, str):
        pruned.append(children)
    else:
        for c in children:
            collect_pruned(c)


# Run Alpha–Beta
value, full_path = alpha_beta(tree, float("-inf"), float("inf"), True)

print("Root Value =", value)
print("Path Returned =", " → ".join(full_path))
print("Visited Leaves =", visited)
print("Pruned Leaves =", pruned)
