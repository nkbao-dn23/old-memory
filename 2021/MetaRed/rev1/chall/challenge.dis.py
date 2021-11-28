  1           0 LOAD_CONST               0 (0)
              2 LOAD_CONST               1 (None)
              4 IMPORT_NAME              0 (math)
              6 STORE_NAME               0 (math)

  2           8 LOAD_CONST               0 (0)
             10 LOAD_CONST               1 (None)
             12 IMPORT_NAME              1 (requests)
             14 STORE_NAME               1 (requests)

  3          16 LOAD_CONST               0 (0)
             18 LOAD_CONST               1 (None)
             20 IMPORT_NAME              2 (hashlib)
             22 STORE_NAME               2 (hashlib)

  4          24 LOAD_CONST               0 (0)
             26 LOAD_CONST               2 (('AES',))
             28 IMPORT_NAME              3 (Crypto.Cipher)
             30 IMPORT_FROM              4 (AES)
             32 STORE_NAME               4 (AES)
             34 POP_TOP

  5          36 LOAD_CONST               0 (0)
             38 LOAD_CONST               1 (None)
             40 IMPORT_NAME              5 (base64)
             42 STORE_NAME               5 (base64)

  7          44 LOAD_CONST               3 (<code object _pad at 0x7fcef8818190, file "challenge.py", line 7>)
             46 LOAD_CONST               4 ('_pad')
             48 MAKE_FUNCTION            0
             50 STORE_NAME               6 (_pad)

 11          52 LOAD_CONST               5 (<code object main at 0x7fcef8818240, file "challenge.py", line 11>)
             54 LOAD_CONST               6 ('main')
             56 MAKE_FUNCTION            0
             58 STORE_NAME               7 (main)
             60 LOAD_CONST               1 (None)
             62 RETURN_VALUE

Disassembly of <code object _pad at 0x7fcef8818190, file "challenge.py", line 7>:
  8           0 LOAD_CONST               1 (16)
              2 STORE_FAST               1 (bs)

  9           4 LOAD_FAST                0 (s)
              6 LOAD_FAST                1 (bs)
              8 LOAD_GLOBAL              0 (len)
             10 LOAD_FAST                0 (s)
             12 CALL_FUNCTION            1
             14 LOAD_FAST                1 (bs)
             16 BINARY_MODULO
             18 BINARY_SUBTRACT
             20 LOAD_GLOBAL              1 (chr)
             22 LOAD_FAST                1 (bs)
             24 LOAD_GLOBAL              0 (len)
             26 LOAD_FAST                0 (s)
             28 CALL_FUNCTION            1
             30 LOAD_FAST                1 (bs)
             32 BINARY_MODULO
             34 BINARY_SUBTRACT
             36 CALL_FUNCTION            1
             38 BINARY_MULTIPLY
             40 BINARY_ADD
             42 RETURN_VALUE

