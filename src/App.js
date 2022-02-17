import React, { useState, useEffect } from 'react';
import { useSearchParams } from "react-router-dom";

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
      const { text } = await (await fetch(`/api/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ marketplace_token: queryToken })
      })).json();
      setData(text);

    })();
  }, []);

  return <div><Log value={data}></Log></div>;
}

export default App;

