import { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);

  const fetchData = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/live/0/");
      const json = await res.json();
      setData(json);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, []);

  if (!data) return <div className="loading">Loading match data...</div>;

  const win = data.win_probability || 0;
  const lose = data.lose_probability || 0;

  const winColor = win > 50 ? "green" : "red";
  const loseColor = lose > 50 ? "green" : "red";

  return (
    <div className="container">
      <h1>🏏 T20 Live Predictor</h1>

      <div className="match-info">
        <h2>{data.team1} vs {data.team2}</h2>
        <p><strong>Match State:</strong> {data.match_state}</p>
        <p><strong>Status:</strong> {data.status}</p>
        <p><strong>Score:</strong> {data.real_score}</p>
        {data.message && (
            <div style={{
              marginTop: "20px",
              padding: "10px",
              backgroundColor: "#334155",
              borderRadius: "8px"
            }}>
              {data.message}
            </div>
          )}

      </div>

      {data.win_probability && (
        <div className="probability-section">
          <h3>Win Probability</h3>

          <div className="team-prob">
            <span>{data.team2}</span>
            <div className="progress-bar">
              <div
                className="progress"
                style={{
                  width: `${win}%`,
                  backgroundColor: winColor
                }}
              >
                {win}%
              </div>
            </div>
          </div>

          <div className="team-prob">
            <span>{data.team1}</span>
            <div className="progress-bar">
              <div
                className="progress"
                style={{
                  width: `${lose}%`,
                  backgroundColor: loseColor
                }}
              >
                {lose}%
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
