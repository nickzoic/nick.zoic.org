#include <assert.h>
#include <dirent.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/mount.h>
#include <sys/reboot.h>

#define REF_ALIGN (8)
typedef uint32_t ref_t;
#define MAX_SIZE ((unsigned long long)REF_ALIGN << (sizeof(ref_t)*8))

uint8_t MAGIC[] = { 0xc0, 0xd1, 0xf1, 0xed, 0xed, 0x1f, 0x1c, 0xe5 };

void *MMAP = NULL;
size_t MMAP_SIZE = 0;

#define REF_TO_PTR(ref) (void *)((ref) ? MMAP + (ref) * REF_ALIGN : NULL)
#define PTR_TO_REF(ptr) (ref_t)((ptr) ? ((ptr) - MMAP) / REF_ALIGN : 0 )
#define SIZE_REFS(size) ((size+REF_ALIGN-1)/REF_ALIGN)

#define ROOT_REF ((ref_t)SIZE_REFS(sizeof(MAGIC)))
#define FREE_REF (ROOT_REF+1)

void die(char *message) {
    fprintf(stderr, "%s: %s (%d)\n", message, strerror(errno), errno);
    exit(1);
}

#define STRINGIZE(x) STRINGIZE2(x)
#define STRINGIZE2(x) #x
#define DIE(message) die(__FILE__ ":" STRINGIZE(__LINE__) ": " message)

int initialize_mmap() {
        if (mount("devtmpfs", "/dev", "devtmpfs", 0, NULL)) DIE("Couldn't mount /dev");

        int fd = open("/dev/sda", O_RDWR);
	if (fd<0) DIE("Couldn't open /dev/sda");
	
	if (ioctl(fd, BLKGETSIZE64, &MMAP_SIZE)) DIE("Couldn't get device size");
	if (MMAP_SIZE > MAX_SIZE) MMAP_SIZE = MAX_SIZE;

	MMAP = mmap(NULL, MMAP_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
	if (MMAP == MAP_FAILED) DIE("Couldn't mmap");
	
	if (memcmp(MMAP, MAGIC, sizeof(MAGIC))) DIE("Incorrect magic number");

	if (*(ref_t *)REF_TO_PTR((FREE_REF)) == 0)
	    *(ref_t *)REF_TO_PTR((FREE_REF)) = ROOT_REF+2;
}

void sync_and_reboot() {
    msync(MMAP, MMAP_SIZE, MS_SYNC);
    reboot(RB_AUTOBOOT);
}

static inline ref_t ptr_to_ref(void *ptr) {
    if (!ptr) return 0;
    assert(ptr > MMAP);
    assert(ptr < MMAP + MMAP_SIZE);
    assert((ptr-MMAP) % REF_ALIGN == 0);
    return (ptr-MMAP) / REF_ALIGN;
}

static inline void *ref_to_ptr(ref_t ref) {
    if (!ref) return NULL;
    assert(ref < MMAP_SIZE / REF_ALIGN);
    return (ref * REF_ALIGN) + MMAP;
}

ref_t allocate(size_t size) {
    size_t alloc_size = (size+REF_ALIGN-1)/REF_ALIGN;
    ref_t ref = *(ref_t *)REF_TO_PTR(FREE_REF);
    *(ref_t *)REF_TO_PTR(FREE_REF) += alloc_size;
    bzero(ref_to_ptr(ref), alloc_size*REF_ALIGN);
    return ref;
}
  
typedef struct {
    ref_t left;
    ref_t right;
    int count;
    char text[1024];
} node_t;

void print_tree(node_t *node_ptr) {
    if (!node_ptr) return;
    if (node_ptr->left) print_tree(ref_to_ptr(node_ptr->left));
    printf("%s %d\n", node_ptr->text, node_ptr->count);
    if (node_ptr->right) print_tree(ref_to_ptr(node_ptr->right));
}

ref_t new_node(char *text) {
    ref_t ref = allocate(sizeof(node_t)-1024+strlen(text));
    node_t *node = ref_to_ptr(ref);
    node->count = 1;
    strcpy(node->text, text);
    return ref;
}

void insert_tree(node_t *node_ptr, char *text) {
    int cmp = strcmp(text, node_ptr->text);
    if (cmp < 0) {
        if (node_ptr->left) insert_tree(ref_to_ptr(node_ptr->left), text);
	else node_ptr->left = new_node(text);
    } else if (cmp > 0) {
        if (node_ptr->right) insert_tree(ref_to_ptr(node_ptr->right), text);
	else node_ptr->right = new_node(text);
    } else {
	node_ptr->count++;
    }
}

void main() {
    printf("Hello from init.c again!\n");
    initialize_mmap();
    printf("Mapped %ld bytes at %p\n", MMAP_SIZE, MMAP);

    node_t *root = ref_to_ptr(*(ref_t *)ref_to_ptr(ROOT_REF));
    print_tree(root);

    char text[1024];
    while (fgets(text, sizeof(text), stdin)) {
	if (text[0] == '\0' || text[0] == '\n') break;
	text[strlen(text)-1] = 0;
	if (root) {
	    insert_tree(root, text);
	} else {
	    root = ref_to_ptr(new_node(text));
            *(ref_t *)ref_to_ptr(ROOT_REF) = ptr_to_ref(root);
	}
    }

    print_tree(root);
    sync_and_reboot();
}

