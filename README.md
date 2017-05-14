# stag-txt2tex
Simple macros for converting bracketed trees into LaTeX STAG tree-pairs.

Usage:
python txt2tex.py (-p) -f filename

If -p is specified, the program will output a preamble containing macro definitions and \usepackage{} commands.

The input file should contain tree-pairs in a bracketed representation. Numbers in parentheses (1) will expand to circled link numbers. The following is a valid input file, which will expand into two tree-pairs:

```
[$C_B(2)$ 
	[$\alpha$]
	[$\beta(1)$]
]
[$C_B(2)$ 
	[$\alpha$ 
		[$\beta(1)$]
	]
]
[$C_B(2)$ [$\beta(1)$]][$C_B$ [$\alpha(2)$ [$\beta(1)$]]]
```

# To-do
- Generate all trees in one forest environment? Then adjunction arrows would be easier to draw using tikz named nodes.
- For STAG pairs: find bottom-left node of source, bottom right node of target, and give them special labels. Then draw STAG brackets/MCsets with a method like the following:
```
\path[draw=none] let \p1=(bottomleft.south), \p2=(bottomright.south) in (bottomright.east|-\pgfmath{min(\y1, \y2)}) -- coordinate[midway](right1) (bottomright.east|-srcroot.north);
\path[draw=none] let \p1=(bottomleft.south), \p2=(bottomright.south) in (bottomleft.west|-\pgfmath{min(\y1,\y2)}) -- coordinate[midway](left1) (bottomleft.west|-srcroot.north);
\draw let \p1=(srcroot.north), \p2=(bottomleft.south), \p3=(bottomright.south), \n1={(\y1-min(\y2,\y3)) / 2} in (left1) node {\resizebox{\abw}{\n1}{$\biggl<$}};
\draw let \p1=(srcroot.north), \p2=(bottomleft.south), \p3=(bottomright.south), \n1={(\y1-min(\y2,\y3)) / 2} in (right1) node {\resizebox{\abw}{\n1}{$\biggr>$}};
```
