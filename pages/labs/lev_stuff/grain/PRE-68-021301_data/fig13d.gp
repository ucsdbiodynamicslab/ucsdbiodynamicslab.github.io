set term post eps  enh color solid "Helvetica" 22
set bmargin 4.0
set lmargin 8.0

set output "fig13d.eps"

set xlabel "y"
set ylabel "{/Symbol=24 r}"

set key 25, 0.45 Left spacing 1.5 box
set label "{/Helvetica=32 d}" at 83, 0.93


set xrange [0:]
set yrange [0:1]
plot \
     'VC_50x100_S0.05_P10_op' u ($1):($0>1?($2):0/0)    t "  P10V5"  w lp  lt 1 lw 5 pt 4  ps 1.5,\
     'VC_50x100_S0.5_P10_op'  u ($1):($0>1?($2):0/0)    t "  P10V50" w lp  lt 2 lw 5 pt 6  ps 1.5,\
     'VC_50x100_S0.05_P50_op' u ($1):($0>1?($2):0/0)    t "  P50V5"  w lp  lt 3 lw 5 pt 8  ps 1.5,\
     'VC_50x100_S0.5_P50_op'  u ($1):($0>1?($2):0/0)    t "  P50V50" w lp  lt 4 lw 5 pt 10 ps 1.5



!gv fig13d.eps&
