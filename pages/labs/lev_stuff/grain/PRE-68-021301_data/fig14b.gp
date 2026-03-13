set term post eps  enh color solid "Helvetica" 22
set bmargin 4.0
set lmargin 8.0


set output "fig14b.eps"
set key 72, 80  Left samplen 2 spacing 1.5 width -25 title "    P20F10" box
set label "{/Helvetica=32 b}" at 75, 90


set xlabel "y"
set ylabel "components of  {/Symbol=24 s}_{xx}"
set yrange [0:]
plot \
'<paste FC_50x100_P20d0.5_rSxx FC_50x100_P20d0.5_fcSxx FC_50x100_P20d0.5_scSxx FC_50x100_P20d0.5_Sxx'  u ($1):($0>1?($2):0/0)    t "  {{/Symbol=24 s}^{@R}_{xx}}"     w lp lt 1 lw 5 pt 4  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSxx FC_50x100_P20d0.5_fcSxx FC_50x100_P20d0.5_scSxx FC_50x100_P20d0.5_Sxx'  u ($1):($0>1?($4):0/0)    t "  {{/Symbol=24 s}^{@{fc}}_{xx}}"  w lp lt 2 lw 5 pt 6  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSxx FC_50x100_P20d0.5_fcSxx FC_50x100_P20d0.5_scSxx FC_50x100_P20d0.5_Sxx'  u ($1):($0>1?($6):0/0)    t "  {{/Symbol=24 s}^{@{s}}_{xx}}"   w lp lt 3 lw 5 pt 8  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSxx FC_50x100_P20d0.5_fcSxx FC_50x100_P20d0.5_scSxx FC_50x100_P20d0.5_Sxx'  u ($1):($0>1?($8):0/0)    t "  {{/Symbol=24 s}_{xx}"           w lp lt 4 lw 5 pt 10 ps 1.5


!gv fig14b.eps&
