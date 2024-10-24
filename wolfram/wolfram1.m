(* Mathematica Source File *)
(* Created by the Wolfram Language Plugin for IntelliJ, see http://wlplugin.halirutan.de/ *)
(* :Author: j.siedersleben *)
(* :Date: 2024-04-19 *)

horner1 := Function[coeff, Function[x, Fold[#1*x+#2 &, coeff]]];
horner2 := Function[coeff, Function[x, Fold[Function[{a, b}, a x+b], coeff]]];
horner3 := Function[x, Fold[Function[{a, b}, a x+b], #]]&;
horner4 := Function[x, Fold[(#1 x + #2 &), #]]&;
(* horner5 := coeff |-> (x |->Fold[{a, b} |-> a x + b, coeff]); *)

horners = {horner1, horner2, horner3, horner4};
coeff = {2, 3, 4};

(#@coeff)@200& /@ horners;
(* (f |->f[coeff][200])/@ horners; *)

gcd[a_Integer, 0] := a;
gcd[a_Integer, b_Integer]:= gcd[b, Mod[a, b]];

gcd@@@{{20, 16}, {16, 30}, {16, 32}, {16, 48}, {16, 90}};