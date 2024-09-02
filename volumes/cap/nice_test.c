#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <unistd.h>

int main() {
  int ret;

  printf("Attempting to set high priority...\n");

  ret = setpriority(PRIO_PROCESS, 0, -20);
  if (ret == -1) {
    perror("setpriority failed");
    return 1;
  }

  printf("Priority set successfully. Current priority: %d\n",
         getpriority(PRIO_PROCESS, 0));

  printf("Sleeping for 60 seconds...\n");
  sleep(60);

  return 0;
}
