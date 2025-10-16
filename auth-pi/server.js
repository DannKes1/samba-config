// server.js

// ex .env: SECRET_KEY=uma_chave_secreta_forte_aqui

require("dotenv").config();
const express = require("express");
const jwt = require("jsonwebtoken");
const bodyParser = require("body-parser");

const app = express();
const PORT = 3000;
const SECRET_KEY = process.env.SECRET_KEY;


app.use(bodyParser.json());


const refreshTokens = new Set();


const users = [
  { id: 1, username: "admin", password: "adminpass", role: "admin" },
  { id: 2, username: "user", password: "userpass", role: "usuario" },
  { id: 3, username: "mod", password: "modpass", role: "moderador" },
];

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});


app.post("/login", (req, res) => {
  const { username, password } = req.body;

  
  const user = users.find(
    (u) => u.username === username && u.password === password
  );
  if (!user) {
    return res.status(401).json({ error: "Credenciais inválidas" });
  }

 
  const accessToken = jwt.sign(
    { id: user.id, name: user.username, role: user.role },
    SECRET_KEY,
    { expiresIn: "15m" }
  );

  
  const refreshToken = jwt.sign({ id: user.id }, SECRET_KEY, {
    expiresIn: "7d",
  });

 
  refreshTokens.add(refreshToken);

  
  res.json({ accessToken, refreshToken });
});


app.post("/refresh", (req, res) => {
  const { refreshToken } = req.body;

  if (!refreshToken) {
    return res.status(401).json({ error: "Refresh Token requerido" });
  }


  if (!refreshTokens.has(refreshToken)) {
    return res.status(403).json({ error: "Refresh Token inválido" });
  }

  try {
    
    const decoded = jwt.verify(refreshToken, SECRET_KEY);

    
    const user = users.find((u) => u.id === decoded.id);
    if (!user) {
      return res.status(401).json({ error: "Usuário não encontrado" });
    }

    
    const newAccessToken = jwt.sign(
      { id: user.id, name: user.username, role: user.role },
      SECRET_KEY,
      { expiresIn: "15m" }
    );

   
    refreshTokens.delete(refreshToken);
    const newRefreshToken = jwt.sign({ id: user.id }, SECRET_KEY, {
      expiresIn: "7d",
    });
    refreshTokens.add(newRefreshToken);

    
    res.json({ accessToken: newAccessToken, refreshToken: newRefreshToken });
  } catch (err) {
    return res
      .status(403)
      .json({ error: "Refresh Token expirado ou inválido" });
  }
});


const authenticateToken = (req, res, next) => {
  const authHeader = req.headers["authorization"];
  const token = authHeader && authHeader.split(" ")[1]; // Bearer <token>

  if (!token) {
    return res.status(401).json({ error: "Token requerido" });
  }

  try {
    const decoded = jwt.verify(token, SECRET_KEY);
    req.user = decoded; 
    next();
  } catch (err) {
    return res.status(403).json({ error: "Token inválido ou expirado" });
  }
};

app.get("/usuarios", authenticateToken, (req, res) => {
  if (req.user.role !== "admin") {
    return res.status(403).json({ error: "Acesso negado" });
  }

  res.json({
    usuarios: users.map((u) => ({
      id: u.id,
      username: u.username,
      role: u.role,
    })),
  });
});


app.post("/dados", authenticateToken, (req, res) => {

  let message = "Dados salvos com sucesso";
  if (req.user.role === "moderador") {
    message += " (modo moderador)";
  }
  res.json({ message, user: req.user });
});


app.post("/logout", (req, res) => {
  const { refreshToken } = req.body;

  if (refreshTokens.has(refreshToken)) {
    refreshTokens.delete(refreshToken);
    return res.json({ message: "Sessão revogada com sucesso" });
  } else {
    return res.status(400).json({ error: "Refresh Token inválido" });
  }
});

