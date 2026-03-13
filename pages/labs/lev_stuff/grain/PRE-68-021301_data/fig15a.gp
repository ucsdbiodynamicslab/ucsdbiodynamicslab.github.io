set term post eps  enh color solid "Helvetica" 22
set bmargin 4.0
set lmargin 8.0

set output "fig15a.eps"

set xlabel "{/Symbol=24 r}"
set ylabel "{{/Symbol=24 s}^f}_{yx} / {/Symbol=24 s}_{yx}"
wg(x) = (1-x)**2.5


set key 0.85,0.8 spacing 1.5 width -19  box
set label "{/Helvetica=32 a}" at 0.85, 0.93
set pointsize 1.5


set xrange [0:1]
set yrange [0:1]
plot \
     '<paste VC_50x100_S0.05_P10_fcSyx VC_50x100_S0.05_P10_rSyx VC_50x100_S0.05_P10_Syx VC_50x100_S0.05_P10_op '  u ($8):($0>1?($2+$4)/($6):0/0)   t "  P10V5"  w p 1 7,\
     '<paste VC_50x100_S0.5_P10_fcSyx  VC_50x100_S0.5_P10_rSyx  VC_50x100_S0.5_P10_Syx  VC_50x100_S0.5_P10_op'    u ($8):($0>1?($2+$4)/($6):0/0)   t "  P10V50" w p 2 9,\
     '<paste VC_50x100_S0.05_P50_fcSyx VC_50x100_S0.05_P50_rSyx VC_50x100_S0.05_P50_Syx VC_50x100_S0.05_P50_op '  u ($8):($0>1?($2+$4)/($6):0/0)   t "  P50V5"  w p 3 11,\
     '<paste VC_50x100_S0.5_P50_fcSyx  VC_50x100_S0.5_P50_rSyx  VC_50x100_S0.5_P50_Syx  VC_50x100_S0.5_P50_op'    u ($8):($0>1?($2+$4)/($6):0/0)   t "  P50V50" w p 4 13,\
      wg(x)  title "  (1-{/Symbol=24 r})^{2.5}" w l lt -1 lw 2



!gv fig15a.eps&
