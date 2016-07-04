module Error where

data ErrorOr a =
    Result a
  | ParseError String
  | TypeError String
  deriving Show

promote :: ErrorOr a -> ErrorOr b
promote (ParseError s     ) = ParseError s
promote (TypeError s      ) = TypeError s

--instance Eq a => Eq (ErrorOr a) where
-- Complete for Problem 1, part (a).
instance Eq a => Eq (ErrorOr a) where
    ParseError _ == ParseError _ = False
    TypeError  _ == TypeError  _ = False
    TypeError  _ == ParseError _ = False
    TypeError  _ == Result     _ = False
    Result    a1 == Result    a2 = a1 == a2

--liftErr :: (a -> b) -> (ErrorOr a -> ErrorOr b)
-- Complete for Problem 1, part (b).
liftErr :: (a -> b) -> (ErrorOr a -> ErrorOr b)
liftErr f (Result a)     = Result (f a)
liftErr f (ParseError s) = ParseError s
liftErr f (TypeError s)  = TypeError s

--joinErr :: ErrorOr (ErrorOr a) -> ErrorOr a
-- Complete for Problem 1, part (b).
joinErr :: ErrorOr (ErrorOr a) -> ErrorOr a
joinErr (Result (Result a))     = Result a
joinErr (Result (ParseError s)) = ParseError s
joinErr (Result (TypeError s))  = TypeError s

--eof