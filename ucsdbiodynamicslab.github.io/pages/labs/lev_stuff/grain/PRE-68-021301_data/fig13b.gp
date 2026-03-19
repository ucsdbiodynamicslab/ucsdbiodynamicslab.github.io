set term post eps  enh color solid "Helvetica-Bold" 22
set bmargin 4.0
set lmargin 8.0

set output "fig13b.eps"

set xlabel "y"
set ylabel "V_x"

set key 40, 40.5 Left spacing 1.5  box
set label "{/Helvetica=32 b}" at 83, 40.93


set xrange [0:]
set yrange [0:]
plot \
     'VC_50x100_S0.05_P10_Vx' u ($1):($0>1?($2):0/0)    t "  P10V5"  w lp  lt 1 lw 5 pt 4  ps 1.5,\
     'VC_50x100_S0.5_P10_Vx'  u ($1):($0>1?($2):0/0)    t "  P10V50" w lp  lt 2 lw 5 pt 6  ps 1.5,\
     'VC_50x100_S0.05_P50_Vx' u ($1):($0>1?($2):0/0)    t "  P50V5"  w lp  lt 3 lw 5 pt 8  ps 1.5,\
     'VC_50x100_S0.5_P50_Vx'  u ($1):($0>1?($2):0/0)    t "  P50V50" w lp  lt 4 lw 5 pt 10 ps 1.5



!gv fig13b.eps&
