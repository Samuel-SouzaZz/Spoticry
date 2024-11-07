import React, { createContext, useContext, useState } from 'react';

const MusicContext = createContext();

export const MusicProvider = ({ children }) => {
  const [musics, setMusics] = useState([]);  // Estado para armazenar músicas

  // Adiciona uma nova música ao estado
  const addMusic = music => {
    setMusics([...musics, music]);
  };

  // Remove uma música do estado
  const removeMusic = musicId => {
    setMusics(musics.filter(music => music.id !== musicId));
  };

  // Atualiza uma música no estado
  const updateMusic = updatedMusic => {
    const updatedMusics = musics.map(music =>
      music.id === updatedMusic.id ? updatedMusic : music
    );
    setMusics(updatedMusics);
  };

  return (
    <MusicContext.Provider value={{ musics, addMusic, removeMusic, updateMusic }}>
      {children}
    </MusicContext.Provider>
  );
};

export const useMusic = () => useContext(MusicContext);
