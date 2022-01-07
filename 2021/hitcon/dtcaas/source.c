#include <sys/stat.h>
#include <sys/wait.h>

#include "dtc.h"
#include "srcpos.h"
@ -159,6 +160,48 @@ static const char *guess_input_format(const char *fname, const char *fallback)
	return guess_type_by_name(fname, fallback);
}

static void writefile(const char *fname)
{
	size_t sz;
	static char buf[4096];
	FILE *f;

	setbuf(stdout, NULL);
	puts("Size?");
	if (scanf("%lu", &sz) != 1)
		die("?");
	if (sz <= 0 || sz > sizeof(buf))
		die("No");
	puts("Data?");
	if (fread(buf, 1, sz, stdin) != sz)
		die("eof");

	f = fopen(fname, "wb");
	if (!f)
		die("Open file %s failed", fname);
	if (fwrite(buf, 1, sz, f) != sz)
		die("Write file %s failed", fname);
	fclose(f);
}

static char *serve(const char *tmpdir)
{
	static char file[30];

	for (int i = 0; i < 2; i++) {
		if (fork() == 0) {
			sprintf(file, "%s/%d", tmpdir, i);
			writefile(file);
			return file;
		} else {
		  wait(NULL);
		}
	}
	exit(0);
	// unreachable
	return NULL;
}

int main(int argc, char *argv[])
{
	struct dt_info *dti;
		fprintf(depfile, "%s:", outname);
	}

	arg = serve(arg);
	if (inform == NULL)
		inform = guess_input_format(arg, "dts");
	if (outform == NULL) {
