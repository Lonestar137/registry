#define _LARGEFILE64_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#define SHM_NAME "/test_shm"
#define SHM_SIZE 4096

int main() {
    int shm_fd;
    void *shm_ptr;

    // Create a shared memory object
    shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(EXIT_FAILURE);
    }

    // Set the size of the shared memory object
    if (ftruncate64(shm_fd, SHM_SIZE) == -1) {
        perror("ftruncate64");
        exit(EXIT_FAILURE);
    }

    // Map the shared memory object into the address space
    shm_ptr = mmap64(NULL, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shm_ptr == MAP_FAILED) {
        perror("mmap64");
        exit(EXIT_FAILURE);
    }

    // Write some data to the shared memory
    sprintf(shm_ptr, "Hello, shared memory!");

    // Display the contents of the shared memory
    printf("Contents of shared memory: %s\n", (char*)shm_ptr);

    // Unmap and close the shared memory object
    if (munmap(shm_ptr, SHM_SIZE) == -1) {
        perror("munmap");
        exit(EXIT_FAILURE);
    }
    if (close(shm_fd) == -1) {
        perror("close");
        exit(EXIT_FAILURE);
    }

    return 0;
}
