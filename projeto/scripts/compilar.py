import argparse
import subprocess
from pathlib import Path

R=Path(__file__).resolve().parents[1]
FLAGS=['-std=c11','-O3','-Wall','-Wextra','-Wpedantic','-Werror',
       '-fno-inline','-fno-omit-frame-pointer','-mno-red-zone',
       '-fno-tree-loop-distribute-patterns','-fno-ipa-cp','-fstack-usage','-fPIC']


def compile_native(sanitize=False):
    build=R/'build'
    build.mkdir(exist_ok=True)
    subprocess.run(['gcc',*FLAGS,'-c','src/heap.c','-o','build/heap.o'],cwd=R,check=True)
    subprocess.run(['gcc','-shared','build/heap.o','-o','build/libheap.so'],cwd=R,check=True)
    subprocess.run(['gcc',*FLAGS,'tests/nativo.c','build/heap.o','-o','build/test_nativo'],cwd=R,check=True)
    subprocess.run([str(build/'test_nativo')],check=True)
    if sanitize:
        subprocess.run(['gcc','-std=c11','-O1','-g','-fsanitize=address,undefined',
                        '-fno-omit-frame-pointer','tests/nativo.c','src/heap.c',
                        '-o','build/test_sanitizado'],cwd=R,check=True)
        subprocess.run([str(build/'test_sanitizado')],check=True)
    print('Biblioteca C compilada; teste nativo independente de Python aprovado.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Compila Heap Sort C com GCC em Linux x86-64.')
    parser.add_argument('--sanitizers',action='store_true')
    args=parser.parse_args()
    compile_native(args.sanitizers)
