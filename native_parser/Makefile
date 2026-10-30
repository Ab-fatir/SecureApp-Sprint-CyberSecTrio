CC = gcc
CFLAGS = -Wall -Wextra -std=c11

all: parser_vulnerable parser_secure libparser_secure.so

parser_vulnerable: metadata_parser_vulnerable.c
	$(CC) $(CFLAGS) -O0 -fno-stack-protector -z execstack metadata_parser_vulnerable.c -o parser_vulnerable

parser_secure: metadata_parser_secure.c
	$(CC) $(CFLAGS) -O2 -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE -pie -Wl,-z,relro,-z,now -Wl,-z,noexecstack metadata_parser_secure.c -o parser_secure

libparser_secure.so: metadata_parser_secure.c
	$(CC) $(CFLAGS) -O2 -fPIC -shared -fstack-protector-strong -D_FORTIFY_SOURCE=2 metadata_parser_secure.c -o libparser_secure.so

parser_asan: metadata_parser_vulnerable.c
	$(CC) $(CFLAGS) -g -O1 -fsanitize=address -fno-omit-frame-pointer metadata_parser_vulnerable.c -o parser_asan

clean:
	rm -f parser_vulnerable parser_secure parser_asan libparser_secure.so *.o
