---------------------------------------------------------------------
--
-- CAS CS 320, Fall 2015
-- Assignment 5 (skeleton code)
-- Graph.hs
-- Kristel Tan (ktan@bu.edu)
--

module Graph where


data Graph a =
    Choices a (Graph a, Graph a)
  | Outcome a
  deriving (Eq, Show)

class State a where
  outcome :: a -> Bool
  choices :: a -> (a, a)


--mapTuple :: (a -> b) -> (a, a) -> (b, b)
--  ... Complete for Problem #3, part (a) ...
mapTuple :: (a -> b) -> (a, a) -> (b, b)
mapTuple (f) (a1, a2) = (f(a1), f(a2))

--state :: (Graph a) -> a
--  ... Complete for Problem #3, part (b) ...
state :: (Graph a) -> a
state (Choices a (x, y)) = a
state (Outcome a       ) = a

-- If states can be compared, then graphs containing
-- those states can be compared by comparing the
-- states in the respective root nodes.
--  ... Complete for Problem #3, part (c) ...
instance Ord a => Ord (Graph a) where
  Outcome (g        ) <= Outcome (g'       ) = g <= g'
  Choices a1 (g1, g2) <= Choices a2 (g3, g4) = a1 <= a2
  Choices a1 (g1, g2) <= Outcome (a2       ) = a1 <= a2
  Outcome (a1       ) <= Choices a2 (g1, g2) = a1 <= a2


-- Complete Problem #3, parts (d-g).

--graph :: State a => a -> Graph a
--  ... Solution for Problem #3, part (d) ...
graph :: State a => a -> Graph a
graph (a) = if outcome (a) == True then (Outcome a) else Choices a (mapTuple graph (choices a))

--depths :: Integer -> Graph a -> [Graph a]
--  ... Solution for Problem #3, part (e) ...
depths :: Integer -> Graph a -> [Graph a]
depths 0 (Outcome a         ) = [Outcome a]
depths 0 (Choices a (g1, g2)) = [Choices a (g1, g2)]
depths i (Choices a (g1, g2)) = (depths (i - 1) (g1)) ++ (depths (i - 1) (g2))

--fold :: State a => (a -> b) -> (a -> (b, b) -> b) -> Graph a -> b
-- ... Solution for Problem #3, part (f) ...
fold :: State a => (a -> b) -> (a -> (b, b) -> b) -> Graph a -> b
fold o c (Outcome g) = o g
fold o c (Choices a (g1, g2)) = c a (fold o c g1, fold o c g2)

--outcomes :: State a => Graph a -> [Graph a]
-- ... Solution for Problem #3, part(g) ...
outcomes :: State a => Graph a -> [Graph a]
outcomes g = fold (\g -> [Outcome g]) (\x (y,z) -> y ++ z) g


--eof