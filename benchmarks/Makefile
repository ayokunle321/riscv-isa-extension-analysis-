# RISC-V cross-compilation toolchain
CC = riscv64-unknown-elf-gcc
CFLAGS = -O2 -march=rv64g -mabi=lp64d -static

# Directories
BASELINE_DIR = baseline
POPCOUNT_DIR = popcount
FMA_DIR = fma

# Baseline targets
BASELINE_SRCS = $(wildcard $(BASELINE_DIR)/*.c)
BASELINE_BINS = $(BASELINE_SRCS:.c=.elf)

all: baseline

baseline: $(BASELINE_BINS)

%.elf: %.c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f $(BASELINE_DIR)/*.elf $(POPCOUNT_DIR)/*.elf $(FMA_DIR)/*.elf

.PHONY: all baseline clean
