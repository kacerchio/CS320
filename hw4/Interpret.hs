---------------------------------------------------------------------
--
-- Kristel Tan (ktan@bu.edu)
-- CAS CS 320, Fall 2015
-- Assignment 4 (skeleton code)
-- Interpret.hs
--

type Value = Integer
type Output = [Value]

data Term =
    Number Integer
  | Plus Term Term
  | Mult Term Term
  | Exponent Term Term
  | Max Term Term
  | Min Term Term

data Stmt =
    Print Term Stmt
  | End

evaluate :: Term -> Value
evaluate (Number t1     ) = t1
evaluate (Plus t1 t2    ) = evaluate(t1) + evaluate(t2)
evaluate (Mult t1 t2    ) = evaluate(t1) * evaluate(t2)
evaluate (Exponent t1 t2) = evaluate(t1) ^ evaluate(t2)
evaluate (Max t1 t2     ) = maximum[evaluate(t1), evaluate(t2)]
evaluate (Min t1 t2     ) = minimum[evaluate(t1), evaluate(t2)]
evaluate _ = 0

execute :: Stmt -> Output
execute (Print t s) = [evaluate(t)] ++ execute(s)
execute _ = []

--eof