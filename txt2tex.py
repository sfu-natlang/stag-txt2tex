# TODO
# - parse tree structure, so that input file can have nicely indented trees
# - generate all trees in one forest environment? then adjunction arrows are easier to draw using tikz named nodes
# - for STAG pairs: find bottom-left corner of source, bottom right corner of target, and give them special labels. then draw STAG brackets/MCsets with a method like the following:
#
#	\path[draw=none] let \p1=(bottomleft.south), \p2=(bottomright.south) in (bottomright.east|-\pgfmath{min(\y1, \y2)}) -- coordinate[midway](right1) (bottomright.east|-srcroot.north);
#	\path[draw=none] let \p1=(bottomleft.south), \p2=(bottomright.south) in (bottomleft.west|-\pgfmath{min(\y1,\y2)}) -- coordinate[midway](left1) (bottomleft.west|-srcroot.north);
#	\draw let \p1=(srcroot.north), \p2=(bottomleft.south), \p3=(bottomright.south), \n1={(\y1-min(\y2,\y3)) / 2} in (left1) node {\resizebox{\abw}{\n1}{$\biggl<$}};
#	\draw let \p1=(srcroot.north), \p2=(bottomleft.south), \p3=(bottomright.south), \n1={(\y1-min(\y2,\y3)) / 2} in (right1) node {\resizebox{\abw}{\n1}{$\biggr>$}};
#

import sys, re
import argparse

parser = argparse.ArgumentParser(description='Generate LaTeX trees from bracketed representations.')
parser.add_argument('-p', dest='preamble', action='store_true', help='Include preamble (macro definitions and \\usepackage{}s)?')
parser.add_argument('-f', dest='path', help='Path to file containing trees.' )
 

args = parser.parse_args()

preamble = """
\\usepackage{adjustbox}
\\usepackage{forest}

% Boxed/circled numbers, for drawing linked nodes:
\\newcommand{\\circled}[1]{\\textcircled{\\scalebox{0.8}{#1}}}

% (Adapted from) Dennis's STAG angle brackets:
\\newlength{\\abw}
\\settowidth{\\abw}{$\\biggl<$}
\\newsavebox{\\mybox}
\\newcommand{\\bigabx}[1]{%
    \\savebox{\\mybox}{#1}%
    \\resizebox{\\abw}{\\ht\\mybox}{$\\biggl<$}%
    \\raisebox{.25\\ht\\mybox}{\\usebox{\\mybox}}%
    \\resizebox{\\abw}{\\ht\\mybox}{$\\biggr>$}%
}

% STAG tree-pair
\\newcommand{\\stagrule}[2]{
    \\bigabx{
        \\begin{adjustbox}{valign=M}
            \\begin{forest}
            #1
            \\end{forest}
        \\end{adjustbox}
        ,
        \\begin{adjustbox}{valign=M}
            \\begin{forest}
            #2
            \\end{forest}
        \\end{adjustbox}
    }
}

% Forest format: makes branches connect at the bottom
% of a node:
\\forestset{
    default preamble={
		for tree={
			parent anchor=south,
			child anchor=north,
			align=center,
		}
    }
}
"""

f = open( args.path )
s = f.read()
f.close()
s = s.split('\n')

if args.preamble:
  print( preamble )

for line in s:
  line = line.strip()
  if line == '':
    continue
  (src_tree, tgt_tree) = line.split('#')
  src_tree = re.sub( r"\((\d+)\)", r"\\circled{\1}", src_tree )
  tgt_tree = re.sub( r"\((\d+)\)", r"\\circled{\1}", tgt_tree )
  print( "\stagrule{"+src_tree+"}{"+tgt_tree+"}" )
