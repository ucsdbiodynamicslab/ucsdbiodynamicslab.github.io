# I link -Bstatic because I run my httpd server with a fairly restricted
# environment

LIBS= -lucb
LDFLAGS= -L/usr/ucblib -Bstatic
CC= gcc

#	cc -o nph-animate nph-animate.o $(LDFLAGS) $(LIBS)
	gcc -o nph-animate nph-animate.o
nph-animate: nph-animate.o

