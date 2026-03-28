import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = "http://127.0.0.1:8000";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [photos, setPhotos] = useState([]);
  const [search, setSearch] = useState("");
  const [editing, setEditing] = useState(null); // Để sửa ảnh

  const api = axios.create({ headers: { Authorization: `Bearer ${token}` } });

  useEffect(() => { if (token) load(); }, [token, search]);

  const load = async () => {
    const res = await api.get(`${API}/photos?q=${search}`);
    setPhotos(res.data);
  };

  const handleAction = async (e, path, method = 'post') => {
    e.preventDefault();
    const fd = new FormData(e.target);
    try {
      const requiresAuth = !path.includes('/login') && !path.includes('/register');
      const client = requiresAuth ? api : axios;
      const res = await client[method](path, fd);
      if (path.includes('login')) {
        localStorage.setItem("token", res.data.token);
        setToken(res.data.token);
      }
      alert("Thành công!");
      if (!path.includes('login')) load();
      e.target.reset();
      setEditing(null);
    } catch (err) { alert("Lỗi rồi Ngân ơi!"); }
  };

  if (!token) return (
    <div className="auth-box">
      <h2>Gallery Login</h2>
      <form onSubmit={(e) => handleAction(e, `${API}/login`)}>
        <input name="username" placeholder="Username" required />
        <input name="password" type="password" placeholder="Password" required />
        <button type="submit">Đăng nhập</button>
      </form>
    </div>
  );

  return (
    <div className="main-container">
      <header>
        <h1>My Personal Library</h1>
        <button onClick={() => {localStorage.clear(); setToken(null);}}>Thoát</button>
      </header>

      {/* Tìm kiếm & Upload */}
      <div className="controls">
        <input placeholder="🔍 Tìm kiếm ảnh theo tên..." onChange={e => setSearch(e.target.value)} />
        <form onSubmit={(e) => handleAction(e, `${API}/photos`)}>
          <input name="title" placeholder="Tên ảnh" required />
          <input type="file" name="file" required />
          <button type="submit">Tải lên</button>
        </form>
      </div>

      {/* Danh sách ảnh Masonry */}
      <div className="masonry-grid">
        {photos.map(p => (
          <div key={p.id} className="masonry-item">
            <img src={`${API}/${p.image_url}`} alt="" />
            <div className="info">
              <h4>{p.title}</h4>
              <button onClick={() => setEditing(p)}>Sửa</button>
              <button onClick={async () => {await api.delete(`${API}/photos/${p.id}`); load();}}>Xóa</button>
            </div>
          </div>
        ))}
      </div>

      {/* Form Sửa (Modal) */}
      {editing && (
        <div className="modal">
          <form onSubmit={(e) => handleAction(e, `${API}/photos/${editing.id}`, 'put')}>
            <h3>Chỉnh sửa ảnh</h3>
            <input name="title" defaultValue={editing.title} />
            <textarea name="desc" defaultValue={editing.description}></textarea>
            <button type="submit">Lưu</button>
            <button type="button" onClick={() => setEditing(null)}>Hủy</button>
          </form>
        </div>
      )}
    </div>
  );
}