import hashlib

class MerkleTree:
    def __init__(self, leaves):
        self.leaves = leaves
        self.tree = self.build_tree()

    def build_tree(self):
        if not self.leaves:
            return [['0']]
        leaves = [hashlib.sha256(leaf.encode()).hexdigest() for leaf in self.leaves]
        tree = [leaves]
        while len(leaves) > 1:
            if len(leaves) % 2 != 0:
                leaves.append(leaves[-1])
            new_level = []
            for i in range(0, len(leaves), 2):
                combined = leaves[i] + leaves[i+1]
                new_level.append(hashlib.sha256(combined.encode()).hexdigest())
            leaves = new_level
            tree.append(leaves)
        return tree

    def get_root(self):
        return self.tree[-1][0]