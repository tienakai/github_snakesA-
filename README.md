# ***Snake Game*** 

## **Introduction** 

+ Họ và tên: <br>
  Nguyễn Ngọc Tiến <br>
  Phạm Như Mạnh <br>
  Trần Thị Khánh Linh
+ Bài tập lớn: Snake Game (Bài tập cuối kỳ)
## **Description** 

### *Game description and instruction* 
- Đây là trò chơi rắn săn mồi hoàn toàn mới với rất nhiều tính năng hay, vượt trội. Game có 2 chế độ chơi cho người chơi thoả sức lựa chọn: 

    + Game mode 1 - 1 Player: Giống với rắn săn mồi truyền thống người chơi sử dụng các phím mũi tên trên bàn phím để di chuyển rắn đến quả táo. 

    + Game mode 2 - bot player: Người chơi sẽ có cơ hội thử sức với 1 con rắn thông minh có khả năng tránh né border và tìm táo rất nhanh với thuật toán A* và BFS

- Game có đầy đủ các chức năng hỗ trợ người chơi trong việc điều chỉnh dễ dàng giữa các chế độ, thoát game, ... 

- Có âm thanh êm dịu thoải mái khi chơi

- Snake Game(new edition) chắc chắn sẽ không khiến cho người chơi phải thất vọng với những tính năng, đồ hoạ cực kì độc đáo, mới lạ.
### *Control* 
| Control | Player 1 |
|---------|----------|
| UP      |     ↑    |     
| DOWN    |     ↓    |     
| LEFT    |     ←    |      
| RIGHT   |     →    |     

### **Setup**
- Yêu cầu: Có Python compiler và tải visual studio code
1. Dùng terminal hoặc git bash tải source code về máy: git clone https://github.com/tienakai/github_snakesA-
2.  Vào thư mục vừa tải về
3.  Trên thanh công cụ vào Tools → Build System và ấn tick vào Build Debug
4.  Ấn phím F5 hoặc tổ hợp phím Ctrl + F5 để chạy chương trình
### *Các kỹ thuật sử dụng*  
- Thư viện Pygame

- Sử dụng nhiều class, vector, tách file, nạp chồng toán tử, ...

- Có thể lưu lại điểm sau mỗi lần chơi 

- Tạo các đối tượng: rắn, táo, đuôi, ... 

- Dùng các kiến thức toán học để tính toán được góc cua của rắn để chèn ảnh thân và đuôi lúc cong 

- Xử lý thời gian, thao tác chuột và bàn phím, âm thanh, hình ảnh, chữ. 

- Tạo menu và các nút ấn di chuyển giữa các menu 

- Sử dụng các kiến thức Đại số, Toán rời rạc: cụ thể là sử dụng toạ độ, thuật toán tìm kiếm A* (A* search algorithm) để tạo nên AI Snake vượt trội, 1 trong những phương thức tối ưu nhất để giúp cho rắn có thể tìm đồ ăn nhanh và né được chướng ngại vật và đuôi rắn. Ngoài ra: còn có thuật toán  BFS(Breadth-First Search)
- ### *Nguồn tham khảo* 
- Cách sử dụng, cài đặt visual studio code : https://code.visualstudio.com/

- Cách sử dụng thư viện Pygame, quản lý chương trình: https://www.pygame.org/news. [Accessed: Jun. 15, 2025].

- Hình ảnh: tìm kiếm trên google và flaticon 

- Âm thanh: Tự tra trên google 

- Thuật toán: https://ant.ncc.asia/thuat-toan-a-tim-duong-ngan-nhat-trong-do-thi/. ; https://wiki.vnoi.info/algo/graph-theory/breadth-first-search.md
- ### ***Điểm hạn chế*** 
- Rắn trong chương trình vẫn đang được quản lý theo vector chứ chưa phải danh sách liên kết đơn.
- ### ***Hướng phát triển*** 
- Cập nhật tính năng bảng xếp hạng, sau mỗi lần chơi người chơi sẽ được nhập tên để lưu lại kết quả chơi của mình.

- Thêm nhiều loại đồ ăn có tính năng khác nhau. 

- Thêm chế độ điều chỉnh tốc độ để người chơi có thể chọn tốc độ tuỳ thích, phù hợp với khả năng chơi của mình.

- Dựa vào thuật toán tìm kiếm A*, em nghĩ mình sẽ có thể mở rộng phạm vi duyệt của đầu rắn kết hợp với thuật toán tìm đường đi Halmiton để tạo ra 1 con AI Snake bất tử mà vẫn có khả năng tìm đồ ăn cực nhanh. 

  ### ***Nhiệm vụ của mỗi người trong nhóm***
  Nguyễn Ngọc Tiến: Leader, code chính
  Phạm Như Mạnh: Tìm hiểu và code thuật toán A* và BFS, viết báo cáo
  Trần Thị Khánh Linh: Thiết kế giao diện, làm slide
     
