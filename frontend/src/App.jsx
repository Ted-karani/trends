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
  const [viralAlerts, setViralAlerts] = useState([])
  const [predictions, setPredictions] = useState([])
  const [crossLanguage, setCrossLanguage] = useState(null)
  const [timeMachine, setTimeMachine] = useState(null)
  const [niches, setNiches] = useState([])
  const [monetization, setMonetization] = useState(null)
  const [health, setHealth] = useState(null)
  const [hooks, setHooks] = useState([])

  const [competitors, setCompetitors] = useState([])
  const [competitorSearch, setCompetitorSearch] = useState("")
  const [competitorResults, setCompetitorResults] = useState([])
  const [competitorData, setCompetitorData] = useState([])

  const [selectedVideo, setSelectedVideo] = useState(null)
  const [contentPackage, setContentPackage] = useState(null)
  const [productionGuide, setProductionGuide] = useState(null)
  const [blueprint, setBlueprint] = useState(null)
  const [contentLoading, setContentLoading] = useState(false)
  const [activeContentTab, setActiveContentTab] = useState("script")

  const [scriptInput, setScriptInput] = useState("")
  const [improvedScript, setImprovedScript] = useState(null)
  const [scriptLoading, setScriptLoading] = useState(false)

  const [repurposeInput, setRepurposeInput] = useState("")
  const [repurposed, setRepurposed] = useState(null)
  const [repurposeLoading, setRepurposeLoading] = useState(false)

  const [growthForm, setGrowthForm] = useState({ subscribers: 0, avg_views: 0, posts_per_week: 1, niche: "general" })
  const [growthResult, setGrowthResult] = useState(null)
  const [growthLoading, setGrowthLoading] = useState(false)

  const [collabForm, setCollabForm] = useState({ niche: "general", subscribers: 0 })
  const [collabResult, setCollabResult] = useState(null)
  const [collabLoading, setCollabLoading] = useState(false)

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

  const fetchExtras = async () => {
    try {
      const [gRes, nRes, vRes, pRes] = await Promise.all([
        axios.get(`${API}/google-trends`, { params: { region } }),
        axios.get(`${API}/news`),
        axios.get(`${API}/viral-alerts`, { params: { region } }),
        axios.get(`${API}/predict`, { params: { region } })
      ])
      setGoogleTrends(gRes.data.trends || [])
      setNews(nRes.data.articles || [])
      setViralAlerts(vRes.data.recent || [])
      setPredictions(pRes.data.predictions || [])
    } catch (err) { console.error(err) }
  }

  const fetchIntelligence = async () => {
    try {
      const [clRes, tmRes, nRes, mRes] = await Promise.all([
        axios.get(`${API}/cross-language`),
        axios.get(`${API}/time-machine`, { params: { region } }),
        axios.get(`${API}/niches`, { params: { region } }),
        axios.get(`${API}/monetization`, { params: { region } })
      ])
      setCrossLanguage(clRes.data)
      setTimeMachine(tmRes.data)
      setNiches(nRes.data.niches || [])
      setMonetization(mRes.data.insights)
    } catch (err) { console.error(err) }
  }

  const fetchHealth = async () => {
    try {
      const res = await axios.get(`${API}/health`)
      setHealth(res.data)
    } catch (err) { console.error(err) }
  }

  const fetchHooks = async () => {
    try {
      const res = await axios.get(`${API}/hooks`)
      setHooks(res.data.hooks || [])
    } catch (err) { console.error(err) }
  }

  const fetchCompetitors = async () => {
    try {
      const res = await axios.get(`${API}/competitors`)
      setCompetitors(res.data.channels || [])
      setCompetitorData(res.data.data || [])
    } catch (err) { console.error(err) }
  }

  const searchCompetitors = async () => {
    if (!competitorSearch.trim()) return
    try {
      const res = await axios.get(`${API}/competitors/search`, { params: { q: competitorSearch } })
      setCompetitorResults(res.data.results || [])
    } catch (err) { console.error(err) }
  }

  const addCompetitor = async (channel) => {
    try {
      await axios.post(`${API}/competitors/add`, channel)
      fetchCompetitors()
      setCompetitorResults([])
      setCompetitorSearch("")
    } catch (err) { console.error(err) }
  }

  const removeCompetitor = async (channelId) => {
    try {
      await axios.delete(`${API}/competitors/${channelId}`)
      fetchCompetitors()
    } catch (err) { console.error(err) }
  }

  const fetchContentPackage = async (video) => {
    setSelectedVideo(video)
    setContentPackage(null)
    setProductionGuide(null)
    setBlueprint(null)
    setContentLoading(true)
    setActiveView("content")
    try {
      const res = await axios.get(`${API}/production-guide`, {
        params: { video_id: video.id, region }
      })
      setContentPackage(res.data.package)
      setProductionGuide(res.data.guide)
      setBlueprint(res.data.blueprint)
    } catch (err) { console.error(err) }
    setContentLoading(false)
  }

  const improveScript = async () => {
    if (!scriptInput.trim()) return
    setScriptLoading(true)
    try {
      const res = await axios.post(`${API}/improve-script`, { script: scriptInput, niche: "general" })
      setImprovedScript(res.data.improved)
    } catch (err) { console.error(err) }
    setScriptLoading(false)
  }

  const repurposeContent = async () => {
    if (!repurposeInput.trim()) return
    setRepurposeLoading(true)
    try {
      const res = await axios.post(`${API}/repurpose`, { video_title: repurposeInput, niche: "general" })
      setRepurposed(res.data.repurposed)
    } catch (err) { console.error(err) }
    setRepurposeLoading(false)
  }

  const simulateGrowth = async () => {
    setGrowthLoading(true)
    try {
      const res = await axios.post(`${API}/growth-simulator`, growthForm, { params: { region } })
      setGrowthResult(res.data.simulation)
    } catch (err) { console.error(err) }
    setGrowthLoading(false)
  }

  const findCollabs = async () => {
    setCollabLoading(true)
    try {
      const res = await axios.post(`${API}/collab-finder`, collabForm, { params: { region } })
      setCollabResult(res.data.collabs)
    } catch (err) { console.error(err) }
    setCollabLoading(false)
  }

  const refreshAll = () => {
    fetchBriefing()
    fetchOpportunities()
    fetchSummary()
    fetchExtras()
  }

  const sendNotification = async () => {
    try {
      await axios.get(`${API}/notify`, { params: { region } })
      setNotified(true)
      setTimeout(() => setNotified(false), 3000)
    } catch (err) { console.error(err) }
  }

  useEffect(() => { refreshAll() }, [region])

  useEffect(() => {
    if (activeView === "intelligence") fetchIntelligence()
    if (activeView === "competitors") fetchCompetitors()
    if (activeView === "health") fetchHealth()
    if (activeView === "hooks") fetchHooks()
  }, [activeView])

  const views = [
    { id: "briefing", label: "Briefing" },
    { id: "opportunities", label: "Opportunities" },
    { id: "trends", label: "Trends" },
    { id: "intelligence", label: "Intelligence" },
    { id: "content", label: "Content Studio" },
    { id: "tools", label: "Tools" },
    { id: "competitors", label: "Competitors" },
    { id: "growth", label: "Growth" },
    { id: "hooks", label: "Hooks" },
    { id: "health", label: "API Health" }
  ]

  return (
    <div className="app">
      <header>
        <div className="header-top">
          <h1>Trend Radar</h1>
          {lastUpdated && <span className="last-updated">Updated {lastUpdated}</span>}
          {viralAlerts.length > 0 && (
            <span className="viral-badge">{viralAlerts.length} VIRAL</span>
          )}
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
        {views.map(v => (
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
              <div className="loading-box"><div className="pulse"></div><p>Generating morning briefing...</p></div>
            ) : briefing ? (
              <div className="briefing">
                <div className="briefing-greeting"><h2>{briefing.greeting}</h2></div>
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
                      <div className="top3-rank" style={{ background: URGENCY_COLORS[item.urgency] }}>#{item.rank}</div>
                      <h4>{item.topic}</h4>
                      <p>{item.why}</p>
                      <div className="top3-footer">
                        <span className="urgency-tag" style={{ color: URGENCY_COLORS[item.urgency], background: URGENCY_BG[item.urgency] }}>{item.urgency}</span>
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
                <div className="motivation-box"><p>{briefing.motivation}</p></div>
              </div>
            ) : <p className="empty">Click refresh to generate your morning briefing</p>}
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
                <div className="summary-loading"><div className="pulse"></div><p>Analyzing trends...</p></div>
              ) : <p>{summary || "Click refresh to generate summary"}</p>}
            </div>
            {oppsLoading ? (
              <div className="loading-box"><div className="pulse"></div><p>Scoring opportunities...</p></div>
            ) : (
              <div className="opp-board">
                {["post_now", "post_today", "post_week", "watch"].map(bucket => {
                  const items = opportunities ? opportunities[bucket] : []
                  const labels = { post_now: "Post Now", post_today: "Post Today", post_week: "Post This Week", watch: "Watch" }
                  const label = labels[bucket]
                  return (
                    <div key={bucket} className="opp-column">
                      <div className="opp-column-header" style={{ borderColor: URGENCY_COLORS[label] }}>
                        <span style={{ color: URGENCY_COLORS[label] }}>{label}</span>
                        <span className="opp-count">{items ? items.length : 0}</span>
                      </div>
                      {items && items.map((opp, i) => (
                        <div key={i} className="opp-card" style={{ borderLeft: `3px solid ${URGENCY_COLORS[label]}` }} onClick={() => fetchContentPackage(opp)}>
                          <img src={opp.thumbnail} alt={opp.title} className="opp-thumb" />
                          <div className="opp-info">
                            <p className="opp-title">{opp.title}</p>
                            <p className="opp-channel">{opp.channel}</p>
                            <div className="opp-stats">
                              <span>Score: {opp.opportunity_score}/100</span>
                              <span>{Number(opp.views).toLocaleString()} views</span>
                            </div>
                            {opp.reasons && opp.reasons[0] && <p className="opp-reason">{opp.reasons[0]}</p>}
                          </div>
                          <div className="opp-action">Tap for content</div>
                        </div>
                      ))}
                      {(!items || items.length === 0) && <p className="empty-col">No items</p>}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )}

        {activeView === "trends" && (
          <div className="view">
            {viralAlerts.length > 0 && (
              <div className="viral-section">
                <h3 className="section-label viral-label">Super Viral Alerts</h3>
                {viralAlerts.map((alert, i) => (
                  <div key={i} className="viral-card">
                    <img src={alert.thumbnail} alt={alert.title} className="viral-thumb" />
                    <div className="viral-info">
                      <p className="viral-title">{alert.title}</p>
                      <p className="viral-velocity">{Number(alert.velocity).toLocaleString()} views/hour</p>
                    </div>
                    <span className="viral-tag">VIRAL</span>
                  </div>
                ))}
              </div>
            )}
            <div className="trends-grid">
              <div className="trends-section">
                <h3 className="section-label">Google Trends</h3>
                <div className="list">
                  {googleTrends.length === 0 ? <p className="empty">No Google Trends available</p> :
                    googleTrends.map((term, i) => (
                      <a key={i} href={"https://www.google.com/search?q=" + encodeURIComponent(term)} target="_blank" rel="noreferrer" className="list-item">
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
                  {news.length === 0 ? <p className="empty">No news available</p> :
                    news.map((article, i) => (
                      <a key={i} href={article.url} target="_blank" rel="noreferrer" className="list-item">
                        <span className="news-source">{article.source}</span>
                        <span className="post-title">{article.title}</span>
                        <span className="arrow">→</span>
                      </a>
                    ))}
                </div>
              </div>
            </div>
            {predictions.length > 0 && (
              <div className="predictions-section">
                <h3 className="section-label">Trend Predictions</h3>
                <div className="predictions-grid">
                  {predictions.map((pred, i) => (
                    <div key={i} className="prediction-card">
                      <div className="pred-header">
                        <span className="pred-trend">{pred.predicted_trend}</span>
                        <span className={"pred-confidence conf-" + pred.confidence.toLowerCase()}>{pred.confidence}</span>
                      </div>
                      <p className="pred-reason">{pred.reason}</p>
                      <p className="pred-time">Expected: {pred.timeframe}</p>
                      <p className="pred-action">{pred.content_opportunity}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeView === "intelligence" && (
          <div className="view">
            <div className="intel-grid">
              <div className="intel-section">
                <h3 className="section-label">Cross-Language Trends</h3>
                {crossLanguage ? (
                  <div>
                    {crossLanguage.analysis && crossLanguage.analysis.map((item, i) => (
                      <div key={i} className="intel-card">
                        <div className="intel-header">
                          <span className="intel-trend">{item.trend}</span>
                          <span className={"intel-badge badge-" + item.crossover_potential.toLowerCase()}>{item.crossover_potential} crossover</span>
                        </div>
                        <p className="intel-lang">{item.language}</p>
                        <p className="intel-reason">{item.reason}</p>
                        <p className="intel-angle">{item.english_angle}</p>
                        <p className="intel-time">Expected: {item.timeframe}</p>
                      </div>
                    ))}
                  </div>
                ) : <p className="empty">Loading cross-language data...</p>}
              </div>

              <div className="intel-section">
                <h3 className="section-label">Trend Time Machine</h3>
                {timeMachine ? (
                  <div>
                    {timeMachine.cycling_trends && timeMachine.cycling_trends.map((trend, i) => (
                      <div key={i} className="intel-card">
                        <div className="intel-header">
                          <span className="intel-trend">{trend.trend}</span>
                          <span className={"intel-badge badge-" + trend.comeback_likelihood.toLowerCase()}>{trend.comeback_likelihood} comeback</span>
                        </div>
                        <p className="intel-reason">{trend.why}</p>
                        <p className="intel-time">Prepare by: {trend.prepare_by}</p>
                      </div>
                    ))}
                  </div>
                ) : <p className="empty">Loading time machine data...</p>}
              </div>

              <div className="intel-section">
                <h3 className="section-label">Best Niches Right Now</h3>
                {niches.length > 0 ? niches.map((niche, i) => (
                  <div key={i} className="intel-card">
                    <div className="intel-header">
                      <span className="intel-trend">{niche.niche}</span>
                      <span className="intel-score">Score: {niche.opportunity_score}/100</span>
                    </div>
                    <p className="intel-reason">{niche.why_opportunity}</p>
                    <div className="intel-meta">
                      <span>Competition: {niche.competition_level}</span>
                      <span>Growth time: {niche.time_to_grow}</span>
                    </div>
                  </div>
                )) : <p className="empty">Loading niches...</p>}
              </div>

              <div className="intel-section">
                <h3 className="section-label">Monetization Intelligence</h3>
                {monetization ? (
                  <div>
                    <div className="intel-card">
                      <h4>Best Path to Money</h4>
                      <p>{monetization.best_monetization_path}</p>
                    </div>
                    {monetization.brand_opportunities && monetization.brand_opportunities.map((opp, i) => (
                      <div key={i} className="intel-card">
                        <div className="intel-header">
                          <span className="intel-trend">{opp.brand_category}</span>
                          <span className="intel-score">{opp.estimated_deal_value}</span>
                        </div>
                        <p className="intel-reason">{opp.pitch_angle}</p>
                      </div>
                    ))}
                  </div>
                ) : <p className="empty">Loading monetization data...</p>}
              </div>
            </div>
          </div>
        )}

        {activeView === "content" && (
          <div className="view">
            {!selectedVideo ? (
              <div className="empty-content">
                <p>Tap any opportunity card to generate a full content package</p>
                <button onClick={() => setActiveView("opportunities")} className="go-btn">View Opportunities</button>
              </div>
            ) : contentLoading ? (
              <div className="loading-box">
                <div className="pulse"></div>
                <p>Generating your full content package...</p>
                <p className="loading-sub">Script, hooks, blueprint, production guide and more</p>
              </div>
            ) : contentPackage ? (
              <div className="content-studio">
                <div className="content-header">
                  <img src={selectedVideo.thumbnail} alt={selectedVideo.title} className="content-thumb" />
                  <div className="content-video-info">
                    <h2>{selectedVideo.title}</h2>
                    <p>{selectedVideo.channel}</p>
                    <div className="content-meta">
                      <span className="urgency-tag" style={{ color: URGENCY_COLORS[selectedVideo.urgency], background: URGENCY_BG[selectedVideo.urgency] }}>{selectedVideo.urgency}</span>
                      <span>Score: {selectedVideo.opportunity_score}/100</span>
                      <span>{contentPackage.difficulty} difficulty</span>
                      <span>Expires: {contentPackage.expiry}</span>
                    </div>
                  </div>
                </div>

                <div className="content-tabs">
                  {["script", "titles", "production", "blueprint", "insights"].map(tab => (
                    <button key={tab} className={activeContentTab === tab ? "active" : ""} onClick={() => setActiveContentTab(tab)}>
                      {tab.charAt(0).toUpperCase() + tab.slice(1)}
                    </button>
                  ))}
                </div>

                {activeContentTab === "script" && (
                  <div className="content-panel">
                    <div className="info-box"><p>{contentPackage.trend_explanation}</p></div>
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
                        <div key={i} className="title-option"><span className="title-rank">#{i + 1}</span><span>{t}</span></div>
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
                      <div className="prod-meta-item"><span className="prod-label">Time needed</span><span>{productionGuide.total_time_needed}</span></div>
                      <div className="prod-meta-item"><span className="prod-label">Best app</span><span>{productionGuide.recommended_app}</span></div>
                      <div className="prod-meta-item"><span className="prod-label">Sound</span><span>{productionGuide.recommended_sound}</span></div>
                      <div className="prod-meta-item"><span className="prod-label">Export</span><span>{productionGuide.export_settings}</span></div>
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
                        <div key={i} className="checklist-item"><span className="check">✓</span><span>{item}</span></div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Common Mistakes to Avoid</h4>
                      {productionGuide.common_mistakes && productionGuide.common_mistakes.map((item, i) => (
                        <div key={i} className="mistake-item"><span className="x-mark">✕</span><span>{item}</span></div>
                      ))}
                    </div>
                  </div>
                )}

                {activeContentTab === "blueprint" && blueprint && (
                  <div className="content-panel">
                    <div className="prod-meta">
                      <div className="prod-meta-item"><span className="prod-label">Style</span><span>{blueprint.video_style}</span></div>
                      <div className="prod-meta-item"><span className="prod-label">Duration</span><span>{blueprint.total_duration}</span></div>
                      <div className="prod-meta-item"><span className="prod-label">CapCut Template</span><span>{blueprint.capcut_template}</span></div>
                      <div className="prod-meta-item"><span className="prod-label">Color Grade</span><span>{blueprint.color_grade}</span></div>
                    </div>
                    <div className="content-block">
                      <h4>Storyboard</h4>
                      {blueprint.storyboard && blueprint.storyboard.map((scene, i) => (
                        <div key={i} className="scene-item">
                          <div className="scene-time">{scene.timestamp}</div>
                          <div className="scene-content">
                            <p className="scene-visual"><strong>Visual:</strong> {scene.visual}</p>
                            <p className="scene-audio"><strong>Audio:</strong> {scene.audio}</p>
                            {scene.text_overlay && <p className="scene-text"><strong>Text:</strong> {scene.text_overlay}</p>}
                            <p className="scene-action"><strong>Action:</strong> {scene.action}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>B-Roll Needed</h4>
                      {blueprint.broll_needed && blueprint.broll_needed.map((broll, i) => (
                        <div key={i} className="broll-item">
                          <p>{broll.description}</p>
                          <a href={"https://www.pexels.com/search/" + encodeURIComponent(broll.search_term)} target="_blank" rel="noreferrer" className="broll-link">
                            Search on {broll.free_source} →
                          </a>
                        </div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Final Checklist</h4>
                      {blueprint.final_checklist && blueprint.final_checklist.map((item, i) => (
                        <div key={i} className="checklist-item"><span className="check">✓</span><span>{item}</span></div>
                      ))}
                    </div>
                  </div>
                )}

                {activeContentTab === "insights" && (
                  <div className="content-panel">
                    <div className="insights-grid">
                      <div className="insight-card"><h5>Sentiment</h5><p>{contentPackage.sentiment}</p></div>
                      <div className="insight-card"><h5>Trend Origin</h5><p>{contentPackage.trend_origin}</p></div>
                      <div className="insight-card"><h5>Difficulty</h5><p>{contentPackage.difficulty}</p></div>
                      <div className="insight-card"><h5>Evergreen Score</h5><p>{contentPackage.evergreen_score}/10</p></div>
                    </div>
                    <div className="content-block">
                      <h4>Series Potential</h4>
                      <p>{contentPackage.series_potential}</p>
                    </div>
                    <div className="content-block">
                      <h4>Unique Angles Nobody Is Covering</h4>
                      {contentPackage.similar_angles && contentPackage.similar_angles.map((angle, i) => (
                        <div key={i} className="angle-item"><span className="angle-num">#{i + 1}</span><span>{angle}</span></div>
                      ))}
                    </div>
                    {contentPackage.controversy_warning && (
                      <div className="warning-box">
                        <h5>Controversy Warning</h5>
                        <p>{contentPackage.controversy_warning}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ) : null}
          </div>
        )}

        {activeView === "tools" && (
          <div className="view">
            <div className="tools-grid">
              <div className="tool-section">
                <h3 className="section-label">Script Improver</h3>
                <textarea
                  className="tool-input"
                  placeholder="Paste your script here..."
                  value={scriptInput}
                  onChange={e => setScriptInput(e.target.value)}
                  rows={6}
                />
                <button onClick={improveScript} className="tool-btn" disabled={scriptLoading}>
                  {scriptLoading ? "Improving..." : "Improve My Script"}
                </button>
                {improvedScript && (
                  <div className="tool-result">
                    <div className="content-block">
                      <h4>Improved Script</h4>
                      <div className="script-box">{improvedScript.improved_script}</div>
                    </div>
                    <div className="content-block">
                      <h4>Changes Made</h4>
                      {improvedScript.changes_made && improvedScript.changes_made.map((c, i) => (
                        <div key={i} className="checklist-item"><span className="check">✓</span><span>{c}</span></div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Why It's Better</h4>
                      <p>{improvedScript.why_better}</p>
                    </div>
                  </div>
                )}
              </div>

              <div className="tool-section">
                <h3 className="section-label">Content Repurposer</h3>
                <input
                  className="tool-input-line"
                  placeholder="Enter video title to repurpose..."
                  value={repurposeInput}
                  onChange={e => setRepurposeInput(e.target.value)}
                />
                <button onClick={repurposeContent} className="tool-btn" disabled={repurposeLoading}>
                  {repurposeLoading ? "Repurposing..." : "Repurpose Content"}
                </button>
                {repurposed && (
                  <div className="tool-result">
                    <div className="content-block">
                      <h4>3 Shorts Angles</h4>
                      {repurposed.shorts_angles && repurposed.shorts_angles.map((angle, i) => (
                        <div key={i} className="repurpose-angle">
                          <p className="angle-title">{angle.angle}</p>
                          <p className="angle-hook">{angle.hook}</p>
                        </div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Twitter Thread</h4>
                      {repurposed.twitter_thread && repurposed.twitter_thread.map((tweet, i) => (
                        <div key={i} className="tweet-item">{tweet}</div>
                      ))}
                    </div>
                    <div className="content-block">
                      <h4>Instagram Caption</h4>
                      <p>{repurposed.instagram_caption}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {activeView === "competitors" && (
          <div className="view">
            <div className="competitor-search">
              <h3 className="section-label">Track a Channel</h3>
              <div className="search-row">
                <input
                  className="tool-input-line"
                  placeholder="Search for a YouTube channel..."
                  value={competitorSearch}
                  onChange={e => setCompetitorSearch(e.target.value)}
                  onKeyDown={e => e.key === "Enter" && searchCompetitors()}
                />
                <button onClick={searchCompetitors} className="tool-btn-inline">Search</button>
              </div>
              {competitorResults.length > 0 && (
                <div className="search-results">
                  {competitorResults.map((ch, i) => (
                    <div key={i} className="search-result-item">
                      <img src={ch.thumbnail} alt={ch.name} className="ch-thumb" />
                      <div className="ch-info">
                        <p className="ch-name">{ch.name}</p>
                        <p className="ch-desc">{ch.description}</p>
                      </div>
                      <button onClick={() => addCompetitor(ch)} className="add-btn">Track</button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {competitors.length > 0 && (
              <div className="competitors-list">
                <h3 className="section-label">Tracked Channels ({competitors.length})</h3>
                {competitorData.map((comp, i) => (
                  <div key={i} className="competitor-card">
                    <div className="comp-header">
                      <img src={comp.channel.thumbnail} alt={comp.channel.name} className="comp-thumb" />
                      <div className="comp-info">
                        <h4>{comp.channel.name}</h4>
                        <p>Total views (recent): {Number(comp.total_views).toLocaleString()}</p>
                      </div>
                      <button onClick={() => removeCompetitor(comp.channel.id)} className="remove-btn">Remove</button>
                    </div>
                    <div className="comp-videos">
                      {comp.recent_videos && comp.recent_videos.map((video, j) => (
                        <div key={j} className="comp-video">
                          <img src={video.thumbnail} alt={video.title} className="comp-video-thumb" />
                          <div className="comp-video-info">
                            <p>{video.title}</p>
                            <span>{Number(video.views).toLocaleString()} views</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {competitors.length === 0 && (
              <p className="empty">Search for channels above to start tracking competitors</p>
            )}
          </div>
        )}

        {activeView === "growth" && (
          <div className="view">
            <div className="growth-section">
              <h3 className="section-label">Growth Simulator</h3>
              <div className="growth-form">
                <div className="form-row">
                  <label>Current Subscribers</label>
                  <input type="number" value={growthForm.subscribers} onChange={e => setGrowthForm({...growthForm, subscribers: parseInt(e.target.value)})} className="form-input" />
                </div>
                <div className="form-row">
                  <label>Average Views Per Video</label>
                  <input type="number" value={growthForm.avg_views} onChange={e => setGrowthForm({...growthForm, avg_views: parseInt(e.target.value)})} className="form-input" />
                </div>
                <div className="form-row">
                  <label>Videos Per Week</label>
                  <input type="number" value={growthForm.posts_per_week} onChange={e => setGrowthForm({...growthForm, posts_per_week: parseInt(e.target.value)})} className="form-input" />
                </div>
                <div className="form-row">
                  <label>Your Niche</label>
                  <input type="text" value={growthForm.niche} onChange={e => setGrowthForm({...growthForm, niche: e.target.value})} className="form-input" placeholder="e.g. football, memes, music" />
                </div>
                <button onClick={simulateGrowth} className="tool-btn" disabled={growthLoading}>
                  {growthLoading ? "Simulating..." : "Simulate My Growth"}
                </button>
              </div>

              {growthResult && (
                <div className="growth-result">
                  <div className="content-block">
                    <h4>Channel Analysis</h4>
                    <p>{growthResult.current_analysis}</p>
                  </div>
                  <div className="scenarios-grid">
                    {growthResult.scenarios && growthResult.scenarios.map((scenario, i) => (
                      <div key={i} className="scenario-card">
                        <h4>{scenario.name}</h4>
                        <p className="scenario-freq">{scenario.frequency}</p>
                        <div className="scenario-stats">
                          <div className="stat-row"><span>30 days</span><span>{scenario["30_days"]?.subscribers?.toLocaleString()} subs</span></div>
                          <div className="stat-row"><span>90 days</span><span>{scenario["90_days"]?.subscribers?.toLocaleString()} subs</span></div>
                          <div className="stat-row"><span>6 months</span><span>{scenario["6_months"]?.subscribers?.toLocaleString()} subs</span></div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="content-block">
                    <h4>Key Milestones</h4>
                    {growthResult.key_milestones && growthResult.key_milestones.map((m, i) => (
                      <div key={i} className="milestone-item">
                        <span className="milestone-name">{m.milestone}</span>
                        <span className="milestone-when">{m.estimated_when}</span>
                        <p className="milestone-what">{m.what_changes}</p>
                      </div>
                    ))}
                  </div>
                  <div className="content-block">
                    <h4>Biggest Growth Lever</h4>
                    <p>{growthResult.biggest_growth_lever}</p>
                  </div>
                </div>
              )}
            </div>

            <div className="collab-section">
              <h3 className="section-label">Collab Finder</h3>
              <div className="growth-form">
                <div className="form-row">
                  <label>Your Niche</label>
                  <input type="text" value={collabForm.niche} onChange={e => setCollabForm({...collabForm, niche: e.target.value})} className="form-input" placeholder="e.g. football, memes" />
                </div>
                <div className="form-row">
                  <label>Your Subscribers</label>
                  <input type="number" value={collabForm.subscribers} onChange={e => setCollabForm({...collabForm, subscribers: parseInt(e.target.value)})} className="form-input" />
                </div>
                <button onClick={findCollabs} className="tool-btn" disabled={collabLoading}>
                  {collabLoading ? "Finding..." : "Find Collab Opportunities"}
                </button>
              </div>
              {collabResult && collabResult.map((collab, i) => (
                <div key={i} className="collab-card">
                  <h4>{collab.creator_name}</h4>
                  <p className="collab-why">{collab.why_good_fit}</p>
                  <p className="collab-idea">{collab.collab_idea}</p>
                  <div className="collab-pitch">
                    <h5>Ready to Send Pitch:</h5>
                    <p>{collab.pitch_message}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeView === "hooks" && (
          <div className="view">
            <h3 className="section-label">Hook Database</h3>
            {hooks.length === 0 ? (
              <div className="empty-content">
                <p>Your hook database is empty. Generate content packages to automatically save hooks here.</p>
              </div>
            ) : (
              <div className="hooks-grid">
                {hooks.map((hook, i) => (
                  <div key={i} className="hook-card">
                    <div className="hook-card-header">
                      <span className="hook-type">{hook.type}</span>
                      <span className="hook-trend">{hook.trend}</span>
                    </div>
                    <p className="hook-text">{hook.hook}</p>
                    <p className="hook-why">{hook.why_it_works}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeView === "health" && (
          <div className="view">
            <h3 className="section-label">API Health Monitor</h3>
            <button onClick={fetchHealth} className="tool-btn" style={{marginBottom: "1rem"}}>Refresh Health Check</button>
            {health ? (
              <div className="health-grid">
                {Object.entries(health).filter(([k]) => k !== "checked_at").map(([api, status]) => (
                  <div key={api} className={"health-card status-" + status.status}>
                    <h4>{api.toUpperCase()}</h4>
                    <span className={"health-status " + status.status}>{status.status}</span>
                    {status.latency_ms && <p>{status.latency_ms}ms</p>}
                    {status.error && <p className="health-error">{status.error}</p>}
                  </div>
                ))}
              </div>
            ) : <p className="empty">Loading health data...</p>}
          </div>
        )}

      </main>
    </div>
  )
}
