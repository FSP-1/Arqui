/****************************************************************
 *
 * ppm.h
 *
 * Read and write PPM files.  Only works for "raw" format.
 *
 * AF970205
 *
 ****************************************************************/

#ifndef PPM_H
#define PPM_H

#include <sys/types.h>

typedef struct Image
{
  int width;
  int height;
  u_char *data;
  int channels;
} Image;

Image *ImageCreate(int width, int height, int channels);
Image *ImageRead(char *filename);
void   ImageWrite(Image *image, char *filename);

#endif /* PPM_H */


