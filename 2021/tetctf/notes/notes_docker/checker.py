import sys
import os
from pathlib import Path

def binary_check(original_binary : Path, patched_binary : Path) -> bool:
    f1 = open(original_binary, 'rb')
    f2 = open(patched_binary, 'rb')

    origin_size = f1.seek(0, os.SEEK_END)
    patched_size = f2.seek(0, os.SEEK_END)

    f1.seek(0, os.SEEK_SET)
    f2.seek(0, os.SEEK_SET)

    while origin_size > 0 and patched_size > 0:
        b1 = f1.read(1)
        b2 = f2.read(1)

        if b1 != b2 and b2 != b'\x90':
            # only allow nop byte
            f1.close()
            f2.close()
            return False

        origin_size -= 1
        patched_size -= 1

    f1.close()
    f2.close()
    return True

def main() -> bool:
    try:
        original_binary = Path('./build/note')
        patched_binary = Path(sys.argv[1])
    except IndexError:
        print(f'Usage: {sys.argv[0]} <patched_binary>')
        return 1
    
    if not original_binary.exists():
        print('Unable to find "./build/note" binary')
        return 1

    if not patched_binary.exists():
        print(f'Patched binary {patched_binary} is not exists.')
        return 1

    res = binary_check(original_binary, patched_binary)
    if res:
        print('OK')
    else:
        print('Failure')

    return 0

if __name__ == '__main__':
    main()
