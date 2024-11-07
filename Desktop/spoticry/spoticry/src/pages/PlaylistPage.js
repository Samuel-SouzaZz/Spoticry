import React from 'react';
import PlaylistList from '../components/Playlists/PlaylistList';
import PlaylistDetails from '../components/Playlists/PlaylistDetails';

function PlaylistPage() {
  return (
    <div>
      <PlaylistList />
      <PlaylistDetails />
    </div>
  );
}

export default PlaylistPage;
