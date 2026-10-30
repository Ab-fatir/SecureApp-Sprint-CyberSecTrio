#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char magic[4];
    unsigned short version;
    unsigned short flags;
    unsigned int data_len;
} __attribute__((packed)) DocumentHeader;

int parse_document_header_vulnerable(const char* raw_data, size_t input_len, char* out_title, char* out_author) {
    char stack_author_buffer[32];
    char stack_title_buffer[48];
    
    if (input_len < sizeof(DocumentHeader)) {
        return -1;
    }
    
    const char* payload = raw_data + sizeof(DocumentHeader);
    
    strcpy(stack_author_buffer, payload);
    
    const char* title_ptr = payload + strlen(stack_author_buffer) + 1;
    if (title_ptr < (raw_data + input_len)) {
        strcpy(stack_title_buffer, title_ptr);
    } else {
        strcpy(stack_title_buffer, "Default Title");
    }
    
    strcpy(out_author, stack_author_buffer);
    strcpy(out_title, stack_title_buffer);
    
    return 0;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <input_payload>\n", argv[0]);
        return 1;
    }
    
    char out_title[128] = {0};
    char out_author[128] = {0};
    
    int ret = parse_document_header_vulnerable(argv[1], strlen(argv[1]), out_title, out_author);
    if (ret == 0) {
        printf("Author: %s\n", out_author);
        printf("Title:  %s\n", out_title);
    }
    return 0;
}
