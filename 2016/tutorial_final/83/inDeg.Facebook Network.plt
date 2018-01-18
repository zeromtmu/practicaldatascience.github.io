#
# Facebook Network In-Degree. G(4039, 88234). 1314 (0.3253) nodes with in-deg > avg deg (43.7), 597 (0.1478) with >2*avg.deg (Tue Nov 01 03:20:37 2016)
#

set title "Facebook Network In-Degree. G(4039, 88234). 1314 (0.3253) nodes with in-deg > avg deg (43.7), 597 (0.1478) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "In-degree"
set ylabel "Count"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'inDeg.Facebook Network.png'
plot 	"inDeg.Facebook Network.tab" using 1:2 title "" with linespoints pt 6
