# N35 preregistration (#48 robustness): matched narrow diagnostic at nalpha = 32

Same inputs, matching and narrow domain as N29 (reference401 fit, Wout 0f2b626c) and N30 (selected401 fit, substitute
Wout 3d5df9a4); only nalpha 16 -> 32 (registered alternative resolution). Script = N29 with nalpha as an argument.
Report: target-launch and matched narrow scores per fit and the selected-vs-reference difference under each.
Robustness rule (fixed now): the N29/N30 conclusion "difference largely vanishes when matched" holds if
|matched difference| <= 1/3 of |target-launch difference| at nalpha 32; otherwise report it as resolution-sensitive.
Budget <= 3 h, one thread, sequential.
