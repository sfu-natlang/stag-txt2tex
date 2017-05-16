# TODO
# - generate all trees in one forest environment? then adjunction arrows are easier to draw using tikz named nodes
# - for STAG pairs: find bottom-left corner of source, bottom right corner of target, and give them special labels. then draw STAG brackets/MCsets with a method like the following:
#
#       \path[draw=none] let \p1=(bottomleft.south), \p2=(bottomright.south) in (bottomright.east|-\pgfmath{min(\y1, \y2)}) -- coordinate[midway](right1) (bottomright.east|-srcroot.north);
#       \path[draw=none] let \p1=(bottomleft.south), \p2=(bottomright.south) in (bottomleft.west|-\pgfmath{min(\y1,\y2)}) -- coordinate[midway](left1) (bottomleft.west|-srcroot.north);
#       \draw let \p1=(srcroot.north), \p2=(bottomleft.south), \p3=(bottomright.south), \n1={(\y1-min(\y2,\y3)) / 2} in (left1) node {\resizebox{\abw}{\n1}{$\biggl<$}};
#       \draw let \p1=(srcroot.north), \p2=(bottomleft.south), \p3=(bottomright.south), \n1={(\y1-min(\y2,\y3)) / 2} in (right1) node {\resizebox{\abw}{\n1}{$\biggr>$}};
#

import sys, re
import argparse

parser = argparse.ArgumentParser(description='Generate LaTeX trees from bracketed representations.')
parser.add_argument('-p', dest='preamble', action='store_true', help='Include preamble (macro definitions and \\usepackage{}s)?')
parser.add_argument('-s', dest='scale', type=float, default=0.6, help='scale the box containing the entire figure by this much')
parser.add_argument('-c', dest='circle', action='store_true', help='Circle links? (default behavior puts links in boxes)')
parser.add_argument('-f', dest='path', help='Path to file containing trees.' )
 
args = parser.parse_args()

def parseNamedTree( s ):
  s = s.strip()
  if s == '':
    raise ValueError("should not call parseNamedTree with an empty string")
  if s[0] == '{':
    return ( ('',) + parseMCSet( s ) )
  elif s[0] == '[':
    return ( ('',) + parseTree( s ) )
  else:
    name, rest = s.split(' ', 1)
    #print "name:", name
    #print "rest:", rest
    return ( (name,) + parseTree( rest ) )  

def parseMCSet( s ):
  #print "entering parseMCSet"
  if s[0] != '{':
    raise ValueError("bad input for MCSet")
  rest = s[1:]
  (left_name, rest, left_tree) = parseNamedTree(rest)
  (right_name, rest, right_tree) = parseNamedTree(rest)
  rest = rest.strip()
  if rest[0] != '}':
    raise ValueError("bad input for MCSet")
  rest = rest[1:] # remove closing curly bracket
  mcset = ''
  if left_name is not '' and right_name is not '':
      mcset = r'\namedmcset{'+left_name+'}{'+left_tree+'}{'+right_name+'}{'+right_tree+'}'
  else:
      mcset = r'\mcset{'+left_tree+'}{'+right_tree+'}'
  return (rest, mcset)

def parseTree( s ):
  return parseTree_( s, 0, '' )

def parseTree_( s, openBraces, tree ):
  char = s[0]
  if char == '[':
    return parseTree_( s[1:], openBraces+1, tree+char )
  elif char == ']':
    if openBraces-1 == 0:
      return (s[1:], tree+char)
    else:
      return parseTree_( s[1:], openBraces-1, tree+char )
  else:
    return parseTree_( s[1:], openBraces, tree+char )

