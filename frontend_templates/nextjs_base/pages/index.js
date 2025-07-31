export default function Home() {
  return (
    <div style={{ textAlign: 'center', marginTop: 40 }}>
      <h1>Benvenuto nella dashboard GDPR!666</h1>
      <a
        href="/dashboard"
        style={{
          display: 'inline-block',
          marginTop: 24,
          fontSize: 20,
          color: '#0070f3',
          textDecoration: 'underline',
        }}
      >
        Vai alla dashboard con metriche
      </a>
    </div>
  );
}
