import { useEffect, useState } from "react"
import axios from "axios"
import "./App.css"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"
const REGIONS = ["KE", "US", "GB", "NG", "IN", "CA", "AU"]

const URGENCY_COLORS = {
  "Post Now": "#ff0000",
  "Post Today": "#ff6600",
  "Post This Week": "#ffcc00",
  "Watch": "#666666"
}

const URGENCY_BG = {
  "Post Now": "#ff000015",
  "Post Today": "#ff660015",
  "Post This Week": "#ffcc0015",
  "Watch": "#66666615"
}

export default function App() {
  const [activeView, setActiveView] = useState("briefing")
  const [region, setRegion] = useState("KE")
  const [notified, setNotified] = useState(false)
  const [lastUpdated, setLastUpdated] = useState(null)

  const [briefing, setBriefing] = useState(null)
  const [briefingLoading, setBriefingLoading] = useState(false)

  const [opportunities, setOpportunities] = useState(null)
  const [oppsLoading, setOppsLoading] = useState(false)

  const [summary, setSummary] = useState("")
  const [summaryLoading, setSummaryLoading] = useState(false)

  const [googleTrends, setGoogleTrends] = useState([])
  const [news, setNews] = useState([])

  const [selectedVideo, setSelectedVideo] = useState(null)
  const [contentPackage, setContentPackage] = useState(null)
  const [productionGuide, setProductionGuide] = useState(null)
  const [contentLoading, setContentLoading] = useState(false)
  const [activeContentTab, setActiveContentTab] = useState("script")

  const fetchBriefing = async () => {
    setBriefingLoading(true)
    try {
      const res = await axios.get(`${API}/briefing`, { params: { region } })
      setBriefing(res.data)
    } catch (err) { console.error(err) }
    setBriefingLoading(false)
  }

  const fetchOpportunities = async () => {
    setOppsLoading(true)
    try {
      const res = await axios.get(`${API}/opportunities`, { params: { region } })
      setOpportunities(res.data)
      setLastUpdated(new Date().toLocaleTimeString())
    } catch (err) { console.error(err) }
    setOppsLoading(false)
  }

  const fetchSummary = async () => {
    setSummaryLoading(true)
    setSummary("")
    try {
      const res = await axios.get(`${API}/summary`, { params: { region } })
      setSummary(res.data.summary)
    } catch (err) { console.error(err) }
    setSummaryLoading(false)
  }

  const fetchGoogleAndNews = async () => {
    try {
      const [gRes, nRes] = await Promise.all([
        axios.get(`${API}/google-trends`, { params: { region } }),
        axios.get(`${API}/news`)
      ])
      setGoogleTrends(gRes.data.trends || [])
      setNews(nRes.data.articles || [])
    } catch (err) { console.error(err) }
  }

  const fetchContentPackage = async (video) => {
    setSelectedVideo(video)
    setContentPackage(null)
    setProductionGuide(null)
    setContentLoading(true)
    setActiveView("content")
    try {
      const res = await axios.get(`${API}/production-guide`, {
        params: { video_id: video.id, region }
      })
      setContentPackage(res.data.package)
      setProductionGuide(res.data.guide)
    } catch (err) { console.error(err) }
    setContentLoading(false)
  }

  const refreshAll = () => {
    fetchBriefing()
    fetchOpportunities()
    fetchSummary()
    fetchGoogleAndNews()
  }

  const sendNotification = async () => {
    try {
      await axios.get(`${API}/notify`, { params: { region } })
      setNotified(true)
      setTimeout(() => setNotified(false), 3000)
    } catch (err) { console.error(err) }
  }

  useEffect(() => { refreshAll() }, [region])

  return (
    <div className="app">
      <header>
        <div className="header-top">
          <h1>Trend Radar</h1>
          {lastUpdated && <span className="last-updated">Updated {lastUpdated}</span>}
        </div>
        <p>YouTube · Google · News · AI Powered</p>
        <div className="header-controls">
          <select value={region} onChange={e => setRegion(e.target.value)}>
            {REGIONS.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
          <button onClick={refreshAll}>Refresh</button>
          <button onClick={sendNotification} className="notify-btn">
            {notified ? "Sent!" : "Notify Me"}
          </button>
        </div>
      </header>

      <nav className="nav">
        {[
          { id: "briefing", label: "Morning Briefing" },
          { id: "opportunities", label: "Opportunities" },
          { id: "trends", label: "Trends" },
          { id: "content", label: "Content Studio" }
        ].map(v => (
          <button
            key={v.id}
            className={activeView === v.id ? "active" : ""}
            onClick={() => setActiveView(v.id)}
          >
            {v.label}
          </button>
        ))}
      </nav>

      <main>

        {activeView === "briefing" && (
          <div className="view">
            {briefingLoading ? (
              <div className="loading-box">
                <div className="pulse"></div>
                <p>Generating your morning briefing...</p>
              </div>
            ) : briefing ? (
              <div className="briefing">
                <div className="briefing-greeting">
                  <h2>{briefing.greeting}</h2>
                </div>

                {briefing.super_trend && (
                  <div className="super-trend">
                    <span className="super-label">Super Trend</span>
                    <p>{briefing.super_trend}</p>
                  </div>
                )}

                <h3 className="section-label">Top 3 Opportunities Today</h3>
                <div className="top3-grid">
                  {briefing.top_3 && briefing.top_3.map((item, i) => (
                    <div key={i} className="top3-card" style={{ borderColor: URGENCY_COLORS[item.urgency] }}>
                      <div className="top3-rank" style={{ background: URGENCY_COLORS[item.urgency] }}>
                        #{item.rank}
                      </div>
                      <h4>{item.topic}</h4>
                      <p>{item.why}</p>
                      <div className="top3-footer">
                        <span className="urgency-tag" style={{
                          color: URGENCY_COLORS[item.urgency],
                          background: URGENCY_BG[item.urgency]
                        }}>
                          {item.urgency}
                        </span>
                        <span className="predicted">{item.predicted_views}</span>
                      </div>
                    </div>
                  ))}
                </div>

                {briefing.avoid_today && (
                  <div className="avoid-box">
                    <span className="avoid-label">Avoid Today</span>
                    <p>{briefing.avoid_today}</p>
                  </div>
                )}

                <div className="motivation-box">
                  <p>{briefing.motivation}</p>
                </div>
              </div>
            ) : (
              <p className="empty">Click refresh to generate your morning briefing</p>
            )}
          </div>
        )}

        {activeView === "opportunities" && (
          <div className="view">
            <div className="summary-box">
              <div className="summary-header">
                <h3>AI Summary</h3>
                <button onClick={fetchSummary} className="small-btn">Regenerate</button>
              </div>
              {summaryLoading ? (
                <div className="summary-loading">
                  <div className="pulse"></div>
                  <p>Analyzing trends...</p>
                </div>
              ) : (
                <p>{summary || "Click refresh to generate summary"}</p>
              )}
            </div>

            {oppsLoading ? (
              <div className="loading-box">
                <div className="pulse"></div>
                <p>Scoring opportunities...</p>
              </div>
            ) : (
              <div className="opp-board">
                {["post_now", "post_today", "post_week", "watch"].map(bucket => {
                  const items = opportunities ? opportunities[bucket] : []
                  const labels = {
                    post_now: "Post Now",
                    post_today: "Post Today",
                    post_week: "Post This Week",
                    watch: "Watch"
                  }
                  const label = labels[bucket]
                  return (
                    <div key={bucket} className="opp-column">
                      <div className="opp-column-header" style={{ borderColor: URGENCY_COLORS[label] }}>
                        <span style={{ color: URGENCY_COLORS[label] }}>{label}</span>
                        <span className="opp-count">{items ? items.length : 0}</span>
                      </div>
                      {items && items.map((opp, i) => (
                        <div
                          key={i}
                          className="opp-card"
                          style={{ borderLeft: `3px solid ${URGENCY_COLORS[label]}` }}
                          onClick={() => fetchContentPackage(opp)}
                        >
                          <img src={opp.thumbnail} alt={opp.title} className="opp-thumb" />
                          <div className="opp-info">
                            <p className="opp-title">{opp.title}</p>
                            <p className="opp-channel">{opp.channel}</p>
                            <div className="opp-stats">
                              <span>Score: {opp.opportunity_score}/100</span>
                              <span>{Number(opp.views).toLocaleString()} views</span>
                            </div>
                            {opp.reasons && opp.reasons[0] && (
                              <p className="opp-reason">{opp.reasons[0]}</p>
                            )}
                          </div>
                          <div className="opp-action">Tap for content</div>
                        </div>
                      ))}
                      {(!items || items.length === 0) && (
                        <p className="empty-col">No items</p>
                      )}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )}

        {activeView === "trends" && (
          <div className="view">
            <div className="trends-grid">
              <div className="trends-section">
                <h3 className="section-label">Google Trends</h3>
                <div className="list">
                  {googleTrends.length === 0 ? (
                    <p className="empty">No Google Trends available</p>
                  ) : googleTrends.map((term, i) => (
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
                  ))}
                </div>
              </div>

              <div className="trends-section">
                <h3 className="section-label">Top News</h3>
                <div className="list">
                  {news.length === 0 ? (
                    <p className="empty">No news available</p>
                  ) : news.map((article, i) => (
                    <a
                      key={i}
                      href={article.url}
                      target="_blank"
                      rel="noreferrer"
                      className="list-item"
                    >
                      <span className="news-source">{article.source}</span>
                      <span className="post-title">{article.title}</span>
                      <span className="arrow">→</span>
                    </a>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeView === "content" && (
          <div className="view">
            {!selectedVideo ? (
              <div className="empty-content">
                <p>Tap any opportunity card to generate a full content package</p>
                <button onClick={() => setActiveView("opportunities")} className="go-btn">
                  View Opportunities
                </button>
              </div>
            ) : contentLoading ? (
              <div className="loading-box">
                <div className="pulse"></div>
                <p>Generating your full content package...</p>
                <p className="loading-sub">Script, hooks, production guide and more</p>
              </div>
            ) : contentPackage ? (
              <div className="content-studio">
                <div className="content-header">
                  <img src={selectedVideo.thumbnail} alt={selectedVideo.title} className="content-thumb" />
                  <div className="content-video-info">
                    <h2>{selectedVideo.title}</h2>
                    <p>{selectedVideo.channel}</p>
                    <div className="content-meta">
                      <span className="urgency-tag" style={{
                        color: URGENCY_COLORS[selectedVideo.urgency],
                        background: URGENCY_BG[selectedVideo.urgency]
                      }}>
                        {selectedVideo.urgency}
                      </span>
                      <span>Score: {selectedVideo.opportunity_score}/100</span>
                      <span>{contentPackage.difficulty} difficulty</span>
                      <span>Expires: {contentPackage.expiry}</span>
                    </div>
                  </div>
                </div>

                <div className="content-tabs">
                  {["script", "titles", "production", "insights"].map(tab => (
                    <button
                      key={tab}
                      className={activeContentTab === tab ? "active" : ""}
                      onClick={() => setActiveContentTab(tab)}
                    >
                      {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                  ))}
                </div>

                {activeContentTab === "script" && (
                  <div className="content-panel">
                    <div className="info-box">
                      <p>{contentPackage.trend_explanation}</p>
                    </div>
                    <div className="content-block">
                      <h4>Hook (First 2 Seconds)</h4>
                      <div className="hook-main">{contentPackage.hook}</div>
                      <h5>Alternative Hooks</h5>
                      {contentPackage.hook_alternatives && contentPackage.hook_alternatives.map((h, i) => (
                        <div key={i} className="hook-alt">{h}</div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Full Script</h4>
                      <div className="script-box">{contentPackage.script}</div>
                    </div>
                    <div className="content-block">
                      <h4>Pin This Comment</h4>
                      <div className="comment-box">{contentPackage.comment_prompt}</div>
                    </div>
                  </div>
                )}

                {activeContentTab === "titles" && (
                  <div className="content-panel">
                    <div className="content-block">
                      <h4>Title Options</h4>
                      {contentPackage.title_options && contentPackage.title_options.map((t, i) => (
                        <div key={i} className="title-option">
                          <span className="title-rank">#{i + 1}</span>
                          <span>{t}</span>
                        </div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Hashtags</h4>
                      <div className="hashtags">
                        {contentPackage.hashtags && contentPackage.hashtags.map((h, i) => (
                          <span key={i} className="hashtag">#{h}</span>
                        ))}
                      </div>
                    </div>
                    <div className="content-block">
                      <h4>Thumbnail Concept</h4>
                      <div className="thumbnail-concept">{contentPackage.thumbnail_concept}</div>
                    </div>
                    <div className="content-block">
                      <h4>Best Time to Post</h4>
                      <div className="time-box">{contentPackage.best_time_to_post}</div>
                    </div>
                    <div className="content-block">
                      <h4>Predicted Views</h4>
                      <div className="views-box">{contentPackage.predicted_views}</div>
                    </div>
                  </div>
                )}

                {activeContentTab === "production" && productionGuide && (
                  <div className="content-panel">
                    <div className="prod-meta">
                      <div className="prod-meta-item">
                        <span className="prod-label">Time needed</span>
                        <span>{productionGuide.total_time_needed}</span>
                      </div>
                      <div className="prod-meta-item">
                        <span className="prod-label">Best app</span>
                        <span>{productionGuide.recommended_app}</span>
                      </div>
                      <div className="prod-meta-item">
                        <span className="prod-label">Sound</span>
                        <span>{productionGuide.recommended_sound}</span>
                      </div>
                      <div className="prod-meta-item">
                        <span className="prod-label">Export</span>
                        <span>{productionGuide.export_settings}</span>
                      </div>
                    </div>
                    <div className="content-block">
                      <h4>Filming Steps</h4>
                      {productionGuide.filming_steps && productionGuide.filming_steps.map((step, i) => (
                        <div key={i} className="step-item">
                          <div className="step-num">{step.step}</div>
                          <div className="step-content">
                            <p className="step-action">{step.action}</p>
                            <p className="step-tip">Tip: {step.tip}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Editing Steps</h4>
                      {productionGuide.editing_steps && productionGuide.editing_steps.map((step, i) => (
                        <div key={i} className="step-item">
                          <div className="step-num">{step.step}</div>
                          <div className="step-content">
                            <p className="step-action">{step.action}</p>
                            <p className="step-tip">Tip: {step.tip}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Upload Checklist</h4>
                      {productionGuide.upload_checklist && productionGuide.upload_checklist.map((item, i) => (
                        <div key={i} className="checklist-item">
                          <span className="check">checkmark</span>
                          <span>{item}</span>
                        </div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Common Mistakes to Avoid</h4>
                      {productionGuide.common_mistakes && productionGuide.common_mistakes.map((item, i) => (
                        <div key={i} className="mistake-item">
                          <span className="x-mark">x</span>
                          <span>{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeContentTab === "insights" && (
                  <div className="content-panel">
                    <div className="insights-grid">
                      <div className="insight-card">
                        <h5>Sentiment</h5>
                        <p>{contentPackage.sentiment}</p>
                      </div>
                      <div className="insight-card">
                        <h5>Trend Origin</h5>
                        <p>{contentPackage.trend_origin}</p>
                      </div>
                      <div className="insight-card">
                        <h5>Difficulty</h5>
                        <p>{contentPackage.difficulty}</p>
                      </div>
                      <div className="insight-card">
                        <h5>Evergreen Score</h5>
                        <p>{contentPackage.evergreen_score}/10</p>
                      </div>
                    </div>
                    <div className="content-block">
                      <h4>Series Potential</h4>
                      <p>{contentPackage.series_potential}</p>
                    </div>
                    <div className="content-block">
                      <h4>Unique Angles Nobody Is Covering</h4>
                      {contentPackage.similar_angles && contentPackage.similar_angles.map((angle, i) => (
                        <div key={i} className="angle-item">
                          <span className="angle-num">#{i + 1}</span>
                          <span>{angle}</span>
                        </div>
                      ))}
                    </div>
                    {contentPackage.controversy_warning && (
                      <div className="warning-box">
                        <h5>Controversy Warning</h5>
                        <p>{contentPackage.controversy_warning}</p>
                      </div>
                    )}
                    <div className="content-block">
                      <h4>Caption Style</h4>
                      <p>{contentPackage.caption_style}</p>
                    </div>
                  </div>
                )}
              </div>
            ) : null}
          </div>
        )}

      </main>
    </div>
  )
}