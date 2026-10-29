import { useState, useEffect, useRef } from 'react'
import { uploadCorpusFile, getCorpusStats } from '../api.js'

export default function DatasetUploader() {
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const [stats, setStats] = useState(null)
  const fileInputRef = useRef(null)

  function loadStats() {
    getCorpusStats()
      .then(setStats)
      .catch(() => {})
  }

  useEffect(() => {
    loadStats()
  }, [])

  function handleFileSelect(selectedFile) {
    if (!selectedFile) return
    const validExts = ['.csv', '.txt', '.pdf', '.docx', '.doc', '.json']
    const ext = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase()
    if (!validExts.includes(ext)) {
      setError(`Unsupported file type '${ext}'. Please upload a CSV, TXT, PDF, DOCX, or JSON file.`)
      setFile(null)
      return
    }
    setError('')
    setFile(selectedFile)
    setResult(null)
  }

  function handleDragOver(e) {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  function handleDragLeave(e) {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  function handleDrop(e) {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  }

  async function handleUpload() {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const data = await uploadCorpusFile(file)
      setResult(data)
      setFile(null)
      if (fileInputRef.current) fileInputRef.current.value = ''
      loadStats()
    } catch (err) {
      setError(err.message || 'Failed to upload and preprocess file.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      {/* Corpus Overview Summary Bar */}
      <div style={{
        background: 'linear-gradient(135deg, #1e1e2d 0%, #171725 100%)',
        border: '1px solid #3f3f5a',
        borderRadius: 12,
        padding: '16px 20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: 12
      }}>
        <div>
          <h3 style={{ margin: '0 0 4px', fontSize: 16, color: '#f8fafc', fontWeight: 600 }}>
            Active Dataset & NLP Vector Corpus
          </h3>
          <p style={{ margin: 0, fontSize: 13, color: '#94a3b8' }}>
            {stats ? (
              <span>
                Currently indexing <strong style={{ color: '#818cf8' }}>{stats.total_projects}</strong> historical projects across {Object.keys(stats.domain_distribution || {}).length} domains.
              </span>
            ) : 'Loading corpus statistics…'}
          </p>
        </div>
        <button
          onClick={loadStats}
          style={{
            background: '#2e2e42',
            color: '#cbd5e1',
            border: '1px solid #3f3f5a',
            borderRadius: 7,
            padding: '6px 14px',
            fontSize: 12,
            fontWeight: 500,
            cursor: 'pointer'
          }}
        >
          ↻ Refresh Stats
        </button>
      </div>

      {/* Main Upload Box */}
      <div style={{
        background: '#13131f',
        border: '1px solid #2e2e3a',
        borderRadius: 12,
        padding: 24,
      }}>
        <div style={{ marginBottom: 16 }}>
          <h2 style={{ margin: '0 0 6px', fontSize: 18, color: '#f1f5f9' }}>
            Add Historical Projects & Data Files
          </h2>
          <p style={{ margin: 0, fontSize: 13, color: '#94a3b8', lineHeight: 1.5 }}>
            Upload capstone project lists, syllabus files, or past project records in <strong>CSV, TXT, PDF, DOCX, or JSON</strong>.
            The pipeline automatically parses titles & abstracts, extracts <strong>tech stack & domain tags</strong> using NLP,
            skips duplicates, and hot-reloads the FAISS vector index in real time.
          </p>
        </div>

        {/* Drag and Drop Area */}
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current && fileInputRef.current.click()}
          style={{
            border: `2px dashed ${isDragging ? '#6366f1' : '#3f3f5a'}`,
            borderRadius: 12,
            padding: '36px 20px',
            textAlign: 'center',
            background: isDragging ? '#6366f115' : '#0d0d1a',
            cursor: 'pointer',
            transition: 'all .2s ease',
            marginBottom: 16
          }}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => handleFileSelect(e.target.files[0])}
            accept=".csv,.txt,.pdf,.docx,.doc,.json"
            style={{ display: 'none' }}
          />
          <div style={{ fontSize: 36, marginBottom: 10 }}>📁</div>
          <p style={{ margin: '0 0 8px', fontSize: 15, fontWeight: 600, color: '#e2e8f0' }}>
            Drag & drop your data file here, or{' '}
            <span style={{ color: '#818cf8', textDecoration: 'underline' }}>browse</span>
          </p>
          <p style={{ margin: 0, fontSize: 12, color: '#64748b' }}>
            Supported formats: .CSV, .TXT (one per line or Name, Roll, Title), .PDF, .DOCX, .JSON
          </p>
        </div>

        {/* Selected File Card */}
        {file && (
          <div style={{
            background: '#1e1e2d',
            border: '1px solid #3f3f5a',
            borderRadius: 8,
            padding: '12px 16px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: 16,
            gap: 10
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <span style={{
                background: '#6366f122',
                color: '#818cf8',
                padding: '4px 8px',
                borderRadius: 6,
                fontWeight: 700,
                fontSize: 11,
                border: '1px solid #6366f144'
              }}>
                {file.name.split('.').pop().toUpperCase()}
              </span>
              <div>
                <p style={{ margin: 0, fontSize: 14, fontWeight: 600, color: '#f8fafc' }}>
                  {file.name}
                </p>
                <p style={{ margin: 0, fontSize: 12, color: '#64748b' }}>
                  {(file.size / 1024).toFixed(1)} KB
                </p>
              </div>
            </div>

            <button
              onClick={(e) => {
                e.stopPropagation()
                setFile(null)
                if (fileInputRef.current) fileInputRef.current.value = ''
              }}
              style={{
                background: 'transparent',
                color: '#ef4444',
                border: 'none',
                cursor: 'pointer',
                fontSize: 14,
                padding: 6
              }}
            >
              ✕ Remove
            </button>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div style={{
            background: '#ef444415',
            border: '1px solid #ef444444',
            color: '#f87171',
            borderRadius: 8,
            padding: '10px 14px',
            fontSize: 13,
            marginBottom: 16
          }}>
            ⚠️ {error}
          </div>
        )}

        {/* Upload Action Button */}
        <div style={{ display: 'flex', gap: 10 }}>
          <button
            onClick={handleUpload}
            disabled={!file || loading}
            style={{
              background: !file || loading ? '#2e2e42' : '#6366f1',
              color: !file || loading ? '#64748b' : '#ffffff',
              border: 'none',
              borderRadius: 8,
              padding: '12px 24px',
              fontSize: 14,
              fontWeight: 600,
              cursor: !file || loading ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              transition: 'background .2s'
            }}
          >
            {loading ? '⚙️ Preprocessing & Indexing…' : '🚀 Upload & Preprocess into Corpus'}
          </button>
        </div>
      </div>

      {/* Post-Upload Results Banner & Preview */}
      {result && (
        <div style={{
          background: '#0d0d1a',
          border: '1px solid #22c55e44',
          borderRadius: 12,
          padding: 20
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
            <span style={{ fontSize: 20 }}>🎉</span>
            <div>
              <h3 style={{ margin: 0, fontSize: 16, color: '#22c55e', fontWeight: 600 }}>
                {result.message}
              </h3>
              <p style={{ margin: 0, fontSize: 12, color: '#94a3b8' }}>
                Source file: <code>{result.filename}</code>
              </p>
            </div>
          </div>

          {/* Metric Badges */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
            gap: 12,
            marginBottom: 16
          }}>
            <div style={{ background: '#171725', borderRadius: 8, padding: 12, border: '1px solid #2e2e3a' }}>
              <span style={{ fontSize: 11, color: '#64748b' }}>Records Parsed</span>
              <p style={{ margin: '4px 0 0', fontSize: 20, fontWeight: 700, color: '#e2e8f0' }}>
                {result.total_parsed}
              </p>
            </div>
            <div style={{ background: '#171725', borderRadius: 8, padding: 12, border: '1px solid #22c55e44' }}>
              <span style={{ fontSize: 11, color: '#22c55e' }}>New Projects Added</span>
              <p style={{ margin: '4px 0 0', fontSize: 20, fontWeight: 700, color: '#22c55e' }}>
                +{result.added_count}
              </p>
            </div>
            <div style={{ background: '#171725', borderRadius: 8, padding: 12, border: '1px solid #f59e0b44' }}>
              <span style={{ fontSize: 11, color: '#f59e0b' }}>Duplicates Skipped</span>
              <p style={{ margin: '4px 0 0', fontSize: 20, fontWeight: 700, color: '#f59e0b' }}>
                {result.duplicate_count}
              </p>
            </div>
            <div style={{ background: '#171725', borderRadius: 8, padding: 12, border: '1px solid #6366f144' }}>
              <span style={{ fontSize: 11, color: '#818cf8' }}>Total Corpus Size</span>
              <p style={{ margin: '4px 0 0', fontSize: 20, fontWeight: 700, color: '#818cf8' }}>
                {result.total_corpus_count}
              </p>
            </div>
          </div>

          {/* Sample Previews */}
          {result.added_entries && result.added_entries.length > 0 && (
            <div>
              <h4 style={{ margin: '0 0 10px', fontSize: 13, color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Preview of Preprocessed Projects Added:
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {result.added_entries.map((item) => (
                  <div key={item.id} style={{
                    background: '#13131f',
                    borderRadius: 8,
                    padding: '10px 14px',
                    border: '1px solid #2e2e3a'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                      <span style={{ fontSize: 14, fontWeight: 600, color: '#f1f5f9' }}>
                        {item.title}
                      </span>
                      <span style={{ fontSize: 11, color: '#818cf8', fontWeight: 600 }}>
                        {item.id} · {item.year}
                      </span>
                    </div>
                    <p style={{ margin: '0 0 6px', fontSize: 12, color: '#94a3b8' }}>
                      {item.abstract}
                    </p>
                    <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                      {item.domain_tags.map(d => (
                        <span key={d} style={{
                          fontSize: 10,
                          fontWeight: 600,
                          padding: '2px 6px',
                          borderRadius: 4,
                          background: '#3b82f622',
                          color: '#60a5fa',
                          border: '1px solid #3b82f644'
                        }}>
                          {d}
                        </span>
                      ))}
                      {item.tech_stack_tags.map(t => (
                        <span key={t} style={{
                          fontSize: 10,
                          fontWeight: 600,
                          padding: '2px 6px',
                          borderRadius: 4,
                          background: '#6366f122',
                          color: '#a5b4fc',
                          border: '1px solid #6366f144'
                        }}>
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Domain Distribution Card */}
      {stats && stats.domain_distribution && (
        <div style={{
          background: '#13131f',
          border: '1px solid #2e2e3a',
          borderRadius: 12,
          padding: 20
        }}>
          <h3 style={{ margin: '0 0 12px', fontSize: 15, color: '#f1f5f9', fontWeight: 600 }}>
            Corpus Domain Coverage
          </h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {Object.entries(stats.domain_distribution).map(([domain, count]) => (
              <span
                key={domain}
                style={{
                  background: '#1e1e2d',
                  border: '1px solid #3f3f5a',
                  color: '#cbd5e1',
                  borderRadius: 6,
                  padding: '5px 10px',
                  fontSize: 12,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 6
                }}
              >
                <strong style={{ color: '#e2e8f0', textTransform: 'capitalize' }}>{domain}</strong>
                <span style={{
                  background: '#6366f133',
                  color: '#a5b4fc',
                  padding: '1px 6px',
                  borderRadius: 999,
                  fontSize: 11,
                  fontWeight: 700
                }}>
                  {count}
                </span>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
