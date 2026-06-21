import { useEffect, useState } from "react"
import axios from "axios"
import "./App.css"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"
const REGIONS = ["US", "KE", "GB", "NG", "IN", "CA", "AU"]

export default function App() {
  const [videos, setVideos] = useState([])
  const [categories, setCategories] = useState({})
  const [category, setCategory] = useState("0")
  const [region, setRegion] = useState("KE")
  const [loading, setLoading] = useState(false)
  const [summary, setSummary] = useState("")
  const [summaryLoading, setSummaryLoading] = useState(false)
  const [googleTrends, setGoogleTrends] = useState([])
  const [notified, setNotified] = useState(false)
  const [activeTab, setActiveTab] = useState("youtube")
  const [lastUpdated, setLastUpdated] = useState(null)

  const fetchTrending = async () => {
    setLoading(true)
    try {
      const res = await axios.get(`${API}/trending`, {
        params: { category, region }
      })
      setVideos(res.data.videos)
      setLastUpdated(new Date().toLocaleTimeString())
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const fetchSummary = async () => {
    setSummaryLoading(true)
    setSummary("")
    try {
      const res = await axios.get(`${API}/summary`, {
        params: { category, region }
      })
      setSummary(res.data.summary)
    } catch (err) {
      console.error(err)
    }
    setSummaryLoading(false)
  }

  const fetchGoogleTrends = async () => {
    try {
      const res = await axios.get(`${API}/google-trends`, {
        params: { region }
      })
      setGoogleTrends(res.data.trends)
    } catch (err) {
      console.error(err)
    }
  }

  const refreshAll = () => {
    fetchTrending()
    fetchGoogleTrends()
    fetchSummary()
  }

  const sendNotification = async () => {
    try {
      await axios.get(`${API}/notify`, {
        params: { category, region }
      })
      setNotified(true)
      setTimeout(() => setNotified(false), 3000)
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    axios.get(`${API}/categories`).then(res => {
      setCategories(res.data)
    })
  }, [])

  useEffect(() => {
    refreshAll()
  }, [category, region])

  return (
    <div className="app">
      <header>
        <div className="header-top">
          <h1>🔥 Trend Radar</h1>
          {lastUpdated && <span className="last-updated">Updated {lastUpdated}</span>}
        </div>
        <p>YouTube · Google · AI Summary</p>
      </header>

      <div className="controls">
        <select value={category} onChange={e => setCategory(e.target.value)}>
          {Object.entries(categories).map(([id, name]) => (
            <option key={id} value={id}>{name}</option>
          ))}
        </select>

        <select value={region} onChange={e => setRegion(e.target.value)}>
          {REGIONS.map(r => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>

        <button onClick={refreshAll}>🔄 Refresh</button>
        <button onClick={sendNotification} className="notify-btn">
          {notified ? "✅ Sent!" : "🔔 Notify Me"}
        </button>
      </div>

      <div className="summary-box">
        <div className="summary-header">
          <h2>🤖 AI Summary</h2>
          <button onClick={fetchSummary} className="regen-btn">Regenerate</button>
        </div>
        {summaryLoading ? (
          <div className="summary-loading">
            <div className="pulse"></div>
            <p>Analyzing trends across all sources...</p>
          </div>
        ) : (
          <p>{summary || "Click refresh to generate summary"}</p>
        )}
      </div>

      <div className="tabs">
        <button
          className={activeTab === "youtube" ? "active" : ""}
          onClick={() => setActiveTab("youtube")}
        >
          📺 YouTube
        </button>
        <button
          className={activeTab === "google" ? "active" : ""}
          onClick={() => setActiveTab("google")}
        >
          🔍 Google
        </button>
      </div>

      {loading ? (
        <p className="loading">Loading trends...</p>
      ) : (
        <>
          {activeTab === "youtube" && (
            <div className="grid">
              {videos.map((v, i) => (
                <a
                  key={v.id}
                  href={"https://youtube.com/watch?v=" + v.id}
                  target="_blank"
                  rel="noreferrer"
                  className="card"
                >
                  <span className="rank">#{i + 1}</span>
                  <img src={v.thumbnail} alt={v.title} />
                  <div className="info">
                    <h3>{v.title}</h3>
                    <p className="channel">{v.channel}</p>
                    <div className="stats">
                      <span>👁 {Number(v.views).toLocaleString()}</span>
                      <span>👍 {Number(v.likes).toLocaleString()}</span>
                    </div>
                  </div>
                </a>
              ))}
            </div>
          )}

          {activeTab === "google" && (
            <div className="list">
              {googleTrends.length === 0 ? (
                <p className="empty">No Google Trends available for this region yet</p>
              ) : (
                googleTrends.map((term, i) => (
                  <a
                    key={i}
                    href={"https://www.google.com/search?q=" + encodeURIComponent(term)}
                    target="_blank"
                    rel="noreferrer"
                    className="list-item"
                  >
                    <span className="rank-small">#{i + 1}</span>
                    <span className="trend-term">{term}</span>
                    <span className="arrow">→</span>
                  </a>
                ))
              )}
            </div>
          )}
        </>
      )}
    </div>
  )
}