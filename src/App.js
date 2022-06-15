import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import './index.css';

function App() {
  const [decodedToken, setDecodedToken] = useState({});
  const [response, setResponse] = useState('');
  const [searchParams] = useSearchParams();
  const queryToken = searchParams.get('token');

  const Log = ({ isJson=false, value, replacer = null, space = 2 }) => (
    <pre>
      {isJson === true ? <code>{JSON.stringify(value, replacer, space)}</code> : <code>{value}</code>}
    </pre>
  )

  useEffect(() => {
    if (response) {
      console.log(response);
      const tokenObject = JSON.parse(response);
      setDecodedToken(tokenObject);
    }
  }, [response]);

  async function decodeToken() {
    try {
      const token = await (await fetch(`/api/resolve_token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ marketplace_token: queryToken })
      })).json();

      setResponse(JSON.stringify(token.text, null, 2));
      setDecodedToken(JSON.parse(response));

    } catch (error) {
      return;
    }
  }

  return <div className='maincontainer'>
    <header>
      <h1>Azure Marketplace</h1>
      <h2>SaaS Offer Landing Page Sample</h2>
    </header>

    <div>
      <h3>Raw Token</h3>
      <Log value={queryToken ? queryToken : 'No token found to decode. Is the token parameter present in the query string?'} />
    </div>

    <div>
      <h3>Decoded Token</h3>
      <Log isJson={true} value={decodedToken} />
    </div>

    <button onClick={() => decodeToken()}
      className="button">
      Decode Token
    </button>

    <footer style={{ marginTop: 10 + '%' }}>For more information see <a href='https://github.com/mormond/marketplace-saas-landing-page'>https://github.com/mormond/marketplace-saas-landing-page</a></footer>
  </div>
}

export default App;

