#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char magic[4];
    unsigned short version;
    unsigned short flags;
    unsigned int data_len;
} __attribute__((packed)) DocumentHeader;

int parse_document_header_secure(
    const char* raw_data, 
    size_t input_len, 
    char* out_title, 
    size_t title_cap, 
    char* out_author, 
    size_t author_cap
) {
    if (!raw_data || !out_title || !out_author) {
        return -5;
    }
    
    if (input_len < sizeof(DocumentHeader)) {
        return -1;
    }
    if (input_len > 4096) {
        return -4;
    }
    
    const DocumentHeader* hdr = (const DocumentHeader*)raw_data;
    if (memcmp(hdr->magic, "CVLT", 4) != 0) {
        return -2;
    }
    
    size_t actual_payload_len = input_len - sizeof(DocumentHeader);
    if (hdr->data_len > actual_payload_len) {
        return -3;
    }
    
    const char* payload = raw_data + sizeof(DocumentHeader);
    size_t author_len = strnlen(payload, actual_payload_len);
    
    if (author_len >= author_cap) {
        author_len = author_cap - 1;
    }
    
    memcpy(out_author, payload, author_len);
    out_author[author_len] = '\0';
    
    if (author_len + 1 < actual_payload_len) {
        const char* title_ptr = payload + author_len + 1;
        size_t title_remaining = actual_payload_len - (author_len + 1);
        size_t title_len = strnlen(title_ptr, title_remaining);
        
        if (title_len >= title_cap) {
            title_len = title_cap - 1;
        }
        memcpy(out_title, title_ptr, title_len);
        out_title[title_len] = '\0';
    } else {
        snprintf(out_title, title_cap, "Untitled");
    }
    
    return 0;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <input_payload>\n", argv[0]);
        return 1;
    }
    
    char out_title[128] = {0};
    char out_author[64] = {0};
    
    int status = parse_document_header_secure(argv[1], strlen(argv[1]), out_title, sizeof(out_title), out_author, sizeof(out_author));
    if (status == 0) {
        printf("Author: %s\n", out_author);
        printf("Title:  %s\n", out_title);
    } else {
        printf("Rejected: code %d\n", status);
    }
    
    return status;
}
