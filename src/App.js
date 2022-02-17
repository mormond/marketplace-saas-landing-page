import React, { useState, useEffect } from 'react';
import { useSearchParams } from "react-router-dom";

function AuthButton() {
  const authorise = () => {
    // Call the authorise API
    console.log("Hello");
  }
  return <button onClick={authorise}>Authorise</button>;
}

function App() {
  const [data, setData] = useState('');

  const [searchParams] = useSearchParams();
  const queryToken = searchParams.get('token');

  const Log = ({ value, replacer = null, space = 2 }) => (
    <pre>
      <code>{JSON.stringify(value, replacer, space)}</code>
    </pre>
  )
  
  useEffect(() => {
    (async function () {
      const { text } = await (await fetch(`/api/resolve_token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ marketplace_token: queryToken })
      })).json();
      setData(text);

    })();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return <div><div><Log value={data}></Log></div><div><AuthButton /></div></div>;
}

export default App;

