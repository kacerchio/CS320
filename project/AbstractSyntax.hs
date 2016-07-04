module AbstractSyntax where

type Value = Bool
type Output = [Value]

data Var = X | Y deriving Eq

instance Show Var where
  show X = "x"
  show Y = "y"

data Stmt =
    Print Exp Stmt
  | Assign Var Exp Stmt
  | End
  deriving (Eq, Show)

data Exp =
    Variable Var
  | Value Bool
  | And Exp Exp
  | Or Exp Exp
  deriving (Eq, Show)

data Type =
    TyBool
  | TyVoid
  deriving (Eq, Show)

--fold :: (Var -> b) -> (Bool -> b) -> (b -> b -> b) -> (b -> b -> b) -> Exp -> b
-- Complete for Problem 1, part (c).
fold :: (Var -> b) -> (Bool -> b) -> (b -> b -> b) -> (b -> b -> b) -> Exp -> b
fold v b a o (Variable var) = v var
fold v b a o (Value val   ) = b val
fold v b a o (And e1 e2   ) = a (fold v b a o e1) (fold v b a o e2)
fold v b a o (Or e1 e2    ) = o (fold v b a o e1) (fold v b a o e2)

--size :: Exp -> Integer
-- Complete for Problem 1, part (c).
size :: Exp -> Integer
size e = fold (\e -> 1) (\e -> 1) (\e1 e2 -> 1 + e1 + e2) (\e1 e2 -> 1 + e1 + e2) e

--foldSmt :: (Exp -> b -> b) -> (Var -> Exp -> b -> b) -> b -> Stmt -> b
-- Complete for Problem 1, part (d).
foldStmt :: (Exp -> b -> b) -> (Var -> Exp -> b -> b) -> b -> Stmt -> b
foldStmt p a e (Print exp stmt     ) = p exp (foldStmt p a e stmt)
foldStmt p a e (Assign var exp stmt) = a var exp (foldStmt p a e stmt)
foldStmt p a e (End                ) = e

--eof