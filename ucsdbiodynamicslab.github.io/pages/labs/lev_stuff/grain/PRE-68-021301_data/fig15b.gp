set term post eps  enh color solid "Helvetica" 22
set bmargin 4.0
set lmargin 8.0

set output "fig15b.eps"

set xlabel "{/Symbol=24 r}"
set ylabel "{{/Symbol=24 s}^{@{f}}_{yy}} _ {{/Symbol=24 s}^{@{}}_{yy}}\ ,\ \ {{/Symbol=24 s}^{@{f}}_{xx}} _ {{/Symbol=24 s}^{@{}}_{xx}}"
wyy(x) = (1-x)**2.5
wxx(x) = (1-x**1.2)**1.9


set key 0.85,0.8 Left spacing 1.5 width -23  box
set label "{/Helvetica=32 b}" at 0.85, 0.93
set pointsize 1.5


set xrange [0:1]
set yrange [0:1]
plot \
     '<paste VC_50x100_S0.05_P10_fcSyy VC_50x100_S0.05_P10_rSyy VC_50x100_S0.05_P10_Syy VC_50x100_S0.05_P10_op '  u ($8):($0>1?($2+$4)/($6):0/0)   t "" w p 1 6,\
     '<paste VC_50x100_S0.5_P10_fcSyy  VC_50x100_S0.5_P10_rSyy  VC_50x100_S0.5_P10_Syy  VC_50x100_S0.5_P10_op'    u ($8):($0>1?($2+$4)/($6):0/0)   t "" w p 2 8,\
     '<paste VC_50x100_S0.05_P50_fcSyy VC_50x100_S0.05_P50_rSyy VC_50x100_S0.05_P50_Syy VC_50x100_S0.05_P50_op '  u ($8):($0>1?($2+$4)/($6):0/0)   t "" w p 3 10,\
     '<paste VC_50x100_S0.5_P50_fcSyy  VC_50x100_S0.5_P50_rSyy  VC_50x100_S0.5_P50_Syy  VC_50x100_S0.5_P50_op'    u ($8):($0>1?($2+$4)/($6):0/0)   t "" w p 4 12,\
     '<paste VC_50x100_S0.05_P10_fcSxx VC_50x100_S0.05_P10_rSxx VC_50x100_S0.05_P10_Sxx VC_50x100_S0.05_P10_op '  u ($8):($0>1?($2+$4)/($6):0/0)   t "  P10V5"  w p 1 7,\
     '<paste VC_50x100_S0.5_P10_fcSxx  VC_50x100_S0.5_P10_rSxx  VC_50x100_S0.5_P10_Sxx  VC_50x100_S0.5_P10_op'    u ($8):($0>1?($2+$4)/($6):0/0)   t "  P10V50" w p 2 9,\
     '<paste VC_50x100_S0.05_P50_fcSxx VC_50x100_S0.05_P50_rSxx VC_50x100_S0.05_P50_Sxx VC_50x100_S0.05_P50_op '  u ($8):($0>1?($2+$4)/($6):0/0)   t "  P50V5"  w p  3 11,\
     '<paste VC_50x100_S0.5_P50_fcSxx  VC_50x100_S0.5_P50_rSxx  VC_50x100_S0.5_P50_Sxx  VC_50x100_S0.5_P50_op'    u ($8):($0>1?($2+$4)/($6):0/0)   t "  P50V50" w p  4 13,\
      wxx(x)  title "  (1-{/Symbol=24 r}^{1.2})^{1.9}" w l lt -1 lw 2,\
      wyy(x)  title "  (1-{/Symbol=24 r})^{2.5}" w l lt 1 lw 2



!gv fig15b.eps&
