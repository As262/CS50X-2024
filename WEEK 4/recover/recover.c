#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }
    FILE *raw = fopen(argv[1], "r");
    uint8_t buffer[512];
    bool found = false;
    int count = 0;
    char filename[8];
    FILE *image = NULL;
    while (fread(buffer, 1, 512, raw) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            found = true;
        }
        if (found == true)
        {
            if (count != 0)
            {
                fclose(image);
            }
            sprintf(filename, "%03i.jpg", count);
            image = fopen(filename, "w");
            fwrite(buffer, 1, 512, image);
            found = false;
            count++;
        }
        else if (count != 0)
        {
            fwrite(buffer, 1, 512, image);
        }
    }
    fclose(raw);
    fclose(image);
}
