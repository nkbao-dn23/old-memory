  
  local_38 = DAT_140005008 ^ (ulonglong)auStackY504;
  local_1a8 = 0x6e6f;
  uStack422 = 0;
  local_1b8 = CONCAT412(0x73726564,CONCAT48(0x6e41202e,0x412073616d6f6854));
  local_145 = 0;
  local_13d = 0;
  local_139 = 0;
  auStack421 = SUB1613(ZEXT816(0),0);
  uStack408 = 0;
  auStack405 = SUB1613(ZEXT816(0),0);
  uStack392 = 0;
  local_185 = SUB1613(ZEXT816(0),0);
  uStack376 = 0;
  local_175 = SUB1613(ZEXT816(0),0);
  uStack360 = 0;
  local_165 = SUB1613(ZEXT816(0),0);
  uStack344 = 0;
  local_155 = SUB1613(ZEXT816(0),0);
  uStack328 = 0;
  inputFun("Enter your key:",param_2,param_3,param_4);
  FUN_140001080("%08x-%08x-%08x",local_1c0,&local_1c4,&local_1c8);
  pbVar9 = (byte *)0x0;
  DAT_140005654 = 0;
  DAT_140005640 = local_1c0[0];
  pbVar16 = (byte *)0xffffffffffffffff;
  DAT_140005644 = local_1c4;
  pbVar5 = (byte *)0xffffffffffffffff;
  DAT_140005648 = local_1c8;
  do {
    pbVar5 = pbVar5 + 1;
  } while (local_1b8[(longlong)pbVar5] != '\0');
  ans1 = pbVar9;
  pbVar11 = pbVar9;
  if (pbVar5 == (byte *)0x0) {
    _DAT_14000564c = 0;
  }
  else {
    do {
      pbVar13 = (byte *)(ulonglong)((int)pbVar11 + 1);
      uVar6 = (int)ans1 + (int)(char)local_1b8[(longlong)pbVar11];
      uVar6 = uVar6 >> 0xc | uVar6 * 0x100000;
      pbVar8 = pbVar9;
      ans1 = (byte *)(ulonglong)(uVar6 ^ 0x55aa);
      pbVar14 = pbVar9;
      pbVar11 = pbVar13;
    } while (pbVar13 < pbVar5);
    do {
      ans1 = (byte *)(ulonglong)((int)pbVar14 + 1);
      uVar7 = (int)pbVar8 + (int)(char)local_1b8[(longlong)pbVar14];
      uVar7 = uVar7 * 0x10000 | uVar7 >> 0x10;
      pbVar8 = (byte *)(ulonglong)(uVar7 ^ 0x3249);
      pbVar14 = ans1;
    } while (ans1 < pbVar5);
    _DAT_14000564c = CONCAT44(uVar7,uVar6) ^ 0x3249000055aa;
    ans1 = pbVar9;
    pbVar11 = pbVar9;
    do {
      pcVar1 = local_1b8 + (longlong)pbVar11;
      pbVar11 = (byte *)(ulonglong)((int)pbVar11 + 1);
      uVar6 = (int)ans1 + (int)*pcVar1;
      DAT_140005654 = (uVar6 * 0x100 | uVar6 >> 0x18) ^ 0x3773;
      ans1 = (byte *)(ulonglong)DAT_140005654;
    } while (pbVar11 < pbVar5);
  }
  ppvVar12 = &DAT_140005658;
  lVar18 = 4;
  ppvVar10 = &DAT_140005658;
  lVar17 = 4;
  do {
    pvVar4 = CreateEventW((LPSECURITY_ATTRIBUTES)0x0,0,0,(LPCWSTR)0x0);
    *ppvVar10 = pvVar4;
    ppvVar10 = ppvVar10 + 1;
    lVar17 = lVar17 + -1;
  } while (lVar17 != 0);
  DAT_140005638 = CreateEventW((LPSECURITY_ATTRIBUTES)0x0,0,0,(LPCWSTR)0x0);
  pvVar4 = CreateThread((LPSECURITY_ATTRIBUTES)0x0,0,(LPTHREAD_START_ROUTINE)&LAB_140001140,
                        (LPVOID)0x0,0,(LPDWORD)0x0);
  if (pvVar4 != (HANDLE)0x0) {
    SetEvent(DAT_140005658);
    WaitForSingleObject(pvVar4,0xffffffff);
    if ((DAT_140005638 != (HANDLE)0x0) && (DVar3 = WaitForSingleObject(DAT_140005638,0), DVar3 == 0)
       ) {
      local_1b8 = ZEXT816(0);
      local_1a8 = 0;
      uStack422 = 0;
      auStack421 = SUB1613(ZEXT816(0) >> 0x18,0);
      uStack408 = 0;
      auStack405 = SUB1613(ZEXT816(0) >> 0x18,0);
      uStack392 = 0;
      local_185 = SUB1613(ZEXT816(0) >> 0x18,0);
      uStack376 = 0;
      local_175 = SUB1613(ZEXT816(0) >> 0x18,0);
      uStack360 = 0;
      local_165 = SUB1613(ZEXT816(0) >> 0x18,0);
      uStack344 = 0;
      local_155 = SUB1613(ZEXT816(0) >> 0x18,0);
      uStack328 = 0;
      local_145 = SUB168(ZEXT816(0) >> 0x18,0);
      local_13d = 0;
      local_139 = 0;
      FUN_1400010e0(local_1b8,"%x.%x.%x",(ulonglong)local_1c0[0],(ulonglong)local_1c4);
      uVar15 = 0xffffffffffffffff;
      do {
        ans2 = uVar15 + 1;
        lVar17 = uVar15 + 1;
        uVar15 = ans2;
      } while (local_1b8[lVar17] != '\0');
      pbVar5 = local_138;
      lVar17 = 0x100;
      ans1 = pbVar9;
      do {
        *pbVar5 = (byte)ans1;
        pbVar5 = pbVar5 + 1;
        uVar6 = (int)ans1 + 1;
        ans1 = (byte *)(ulonglong)uVar6;
      } while ((int)uVar6 < 0x100);
      pbVar5 = local_138;
      pbVar11 = pbVar9;
      ans1 = pbVar9;
      do {
        bVar2 = *pbVar5;
        uVar6 = (int)ans1 + (int)(char)local_1b8[(ulonglong)pbVar11 % ans2] + (uint)bVar2 &
                0x800000ff;
        if ((int)uVar6 < 0) {
          uVar6 = (uVar6 - 1 | 0xffffff00) + 1;
        }
        ans1 = (byte *)(ulonglong)uVar6;
        pbVar11 = pbVar11 + 1;
        *pbVar5 = local_138[(int)uVar6];
        pbVar5 = pbVar5 + 1;
        local_138[(int)uVar6] = bVar2;
        lVar17 = lVar17 + -1;
      } while (lVar17 != 0);
      do {
        pbVar11 = pbVar16 + 1;
        pbVar5 = pbVar16 + 0x140005039;
        pbVar16 = pbVar11;
      } while (*pbVar5 != 0);
      pbVar16 = pbVar9;
      pbVar5 = pbVar9;
      if (pbVar11 != (byte *)0x0) {
        do {
          uVar6 = (int)pbVar16 + 1U & 0x800000ff;
          if ((int)uVar6 < 0) {
            uVar6 = (uVar6 - 1 | 0xffffff00) + 1;
          }
          pbVar16 = (byte *)(longlong)(int)uVar6;
          ans1 = local_138;
          bVar2 = ans1[(longlong)pbVar16];
          ans2 = (ulonglong)bVar2;
          uVar6 = (int)pbVar9 + (uint)bVar2 & 0x800000ff;
          if ((int)uVar6 < 0) {
            uVar6 = (uVar6 - 1 | 0xffffff00) + 1;
          }
          pbVar9 = (byte *)(ulonglong)uVar6;
          ans1[(longlong)pbVar16] = local_138[(int)uVar6];
          local_138[(int)uVar6] = bVar2;
          pbVar5[0x140005678] =
               local_138[(byte)(ans1[(longlong)pbVar16] + bVar2)] ^ pbVar5[0x140005038];
          pbVar5 = pbVar5 + 1;
        } while (pbVar5 < pbVar11);
      }
      inputFun("Flag: ASCIS{%s}\n",&DAT_140005678,ans1,ans2);
    }
    do {
      if (*ppvVar12 != (HANDLE)0x0) {
        CloseHandle(*ppvVar12);
      }
      ppvVar12 = ppvVar12 + 1;
      lVar18 = lVar18 + -1;
    } while (lVar18 != 0);
    CloseHandle(pvVar4);
  }
  FUN_140001690(local_38 ^ (ulonglong)auStackY504);
  return;
}
