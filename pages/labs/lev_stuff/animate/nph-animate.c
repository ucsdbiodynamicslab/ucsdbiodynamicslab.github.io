#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

/*
 * This program was created by Paul Ramsey (pramsey@postmodern.com)
 * 
 * Last modified 30 July 1995
 *
 * This seems like an awfully simple program to put a copyright notice
 * on so I'll just say if you attempt to take credit for writing this
 * program ... shame on you.
 *
 * BUILDING ANIMATE
 *
 * This program was developed under Solaris for x86. I haven't tried
 * it on anything else yet. (let me know how it goes on your system).
 * Under Solaris you need to link in /usr/ucblib/libucb.a since I
 * couldn't find a replacement for usleep() in the standard Solaris
 * libraries. Otherwise this program is completely self contained.
 *
 *    
 * INSTALLING AND CONFIGURING

 * For better looking urls you might want to do some mapping of names.
 * I use the following lines httpd.conf for my CERN httpd server
 *
 *      Map	/animate/*	/cgi-bin/nph-animate
 *      Exec    /cgi-bin/*	/www/scripts/*
 *
 * Put the executable in the script directory as nph-animate. Using the
 * CERN server the name must begin with "nph-" so that the output will go
 * directly to the client without being buffered in the server. No shell is
 * needed.
 *
 * Animation files have the following format and must end with ".ani".
 * This make it easier to prevent arbitrary files from being passed to
 * the animate script.
 *
 *      filename1.gif	delay1
 *      filename2.gif	delay2
 *      filename3.gif	delay3
 *
 * The filename is relative to the animation file.
 *
 *
 * Using the example server configuration above the animation file
 * /www/arrow.ani would be execute with the URL
 * http://www.yourserver.com/animate/arrow.ani
 *
 * If the client is not Netscape then only the last frame is displayed
 */

#define RANDOMSTRING "PaulWasHere"

/*
 * Create a simple HTML document with the provided error message
 */
void error(char string[])
{
   printf("HTTP/1.0 200 OK\n");
   printf("Content-type: text/html\n");
   printf("\n");
   printf("<html>\n");
   printf("<head>\n");
   printf("<title>Animation Error</title>\n");
   printf("</head>\n");
   printf("<body>\n");
   printf("<h2>Error</h2>\n");
   printf("<p>%s</p>\n",string);
   printf("</body>\n");
   printf("</html>\n");
   exit(0);
}

/*
 * Create an error message for use in the middle of a multi-part document
 */
void multi_error(char string[])
{
   printf("Content-type: text/html\n");
   printf("\n");
   printf("<html>\n");
   printf("<head>\n");
   printf("<title>Animation Error</title>\n");
   printf("</head>\n");
   printf("<body>\n");
   printf("<h2>Error</h2>\n");
   printf("<p>%s</p>\n",string);
   printf("</body>\n");
   printf("</html>\n");
   printf("\n");
}

/*
 * copy the file to stdout (with a header)
 */
void copyout(char filename[])
{
   int infile;
   struct stat buf;
   char buffer[50000];
   int count;
   int chunksize;

   /* get the size of the file */
   if (stat(filename,&buf)) {
      sprintf(buffer,"Error getting the size of %s\n",filename);
      multi_error(buffer);
      return;
   }

   /* open the file */
   infile= open(filename,O_RDONLY);
   if (infile < 0) {
      sprintf(buffer,"Error opening %s\n",filename);
      multi_error(buffer);
      return;
   }

   /* write out the header */
   printf("Content-type: image/gif\n");
   printf("\n");

   count= buf.st_size;
   while (count) {
      if (count > sizeof(buffer)) {
         chunksize= sizeof(buffer);
      } else {
         chunksize= count;
      }

      /*
       * there isn't really anything reasonable to be done at this point
       * if the reads or writes fail so don't bother checking for errors
       */
      read(infile,buffer,chunksize);
      fwrite(buffer,chunksize,1,stdout);
      count-=chunksize;
   }
   close(infile);
}


/*
 * Write out only 1 file
 */
void other(FILE* list)
{
   char filename[500];
   int nextdelay;

   printf("HTTP/1.0 200 OK\n");

   /* go to the last filename */
   while (fscanf(list,"%499s %d",filename,&nextdelay)==2);

   copyout(filename);
}

/*
 * Write out the entire animation
 */
void netscape(FILE* list)
{
   char filename[500];
   int delay,nextdelay;

   /* send the multipart header */
   printf("HTTP/1.0 200 OK\n");
   printf("Content-type: multipart/x-mixed-replace;boundary=%s\n",RANDOMSTRING);
   printf("\n");

  
   /* if there are no files then send the end string */
   if (fscanf(list,"%499s %d",filename,&delay)!=2) {
      /* the boundary string should be followed by "--" if no more parts */
      printf("--%s--\n",RANDOMSTRING);
      return;
   }

   filename[499]=NULL; /* be sure the string is terminated */
   printf("--%s\n",RANDOMSTRING);

   /* loop through the list of gif files and send them */
   do {
      copyout(filename);

      /* get the next string/delay pair */
      if (fscanf(list,"%499s %d",filename,&nextdelay)!=2) break;

      /* send the boundary string */
      printf("\n--%s\n",RANDOMSTRING);

      /* make sure everything has been written */
      fflush(stdout);

      /* wait the specified amount of time */
      usleep(delay*1000);

      delay=nextdelay;
   } while (1);

   /* send the final boundary string */
   printf("\n--%s--\n",RANDOMSTRING);

   fclose(list);
}

main(argc,argv)
int argc;
char **argv;
{
   char *listname,list1[100],*p;
   char* clientname;
   char *ptr;
   FILE* list;
	int i;

   /* get the name of the animation file */
/*   listname= getenv("PATH_TRANSLATED"); */
	listname=argv[1]; 
   if (listname==NULL) error("No animation file specified");

   /* open the file it must end with .ani */
   ptr= strrchr(listname,'.');
   if (ptr==NULL) error("Specified file is not an animation file");
   if (strcmp(ptr,".ani")!=0) error("Specified file is not an animation file");
   list= fopen(listname,"r");
   if (list==NULL) error("Error reading animation file");

   /* change to the directory of the animation file */
   ptr= strrchr(listname,'/');
   if (ptr) {
i=0;
for(p=listname;p<ptr;p++)
	list1[i]=listname[i++];
/* *ptr=NULL; */
	list1[i]=NULL;
      chdir(list1);
   }

   /* get HTTP_USER_AGENT to see if this client can do multipart documents */
   clientname= getenv("HTTP_USER_AGENT");
   if (clientname==0) {
      other(list);
   } else if (strncmp(clientname,"Mozilla",7)==0) {
      netscape(list);
   } else {
      other(list);
   }
}
