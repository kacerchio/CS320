module Compile where

import Error
import AbstractSyntax
import TypeCheck
import Machine

-- Complete for Problem 4, part (a).
convert :: Value -> Integer
convert b = if b == True then 1 else 0

-- Complete for Problem 4, part (a).
converts :: Output -> Buffer
converts os = map convert os

type AddressEnvironment = [(Var, Address)]

addressVar :: Var -> AddressEnvironment -> Address
addressVar x' ((x,a):xas) = if x == x' then a else addressVar x xas

class Compilable a where
  compile :: AddressEnvironment -> a -> [Instruction]

-- Complete for Problem 3, part (a).
instance Compilable Exp where

  compile env (Variable var) = let addr = addressVar var env in [SET 3 8, SET 4 addr, COPY]

  compile env (Value val) = if val == True then [SET 8 1] else [SET 8 0]

  compile env (And e1 e2) =
    let [insts1] = compile env e1
        [insts2] = compile env e2
    in [insts1] ++ [SET 3 (size e1 + 8), SET 4 1] ++ [insts2] ++
       [SET 3 (size e2 + 8), SET 4 2, COPY, MUL, SET 3 0, SET 4 (size (And e1 e2) + 8), COPY]

  compile env (Or e1 e2) =
    let [insts1] = compile env e1
        [insts2] = compile env e2
    in [insts1] ++ [SET 3 (size e1 + 8), SET 4 1] ++ [insts2] ++
       [SET 3 (size e2 + 8), SET 4 2, COPY, ADD, SET 3 0, SET 4 (size (And e1 e2) + 8), COPY]

-- Complete for Problem 3, part (a).
instance Compilable Stmt where

  compile env (End) = []

  compile env (Print exp stmt) =
    let [insts1] = compile env exp
        [insts2] = compile env stmt
    in [insts1] ++ [SET 3 8, SET 4 5, COPY] ++ [insts2]

  compile env (Assign var exp stmt) =
    let [insts1] = compile env exp
        [insts2] = compile env stmt
        addr = addressVar var env
    in [SET 3 8, SET 4 addr, COPY] ++ [insts1] ++ [SET 3 8, SET 4 5, COPY] ++ [insts2]

compileSimulate  :: Stmt -> ErrorOr Buffer
compileSimulate s = if check [] s == Result TyVoid then Result (simulate (compile [] s)) else liftType(check [] s)

liftType :: ErrorOr Type -> ErrorOr Buffer
liftType (TypeError s) = TypeError s

--eof