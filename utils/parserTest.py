# -*- coding: utf-8 -*-

# unit test for parser.parse

import parser
import unittest

class parserTest(unittest.TestCase):

    block = []
    # Defination
    block.append('array a')
    block.append('int a = 1+2')
    block.append('char a = \'a\'')
    block.append('function A(x, y)')
    # Statement
    block.append('if a == 1')
    block.append('while a >= 10')
    block.append('for a = 1 to 10, step 2')
    # PsudoExp
    # block.append('swap a[1], a[2]')
    # Exp
    block.append('a.revert()')
    block.append('s.push()')

    def test_lexical(self):
        for i in range(len(self.block)):
            tokens = parser.lexical(self.block[i])
            self.assertEqual(len(tokens[0]), 2)
            print('\n')
            print(tokens)

    def test_parse(self):
        for i in range(4):
            grammType, tokens, extoken, paramList = parser.parse(self.block[i], {}, {})
            self.assertEqual(grammType, 'defination')
            print('\n')
        for i in range(4, 7):
            grammType, token, extoken, paramList = parser.parse(self.block[i], {}, {})
            self.assertEqual(grammType, 'statement')
            print('\n')
        for i in range(7, 9):
            grammType, token, extoken, paramList = parser.parse(self.block[i], {}, {})
            self.assertEqual(grammType, 'exp')
            print('\n')

    def test_preprocess(self):
        infile = open(r'test1', 'r')
        strContent = ''.join(infile.readlines())
        content = parser.preprocess(strContent)
        print(content)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(parserTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
