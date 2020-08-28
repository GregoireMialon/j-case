from collections import defaultdict, Counter


class MoleculeParser:

    def __init__(self):
        super().__init__()
        self.left_brackets = ['(', '[', '{']
        self.right_brackets = [')', ']', '}']
    
    def push(self, obj, l, depth):
        while depth:
            l = l[-1]
            depth -= 1
        l.append(obj)

    def parse_lower(self, mol):
        parsed = []
        i = len(mol) - 1
        while i >= 0:
            if mol[i].islower():
                parsed.append(mol[i - 1] + mol[i])
                i -= 1
            else:
                parsed.append(mol[i])
            i -= 1
        parsed.reverse()
        return parsed

    def parse_parentheses(self, mol):
        groups = []
        depth = 0
        try:
            for char in mol:
                if char in self.left_brackets:
                    self.push([], groups, depth)
                    depth += 1
                elif char in self.right_brackets:
                    depth -= 1
                else:
                    self.push(char, groups, depth)
        except IndexError:
            raise ValueError('Parentheses mismatch')
        if depth > 0:
            raise ValueError('Parentheses mismatch')
        else:
            return groups

    def parse_mol(self, mol):
        expanded_mol = []
        if isinstance(mol, str):
            expanded_mol.append(mol)
        else:
            i = len(mol) - 1
            while i >= 0:
                if isinstance(mol[i], list):
                    expanded_mol += self.parse_mol(mol[i])
                else:
                    if mol[i].isdigit():
                        expanded_mol += self.parse_mol(
                        mol[i - 1]) * int(mol[i])
                        i -= 1
                    else:
                        expanded_mol.append(mol[i])
                i -= 1
        return expanded_mol

    def output(self, mol):
        parsed_lower = self.parse_lower(mol)
        parsed_parentheses = self.parse_parentheses(parsed_lower)
        parsed_mol = self.parse_mol(parsed_parentheses)
        return dict(Counter(parsed_mol).items())

if __name__ == "__main__":
    parser = MoleculeParser()
    # mol = 'Mg2[(OH]2]3'
    mol = 'K4[ON(SO3)2]2'
    print('Output', parser.output(mol))