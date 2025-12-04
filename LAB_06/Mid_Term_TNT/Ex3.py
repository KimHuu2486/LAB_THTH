def brute_force_bai3():
    R = C = 5

    # Đánh số ô từ 0..24 theo hàng
    def id_of(r, c):
        return r * C + c

    # Tạo mask cho 9 hình 3x3
    sub_masks = []
    for r in range(R - 3 + 1):       # 0,1,2
        for c in range(C - 3 + 1):   # 0,1,2
            m = 0
            for i in range(3):
                for j in range(3):
                    bit = id_of(r + i, c + j)
                    m |= (1 << bit)
            sub_masks.append(m)

    ans = 0
    TOTAL = 1 << (R * C)   # 2^25

    for mask in range(TOTAL):
        ok = True
        for sm in sub_masks:
            # nếu sm nằm trọn trong mask → hình vuông 3x3 này toàn đỏ
            if (mask & sm) == sm:
                ok = False
                break
        if ok:
            ans += 1

    print("So cach to hop le (brute force):", ans)

brute_force_bai3()