Disassembly of <code object main at 0x7fcef8818240, file "challenge.py", line 11>:
 12           0 LOAD_GLOBAL              0 (requests)
              2 LOAD_METHOD              1 (get)
              4 LOAD_CONST               1 ('https://cdimage.kali.org/kali-2020.4/kali-linux-2020.4-installer-amd64.iso')
              6 CALL_METHOD              1
              8 STORE_FAST               0 (a)

 13          10 LOAD_GLOBAL              2 (hashlib)
             12 LOAD_METHOD              3 (sha256)
             14 CALL_METHOD              0
             16 STORE_FAST               1 (m)

 14          18 LOAD_FAST                1 (m)
             20 LOAD_METHOD              4 (update)
             22 LOAD_FAST                0 (a)
             24 LOAD_ATTR                5 (content)
             26 CALL_METHOD              1
             28 POP_TOP

 15          30 LOAD_GLOBAL              6 (int)
             32 LOAD_FAST                1 (m)
             34 LOAD_METHOD              7 (hexdigest)
             36 CALL_METHOD              0
             38 LOAD_CONST               2 (16)
             40 CALL_FUNCTION            2
             42 STORE_FAST               0 (a)

 17          44 LOAD_FAST                0 (a)
             46 LOAD_CONST               3 (2941460046203168433808698735326701052265551841195155278226402)
             48 BINARY_FLOOR_DIVIDE
             50 STORE_FAST               2 (limit)

 19          52 LOAD_CONST               4 (0)
             54 STORE_FAST               3 (n1)

 20          56 LOAD_GLOBAL              8 (range)
             58 LOAD_FAST                2 (limit)
             60 CALL_FUNCTION            1
             62 GET_ITER
        >>   64 FOR_ITER                20 (to 86)
             66 STORE_FAST               4 (i)

 21          68 LOAD_FAST                3 (n1)
             70 LOAD_FAST                4 (i)
             72 LOAD_CONST               5 (2)
             74 BINARY_MULTIPLY
             76 LOAD_CONST               6 (1)
             78 BINARY_SUBTRACT
             80 INPLACE_ADD
             82 STORE_FAST               3 (n1)
             84 JUMP_ABSOLUTE           64

 22     >>   86 LOAD_GLOBAL              9 (print)
             88 LOAD_FAST                3 (n1)
             90 CALL_FUNCTION            1
             92 POP_TOP

 23          94 LOAD_CONST               4 (0)
             96 STORE_FAST               5 (n2)

 24          98 LOAD_GLOBAL              8 (range)
            100 LOAD_FAST                3 (n1)
            102 CALL_FUNCTION            1
            104 GET_ITER
        >>  106 FOR_ITER                26 (to 134)
            108 STORE_FAST               4 (i)

 25         110 LOAD_FAST                5 (n2)
            112 LOAD_GLOBAL             10 (math)
            114 LOAD_METHOD             11 (floor)
            116 LOAD_FAST                4 (i)
            118 LOAD_CONST               5 (2)
            120 BINARY_TRUE_DIVIDE
            122 CALL_METHOD              1
            124 LOAD_CONST               5 (2)
            126 BINARY_MULTIPLY
            128 INPLACE_ADD
            130 STORE_FAST               5 (n2)
            132 JUMP_ABSOLUTE          106

 27     >>  134 LOAD_GLOBAL             12 (hex)
            136 LOAD_FAST                5 (n2)
            138 CALL_FUNCTION            1
            140 LOAD_CONST               5 (2)
            142 LOAD_CONST               0 (None)
            144 BUILD_SLICE              2
            146 BINARY_SUBSCR
            148 LOAD_METHOD             13 (encode)
            150 CALL_METHOD              0
            152 STORE_FAST               6 (key)

 28         154 LOAD_GLOBAL             14 (AES)
            156 LOAD_METHOD             15 (new)
            158 LOAD_FAST                6 (key)
            160 LOAD_CONST               0 (None)
            162 LOAD_CONST               2 (16)
            164 BUILD_SLICE              2
            166 BINARY_SUBSCR
            168 LOAD_GLOBAL             14 (AES)
            170 LOAD_ATTR               16 (MODE_ECB)
            172 CALL_METHOD              2
            174 STORE_FAST               7 (cipher)

 30         176 LOAD_GLOBAL             17 (_pad)
            178 LOAD_GLOBAL             18 (open)
            180 LOAD_CONST               7 ('flag.txt')
            182 CALL_FUNCTION            1
            184 LOAD_METHOD             19 (read)
            186 CALL_METHOD              0
            188 CALL_FUNCTION            1
            190 LOAD_METHOD             13 (encode)
            192 LOAD_CONST               8 ('utf8')
            194 CALL_METHOD              1
            196 STORE_FAST               8 (raw)

 31         198 LOAD_FAST                7 (cipher)
            200 LOAD_METHOD             20 (encrypt)
            202 LOAD_FAST                8 (raw)
            204 CALL_METHOD              1
            206 STORE_FAST               9 (encrypted)

 32         208 LOAD_GLOBAL             21 (base64)
            210 LOAD_METHOD             22 (b64encode)
            212 LOAD_FAST                9 (encrypted)
            214 CALL_METHOD              1
            216 STORE_FAST              10 (encoded)

 33         218 LOAD_GLOBAL              9 (print)
            220 LOAD_FAST               10 (encoded)
            222 CALL_FUNCTION            1
            224 POP_TOP

 34         226 LOAD_FAST               10 (encoded)
            228 LOAD_METHOD             23 (decode)
            230 CALL_METHOD              0
            232 LOAD_CONST               9 ('zoCeKfVqUw66ErPWhOWnPSmHq5h6rnofsrLkkwgQcDnEnvJMtWgaXSg6KYOSFG+i')
            234 COMPARE_OP               2 (==)
            236 POP_JUMP_IF_FALSE      246

 35         238 LOAD_GLOBAL              9 (print)
            240 LOAD_CONST              10 ('Correct Password! Ricardo Narvaja is proud of you!')
            242 CALL_FUNCTION            1
            244 POP_TOP
        >>  246 LOAD_CONST               0 (None)
            248 RETURN_VALUE
