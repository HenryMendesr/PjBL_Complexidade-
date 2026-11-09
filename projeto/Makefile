CC = gcc
CFLAGS = -std=c11 -O3 -Wall -Wextra -Wpedantic -Werror -fno-inline -fno-omit-frame-pointer -mno-red-zone -fno-tree-loop-distribute-patterns -fstack-usage
CPPFLAGS = -Isrc -Itests
OBJ = build/heap.o build/bitmap.o
.PHONY: all test math sanitize bench docs clean
all: build/benchmark build/test
build:
	mkdir -p build
build/%.o: src/%.c src/dedup.h | build
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@
build/benchmark: src/main.c tests/oracle.h $(OBJ)
	$(CC) $(CPPFLAGS) $(CFLAGS) $< $(OBJ) -o $@
build/test: tests/test.c tests/oracle.h $(OBJ)
	$(CC) $(CPPFLAGS) $(CFLAGS) $< $(OBJ) -o $@
test: build/test
	./build/test
sanitize: | build
	$(CC) $(CPPFLAGS) -std=c11 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer tests/test.c src/heap.c src/bitmap.c -o build/test_san
	ASAN_OPTIONS=detect_leaks=1 ./build/test_san
bench: all
	python3 scripts/experimentos.py
docs:
	MPLCONFIGDIR=/tmp/pjbl-mpl python3 scripts/documentos.py
clean:
	rm -rf build

math:
	python3 scripts/validar_matematica.py
