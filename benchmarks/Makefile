# RISC-V cross-compilation toolchain
CC = riscv64-unknown-elf-gcc
CFLAGS = -O2 -march=rv64gc -mabi=lp64d -static

# Source files
SRCS = bfs.c factorial.c hash_lookup.c

# Output binaries
BINS = bfs_riscv factorial_riscv hash_lookup_riscv

.PHONY: all clean

all: $(BINS)

bfs_riscv: bfs.c
	$(CC) $(CFLAGS) $< -o $@
	@echo "✓ Built bfs_riscv"

factorial_riscv: factorial.c
	$(CC) $(CFLAGS) $< -o $@
	@echo "✓ Built factorial_riscv"

hash_lookup_riscv: hash_lookup.c
	$(CC) $(CFLAGS) $< -o $@
	@echo "✓ Built hash_lookup_riscv"

clean:
	rm -f $(BINS)
	@echo "✓ Cleaned all binaries"

# Build and verify
test: all
	@echo "=== Verifying RISC-V binaries ==="
	@file bfs_riscv
	@file factorial_riscv
	@file hash_lookup_riscv