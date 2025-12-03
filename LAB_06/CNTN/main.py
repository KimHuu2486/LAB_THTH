from Graph import Graph

if __name__ == "__main__":
    
    # 1. KHỞI TẠO VÀ LOAD DỮ LIỆU
    print("--- 1. LOAD GRAPH ---")
    g = Graph.load_graph_from_jl("g1.v2.jl", directed=False)
    print(f"Load thành công. Tổng số đỉnh: {g.countVertices()}")
    print(f"Tổng số cạnh: {g.countEdges()}")
        
    # 2. HIỂN THỊ CẤU TRÚC
    print("\n--- 2. HIỂN THỊ ---")
    g.print_adj_list()
    #g.print_adj_matrix()
    
    if len(g.vertices) > 0:
        sample_node = g.vertices[0]
        
        # 3. KIỂM TRA BẬC VÀ ĐỈNH ĐẶC BIỆT
        print("\n--- 3. THÔNG TIN ĐỈNH ---")
        print(f"Bậc của đỉnh '{sample_node}': {g.Degree(sample_node)}")
        print(f"Danh sách đỉnh cô lập (Isolated): {g.isolated_vertices()}")
        print(f"Danh sách đỉnh lá (Leaf): {g.leaf_vertices()}")

        # 4. DUYỆT ĐỒ THỊ
        print("\n--- 4. DUYỆT ĐỒ THỊ (TRAVERSAL) ---")
        print(f"DFS bắt đầu từ '{sample_node}': {g.DFS(sample_node)}")
        print(f"BFS bắt đầu từ '{sample_node}': {g.BFS(sample_node)}")

        # 5. TÍNH CHẤT ĐỒ THỊ
        print("\n--- 5. TÍNH CHẤT ---")
        print(f"Có phải đồ thị đầy đủ (Complete)? {g.is_complete()}")
        print(f"Có phải đồ thị vòng (Cycle)? {g.is_cycle()}")
        print(f"Có phải đồ thị hai phía (Bipartite)? {g.is_bipartite()}")
        
        # 6. TÍNH LIÊN THÔNG MẠNH/YẾU, KHỚP VÀ CẦU
        print("\n--- 6. LIÊN THÔNG & CẤU TRÚC ---")
        comps = g.count_connect_components()
        print(f"Số thành phần liên thông: {comps}")
        
        if not g.directed:
            print(f"Các đỉnh khớp (Articulation Points): {g.articulation_points()}")
            print(f"Các cạnh cầu (Bridges): {g.bridges()}")

        # 7. EULER (Hierholzer & Fleury)
        print("\n--- 7. EULER ---")
        euler_path = g.euler_hierholzer()
        if euler_path:
            print(f"Đường đi/Chu trình Euler (Hierholzer): {euler_path}")
        else:
            print("Đồ thị không có đường đi Euler (Hierholzer).")
            
    # 8. CÁC PHÉP BIẾN ĐỔI ĐỒ THỊ (Tạo bản sao để không ảnh hưởng đồ thị gốc)
    print("\n--- 8. BIẾN ĐỔI ---")
    if g.directed:
        conv = g.converse_graph()
        print("Đã tạo đồ thị đảo (Converse).")
    else:
        comp = g.complement_graph()
        print(f"Đã tạo đồ thị bù (Complement). Số cạnh đồ thị bù: {comp.countEdges()}")