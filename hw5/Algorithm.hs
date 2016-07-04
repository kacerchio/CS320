---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2015
-- Assignment 5 (skeleton code)
-- Algorithm.hs
--

module Algorithm where

import Graph

type Algorithm a = Graph a -> Graph a


-- Complete Problem #4, parts (a-f).

greedy :: Ord a => Algorithm a
greedy (Choices a (g1, g2)) = if Outcome (g1) < Outcome (g2) then g1 else g2

patient :: Ord a => Integer -> Algorithm a
patient (0) (g                )  = g
patient (n) (Choices a (g1, g2)) = minimum ([(patient (n - 1) g1), (patient (n - 1) g2)])

optimal :: (State a, Ord a) => Algorithm a
optimal a = minimum (outcomes a)

metaCompose :: Algorithm a -> Algorithm a -> Algorithm a
metaCompose a1 a2 g = (a1 . a2) (g)

metaRepeat :: Integer -> Algorithm a -> Algorithm a
metaRepeat 0 a g = g
metaRepeat 1 a g = a(g)
metaRepeat n a g = metaRepeat (n - 1) a (a(g))

metaGreedy :: Ord a => Algorithm a -> Algorithm a -> Algorithm a
metaGreedy a1 a2 g = minimum ([a1(g), a2(g)])

-- Problem #4, part (g).
impatient :: Ord a => Integer -> Algorithm a
impatient n g = (metaRepeat n greedy) g

{--

Superior: There are less expensive comparisons and recursive calls in
impatient than patient. This means that it is generally more optimal
and will have a faster run time.

Inferior: Compared to patient, impatient may not always return the best
allocation at depth n. This is because patient definitely looks through
the entire tree at that specified depth while impatient essentially
only considers a path of the tree.

--}


---------------------------------------------------------------------
-- Problem #6 (extra extra credit).

-- An embedded language for algorithms.
data Alg =
    Greedy
  | Patient Integer
  | Impatient Integer
  | Optimal
  | MetaCompose Alg Alg
  | MetaRepeat Integer Alg
  | MetaGreedy Alg Alg
  deriving (Eq, Show)

--interpret :: (State a, Ord a) => Alg -> Algorithm a
--interpret _ = \g -> g -- Replace for Problem #6, part (a).

data Time =
    N Integer 
  | Infinite
  deriving (Eq, Show)

--instance Num Time where
--   ... Complete for Problem #6, part (b).

--performance :: Alg -> Time
--performance _ = N 0 -- Replace for Problem #6, part (c).


--eof