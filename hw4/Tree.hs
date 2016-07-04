---------------------------------------------------------------------
--
-- Kristel Tan (ktan@bu.edu)
-- CAS CS 320, Fall 2015
-- Assignment 4 (skeleton code)
-- Tree.hs
--

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving(Eq, Show)

twigs :: Tree -> Integer
twigs (Leaf           ) = 0
twigs (Twig           ) = 1
twigs (Branch t1 t2 t3) = twigs(t1) + twigs(t2) + twigs(t3)

branches :: Tree -> Integer
branches (Leaf           ) = 0
branches (Twig           ) = 0
branches (Branch t1 t2 t3) = 1 + branches(t1) + branches(t2) + branches(t3)

width :: Tree -> Integer
width (Leaf           ) = 1
width (Twig           ) = 1
width (Branch t1 t2 t3) = width(t1) + width(t2) + width(t3)

perfect :: Tree -> Bool
perfect (Leaf                 ) = False
perfect (Twig                 ) = False
perfect (Branch Leaf Leaf Leaf) = True
perfect (Branch t1 t2 t3      ) = perfect(t1) && perfect(t2) && perfect(t3) && (t1 == t2) && (t2 == t3)

degenerate :: Tree -> Bool
degenerate (Leaf               ) = True
degenerate (Twig               ) = True
degenerate (Branch Leaf Leaf t3) = True && degenerate(t3)
degenerate (Branch Twig Twig t3) = True && degenerate(t3)
degenerate (Branch Leaf Twig t3) = True && degenerate(t3)
degenerate (Branch Twig Leaf t3) = True && degenerate(t3)
degenerate (Branch Leaf t2 Leaf) = True && degenerate(t2)
degenerate (Branch Twig t2 Twig) = True && degenerate(t2)
degenerate (Branch Leaf t2 Twig) = True && degenerate(t2)
degenerate (Branch Twig t2 Leaf) = True && degenerate(t2)
degenerate (Branch t1 Leaf Leaf) = True && degenerate(t1)
degenerate (Branch t1 Twig Twig) = True && degenerate(t1)
degenerate (Branch t1 Leaf Twig) = True && degenerate(t1)
degenerate (Branch t1 Twig Leaf) = True && degenerate(t1)
degenerate (_) = False

infinite :: Tree
infinite = Branch infinite infinite infinite

--eof