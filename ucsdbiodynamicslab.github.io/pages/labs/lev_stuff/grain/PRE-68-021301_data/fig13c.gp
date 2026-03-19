set term post eps  enh color solid "Helvetica" 22
set bmargin 4.0
set lmargin 11.0
set output "fig13c.eps"

#set grid
set xlabel "y"
set ylabel "( T_{xx} + T_{yy} ) / 2"

set logscale y
set key 40, 80.6 Left spacing 1.2  box
set label "{/Helvetica=32 c}" at 83, 270.93


set xrange [0:]
set yrange [:750]
plot \
     '<paste VC_50x100_S0.05_P10_Tyy VC_50x100_S0.05_P10_Txx'  u ($1):($0>1?(($4+$2)*0.5):0/0)    t "  P10V5"  w lp lt 1 lw 5 pt 4  ps 1.5,\
     '<paste VC_50x100_S0.5_P10_Tyy  VC_50x100_S0.5_P10_Txx'   u ($1):($0>1?(($4+$2)*0.5):0/0)    t "  P10V50" w lp lt 2 lw 5 pt 6  ps 1.5,\
     '<paste VC_50x100_S0.05_P50_Tyy VC_50x100_S0.05_P50_Txx'  u ($1):($0>1?(($4+$2)*0.5):0/0)    t "  P50V5"  w lp lt 3 lw 5 pt 8  ps 1.5,\
     '<paste VC_50x100_S0.5_P50_Tyy  VC_50x100_S0.5_P50_Txx'   u ($1):($0>1?(($4+$2)*0.5):0/0)    t "  P50V50" w lp lt 4 lw 5 pt 10 ps 1.5



!gv fig13c.eps&
