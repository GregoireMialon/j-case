from mol_back import MoleculeParser


class TestMoleculeParser:

    def test_basic_molecules(self):
        parser = MoleculeParser()
        mol = 'H2Og'
        assert parser.parse(mol) == {'H': 2, 'Og': 1}
    
    def test_nested(self):
        parser = MoleculeParser()
        mol = 'K4[ON((SO3})2]2'
        assert parser.parse(mol) == {'K': 4, 'O': 14, 'N': 2, 'S': 4}
    
    def test_two_digits(self):
        parser = MoleculeParser()
        mol = 'K40[OMn((SO3})2]2'
        assert parser.parse(mol) == {'K': 40, 'O': 14, 'Mn': 2, 'S': 4}

    def test_invalid_atom(self):
        parser = MoleculeParser()
        mol = 'Kol40[OM2]2'
        assert parser.output(mol) == parser.error_message

    def test_invalid_stoechio(self):
        parser = MoleculeParser()
        mol = '1Kol40[OM2]2'
        assert parser.output(mol) == parser.error_message
    
    def test_invalid_par(self):
        parser = MoleculeParser()
        mol = '[(OM2]2'
        assert parser.output(mol) == parser.error_message