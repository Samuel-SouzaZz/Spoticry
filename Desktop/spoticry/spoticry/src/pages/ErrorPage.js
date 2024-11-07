import React from 'react';

function ErrorPage({ message = "Ocorreu um erro!" }) {
  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Erro</h1>
      <p>{message}</p>
    </div>
  );
}

export default ErrorPage;
