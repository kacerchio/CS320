module Interpret where

import Error
import AbstractSyntax
import TypeCheck

type ValueEnvironment = [(Var, Value)]

valueVar :: Var -> ValueEnvironment -> Value
valueVar x' ((x,v):xvs) = if x == x' then v else valueVar x' xvs

-- Complete for Problem 2, part (b).
evaluate :: ValueEnvironment -> Exp -> Value
evaluate env exp = fold (\var -> valueVar var env) (\var -> var) (\e1 e2 -> e1 && e2) (\e1 e2 -> e1 || e2) exp

-- Complete for Problem 2, part (b).

updateEnv :: Eq a => a -> b -> [(a, b)] -> [(a, b)]
updateEnv key val env = (key, val):(filter ((key /=).fst) env)

execute :: ValueEnvironment -> Stmt -> (ValueEnvironment, Output)

execute env (Print exp stmt) =
    let (env', o) = execute env (stmt) in (env', [evaluate env exp] ++ o)

execute env (Assign var exp stmt) =
    let v = evaluate env exp
        env1 = updateEnv var v env
        (env2, o) = execute env1 stmt
    in (env2, o)

execute env _ = (env, [])

interpret :: Stmt -> ErrorOr Output
interpret s = if (check [] s) == Result TyVoid then let (env, o) = execute [] s in Result o else lift(check [] s)

lift :: ErrorOr Type -> ErrorOr Output
lift (TypeError s) = TypeError s


--eof