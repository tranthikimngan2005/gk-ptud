import sqlite3
conn = sqlite3.connect('gallery.db')
c = conn.cursor()
c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', '123')")
imgs = [('Corgi 1', 'uploads/pic1.jpg'), ('Corgi 2', 'uploads/pic2.jpg'), 
        ('Corgi 3', 'uploads/pic3.jpg'), ('Corgi 4', 'uploads/pic4.jpg')]
for t, u in imgs:
    c.execute("INSERT INTO photos (title, image_url, user_id) VALUES (?, ?, 1)", (t, u))
conn.commit()
conn.close()
print("Đã nạp xong ảnh!")