set term post eps  enh color solid "Helvetica" 22
set bmargin 4.0
set lmargin 8.0


set output "fig14c.eps"
set key 62, 18.5  Left samplen 2 spacing 1.5 width -25 title "    P20F10" box
set label "{/Helvetica=32 c}" at 75, 19

set xlabel "y"
set ylabel "components of - {/Symbol=24 s}_{yx}"
set yrange [-0.2:20]
plot \
'<paste FC_50x100_P20d0.5_rSyx FC_50x100_P20d0.5_fcSyx FC_50x100_P20d0.5_scSyx FC_50x100_P20d0.5_Syx'  u ($1):($0>1?(-$2):0/0)    t " - {{/Symbol=24 s}^{@R}_{yx}}"     w lp lt 1 lw 5 pt 4  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSyx FC_50x100_P20d0.5_fcSyx FC_50x100_P20d0.5_scSyx FC_50x100_P20d0.5_Syx'  u ($1):($0>1?(-$4):0/0)    t " - {{/Symbol=24 s}^{@{fc}}_{yx}}"  w lp lt 2 lw 5 pt 6  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSyx FC_50x100_P20d0.5_fcSyx FC_50x100_P20d0.5_scSyx FC_50x100_P20d0.5_Syx'  u ($1):($0>1?(-$6):0/0)    t " - {{/Symbol=24 s}^{@{s}}_{yx}}"   w lp lt 3 lw 5 pt 8  ps 1.5,\
'<paste FC_50x100_P20d0.5_rSyx FC_50x100_P20d0.5_fcSyx FC_50x100_P20d0.5_scSyx FC_50x100_P20d0.5_Syx'  u ($1):($0>1?(-$8):0/0)    t " - {{/Symbol=24 s}_{yx}"           w lp lt 4 lw 5 pt 10 ps 1.5


!gv fig14c.eps&
