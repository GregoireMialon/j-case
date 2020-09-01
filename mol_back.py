from collections import defaultdict, Counter


class MoleculeParser:

    def __init__(self):
        super().__init__()
        self.left_brackets = ['(', '[', '{']
        self.right_brackets = [')', ']', '}']
        self.error_message = 'it seems that your molecule is not valid. Use regular atoms, indexing and avoid parentheses mismatch'
        self.succes_message = 'it seems that your molecule contains '
    
    def push(self, obj, l, depth):
        while depth:
            l = l[-1]
            depth -= 1
        l.append(obj)

    def parse_lower_and_int(self, mol):
        parsed = []
        i = len(mol) - 1
        while i >= 0:
            if mol[i].islower():
                parsed.append(mol[i - 1] + mol[i])
                i -= 1
            elif mol[i].isdigit():
                digit = mol[i]
                while mol[i - 1].isdigit():
                    digit = mol[i - 1] + digit
                    i -= 1
                parsed.append(digit)
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
            # raise ValueError('Parentheses mismatch')
            return False
        if depth > 0:
            # raise ValueError('Parentheses mismatch')
            return False
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
    
    def is_valid(self, mol, mol_dic):
        if mol[0].isdigit():
            return False
        else:
            for element in mol_dic:
                if len(element) == 1:
                    if element.isupper():
                        pass
                    else:
                        return False
                elif len(element) == 2:
                    if element[0].isupper() and element[1].islower():
                        pass
                    else:
                        return False
                else:
                    return False
            return True
    
    def nice_output(self, mol_dic):
        output = ''
        compt = 0
        for atom in mol_dic:
            output += str(mol_dic[atom]) + ' ' + atom
            compt += 1
            if compt == len(mol_dic):
                pass
            elif compt == len(mol_dic) - 1:
                output += ', and '
            else:
                output += ', '
        return self.succes_message + output
    
    def parse(self, mol):
        parsed_lower_and_int = self.parse_lower_and_int(mol)
        parsed_parentheses = self.parse_parentheses(parsed_lower_and_int)
        if parsed_parentheses == False:
            return self.error_message
        parsed_mol = self.parse_mol(parsed_parentheses)
        return dict(Counter(parsed_mol).items())

    def output(self, mol):
        mol_dic = self.parse(mol)
        if self.is_valid(mol, mol_dic):
            return self.nice_output(mol_dic)
        else:
            return self.error_message

if __name__ == "__main__":
    # quick tests
    parser = MoleculeParser()
    # mol = 'H2Ol982'
    # mol = 'Mg2[(OH]2]3H2'
    mol = 'K4[(ON(S(Ol)23)2]2'
    print('Output', parser.parse(mol))