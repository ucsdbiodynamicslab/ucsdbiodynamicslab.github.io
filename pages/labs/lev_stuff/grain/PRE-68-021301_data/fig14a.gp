set term post eps  enh color solid "Helvetica" 22
set bmargin 4.0
set lmargin 8.0


set output "fig14a.eps"
set key 72, 82  Left samplen 2 spacing 1.5 width -25 title "    P20F10" box
set label "{/Helvetica=32 a}" at 75, 95

set xlabel "y"
set ylabel "components of  {/Symbol=24 s}_{yy}"
set yrange [0:105]
plot \
'<paste FC_50x100_P20d0.5_rSyy FC_50x100_P20d0.5_fcSyy FC_50x100_P20d0.5_scSyy FC_50x100_P20d0.5_Syy'  u ($1):($0>1?($2):0/0)    t "  {{/Symbol=24 s}^{@R}_{yy}}"     w lp lt 1 lw 5 pt 4  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSyy FC_50x100_P20d0.5_fcSyy FC_50x100_P20d0.5_scSyy FC_50x100_P20d0.5_Syy'  u ($1):($0>1?($4):0/0)    t "  {{/Symbol=24 s}^{@{fc}}_{yy}}"  w lp lt 2 lw 5 pt 6  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSyy FC_50x100_P20d0.5_fcSyy FC_50x100_P20d0.5_scSyy FC_50x100_P20d0.5_Syy'  u ($1):($0>1?($6):0/0)    t "  {{/Symbol=24 s}^{@{s}}_{yy}}"   w lp lt 3 lw 5 pt 8  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSyy FC_50x100_P20d0.5_fcSyy FC_50x100_P20d0.5_scSyy FC_50x100_P20d0.5_Syy'  u ($1):($0>1?($8):0/0)    t "  {{/Symbol=24 s}_{yy}"           w lp lt 4 lw 5 pt 10 ps 1.5


!gv fig14a.eps&
