# N25 preregistration — nfp=2 existence from the other side (exploratory, #114)

Question: can ConStellaration's ALM-NGOpt raise QI (log10 <= -3.5) on nfp=2 dataset boundaries that already meet
W>=0, FC<=0.9, mirror<=0.25, |iota|>=0.25 at A in [8,10.5], while keeping those and A<=10?
Seeds (fixed before running): the 3 rows with lowest QI among the 11 qualifying nfp=2 rows of ConStellaration
default split revision 8da71572 (MIT): rows 57491 (DdT8PCJuXuVytJsDEAEz8Jy, log10QI -2.12), 48627 (-1.83),
79615 (-1.56). Settings as N24 (|iota| runner fix, maxit 10, budget 800+100, 6 workers, very_low_fidelity,
seed 123), modes 4/4 (= seeds' own resolution), 1.5 h wall per arm, sequential.
Outcome: any eval with normalized violation <= 1e-2 at A<=10 => "nfp=2 MHD-stable QI design found" (then
re-score at high fidelity, and check draft-v1 QI <= -4 separately). Otherwise report best violation, QI reached.
