module Exhaustive where

import Error
import AbstractSyntax
import Parse
import TypeCheck
import Interpret
import Compile
import Machine

type Height = Integer
type Quantity = Integer

class Exhaustive a where
  exhaustive :: Integer -> [a]

-- Complete for Problem 4, part (b).
instance Exhaustive Stmt where
  exhaustive 0 = []
  exhaustive 1 = [End]
  exhaustive n = [Print e s | e <- (exhaustive(n - 1) :: [Exp]), s <- (exhaustive(n - 1)) :: [Stmt]] ++
                 [Assign X e s | e <- (exhaustive(n - 1) :: [Exp]), s <- (exhaustive(n - 1)) :: [Stmt]] ++
                 [Assign Y e s | e <- (exhaustive(n - 1) :: [Exp]), s <- (exhaustive(n - 1)) :: [Stmt]]

 -- Complete for Problem 4, part (b).
instance Exhaustive Exp where
  exhaustive 0 = []
  exhaustive 1 = [Variable X, Variable Y, Value True, Value False]
  exhaustive n = [And e1 e2 | e1 <- (exhaustive(n - 1) :: [Exp]), e2 <- (exhaustive(n - 1)) :: [Exp]] ++
                 [Or e1 e2 | e1 <- (exhaustive(n - 1) :: [Exp]), e2 <- (exhaustive(n - 1)) :: [Exp]]

take' :: Integer -> [a] -> [a]
take' n (x:xs) = x:(take' (n-1) xs)
take' 0 _      = []
take' _ _      = []

validate :: Height -> Quantity -> Bool
validate n k = False -- Complete for Problem 4, part (c).

complete :: String -> ErrorOr Buffer
complete _ = TypeError "Complete for Problem 4, part (d)."

--
-- Could not get this function to compile because tokenizeParse returns an
-- ErrorOr Stmt but compileSimulate expects a Stmt. Wasn't sure how to resolve this.

--complete s = if (check [] (tokenizeParse (s))) == Result TyVoid then compileSimulate(tokenizeParse (s))
             --else liftType(check [] (tokenizeParse (s)))

--eof