preamble = """
\\usepackage{adjustbox}
\\usepackage{forest}
\\usepackage{amsmath}

% Boxed/circled numbers, for drawing linked nodes:
\\newcommand{\\circled}[1]{\\textcircled{\\scalebox{0.8}{#1}}}
\\renewcommand{\\boxed}[1]{\\raisebox{1pt}{\\scalebox{0.65}{\\fbox{#1}}}}


% Draw the angled brackets around the STAG tree-pair
\\newlength{\\abw}
\\settowidth{\\abw}{$\\biggl<$}
\\newsavebox{\\mybox}
\\newcommand{\\bigabx}[1]{%
    \\savebox{\\mybox}{#1}%
    \\resizebox{\\abw}{\\ht\\mybox}{$\\biggl<$}%
    \\raisebox{.25\\ht\\mybox}{\\usebox{\\mybox}}%
    \\resizebox{\\abw}{\\ht\\mybox}{$\\biggr>$}%
}

% Draw the curly brackets around the STAG MC sets
\\newlength{\\acw}
\\settowidth{\\acw}{$\\biggl\\{$}
\\newsavebox{\\cbox}
\\newcommand{\\bigacx}[1]{%
    \\savebox{\\cbox}{#1}%
    \\resizebox{\\acw}{\\ht\\cbox}{$\\biggl\\{$}%
    \\raisebox{.25\\ht\\cbox}{\\usebox{\\cbox}}%
    \\resizebox{\\acw}{\\ht\\cbox}{$\\biggr\\}$}%
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

% Named STAG tree-pair
\\newcommand{\\namedstagrule}[4]{
    \\bigabx{
        \\begin{adjustbox}{valign=M}
            \\begin{forest}
            [,phantom,s sep=0
                [#1:]
                #2
            ]
            \\end{forest}
        \\end{adjustbox}
        ,
        \\begin{adjustbox}{valign=M}
            \\begin{forest}
            [,phantom,s sep=0
                [#3:]
                #4
            ]
            \\end{forest}
        \\end{adjustbox}
    }
}

% Named STAG MCSet tree-pair
\\newcommand{\\namedstagmcset}[3]{
    \\bigabx{
        \\begin{adjustbox}{valign=M}
            \\begin{forest}
            [,phantom,s sep=0
                [#1:]
                #2
            ]
            \\end{forest}
        \\end{adjustbox}
        ,
        \\begin{adjustbox}{valign=M}
            #3
        \\end{adjustbox}
    }
}

% STAG MCSet pair
\\newcommand{\\mcset}[2]{
    \\bigacx{
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

% Named STAG MCSet pair
\\newcommand{\\namedmcset}[4]{
    \\bigacx{
        \\begin{adjustbox}{valign=M}
            \\begin{forest}
            [,phantom,s sep=0
                [#1:]
                #2
            ]
            \\end{forest}
        \\end{adjustbox}
        ,
        \\begin{adjustbox}{valign=M}
            \\begin{forest}
            [,phantom,s sep=0
                [#3:]
                #4
            ]
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

header = r'\begin{adjustbox}{scale=' + str(args.scale) + r'}'
footer = r'\end{adjustbox}'

f = open( args.path )
s = f.read()
s = s.replace("\t", " ")
s = s.replace("\n", " ")
f.close()

if args.preamble:
  print( preamble )

print(header)
while s.strip() != '':
  if s == '': 
    break
  else:
    #print "s:", s
    print 
  try:
    (src_name, s, src_tree) = parseNamedTree(s)
    (tgt_name, s, tgt_tree) = parseNamedTree(s)
  except IndexError:
    print('Couldn\'t parse tree! Are there are even number of trees in the input file?')
  link_annotation = r"\\circled{\1}" if args.circle else r"\\boxed{\1}"
  src_tree = re.sub( r"\((\d+)\)", link_annotation, src_tree.strip() )
  tgt_tree = re.sub( r"\((\d+)\)", link_annotation, tgt_tree.strip() )
  if src_name != '' and tgt_name != '':
      print( r'\namedstagrule{'+src_name+'}{'+src_tree+'}{'+tgt_name+'}{'+tgt_tree+'}' )
  elif src_name != '' and tgt_name == '':
      print( r'\namedstagmcset{'+src_name+'}{'+src_tree+'}{'+tgt_tree+'}' )
  else:
      print( r'\stagrule{'+src_tree+'}{'+tgt_tree+'}' )
print(footer)
