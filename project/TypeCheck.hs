module TypeCheck where

import Error
import AbstractSyntax

type TypeEnvironment = [(Var, Type)]

typeVar :: Var -> TypeEnvironment -> ErrorOr Type
typeVar x' ((x,t):xvs) = if x == x' then Result t else typeVar x' xvs
typeVar x'  _          = TypeError (show x' ++ " is not bound.")

class Typeable a where
  check :: TypeEnvironment -> a -> ErrorOr Type

instance Typeable Stmt where

    check env (Print exp stmt) =
        if check env (exp) == Result TyBool
            then if check env (stmt) == Result TyVoid
                then Result TyVoid
                else TypeError ("Incompatible types.")
            else check env (exp)

    check env (Assign var exp stmt) =
        if var == X || var == Y
            then if check env (exp) == Result TyBool
                then if check env (stmt) == Result TyVoid
                    then Result TyVoid
                    else TypeError ("Incompatible types.")
                else check env (exp)
            else typeVar var env

    check env (End) = Result TyVoid

instance Typeable Exp where

    check env (Variable var) = typeVar var env

    check env (Value _) = Result TyBool

    check env (And e1 e2) =
        if (check env (e1) == Result TyBool) && (check env (e2) == Result TyBool) then Result TyBool
        else TypeError ("Incompatible types.")

    check env (Or e1 e2) =
        if (check env (e1) == Result TyBool) && (check env (e2) == Result TyBool) then Result TyBool
        else TypeError ("Incompatible types.")

typeCheck :: Typeable a => a -> ErrorOr (a, Type)
typeCheck ast = liftErr (\t -> (ast, t)) (check [] ast) -- Pair result with its type.

--eof