import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);  // Estado para armazenar o usuário logado

  // Função para simular o login
  const login = async (username, password) => {
    setUser({ username, token: 'fake-jwt-token' });
  };
  // Função para deslogar o usuário
  const logout = () => {
    setUser(null);  // Limpa o usuário do estado
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
