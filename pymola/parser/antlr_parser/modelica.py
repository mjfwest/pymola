#!/usr/bin/env python
"""
Modelica compiler.
"""
from __future__ import print_function
import sys
import antlr4
import antlr4.Parser
from generated.ModelicaLexer import ModelicaLexer
from generated.ModelicaParser import ModelicaParser
from generated.ModelicaListener import ModelicaListener
import argparse
import re
from pprint import pprint

#pylint: disable=invalid-name, no-self-use, missing-docstring

class TraceListener(ModelicaListener):

    def __init__(self, parser):
        self._parser = parser
        self._ctx = None

    def enterEveryRule(self, ctx):
        self._ctx = ctx
        print(" "*ctx.depth(), "enter   " +
              self._parser.ruleNames[ctx.getRuleIndex()] + ", LT(1)=" +
              self._parser._input.LT(1).text)

    def visitTerminal(self, node):
        print(" "*self._ctx.depth() + "consume " + str(node.symbol) +
              " rule " + self._parser.ruleNames[self._ctx.getRuleIndex()])

    def visitErrorNode(self, node):
        pass

    def exitEveryRule(self, ctx):
        print(" "*ctx.depth(), "exit    " + self._parser.ruleNames[ctx.getRuleIndex()] +
              ", LT(1)=" + self._parser._input.LT(1).text)


class DictConverter(ModelicaListener):

    def __init__(self):
        self.tree_property = {}
        self.d = None;

    def getValue(self, node):
        return self.tree_property[node]

    def setValue(self, node, value):
        self.tree_property[node] = value

    def exitEveryRule(self, ctx):
        val = {}
        d_ctx = dict(ctx.__dict__)
        for key in d_ctx.keys():
            if re.match('l_.*', key):
                data = None
                key_name = key[2:]
                try:
                    # see if dict already has value for child
                    data = self.getValue(d_ctx[key])
                except KeyError as e:
                    try:
                        # no value in dict, see if token and has text
                        data = d_ctx[key].text
                    except AttributeError as e:
                        if d_ctx[key] is None:
                            data = None
                except TypeError as e:
                    # this is a list, hanlde appropriately
                    data = d_ctx[key]

                if data is not None:
                    val[key_name] = data
                else:
                    val[key_name] = data

        self.setValue(ctx, val)

    def exitStored_definition(self, ctx):
        self.d = self.getValue(ctx.children[0])

def main(argv):
    #pylint: disable=unused-argument
    "The main function"
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    text = antlr4.FileStream(args.filename)
    lexer = ModelicaLexer(text)
    stream = antlr4.CommonTokenStream(lexer)
    parser = ModelicaParser(stream)
    tree = parser.stored_definition()
    # print(tree.toStringTree(recog=parser))
    dictConverter = DictConverter()
    walker = antlr4.ParseTreeWalker()
    walker.walk(dictConverter, tree)

    pprint(dictConverter.d)

    # trace = TraceListener(parser)
    # walker.walk(trace, tree)

if __name__ == '__main__':
    main(sys.argv)

# vim: set et ft=python fenc=utf-8 ff=unix sts=0 sw=4 ts=4 :
