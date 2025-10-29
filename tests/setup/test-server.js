const express = require('express')
const cors = require('cors')
const path = require('path')

const app = express()
const PORT = process.env.PORT || 3001

// Middleware
app.use(cors())
app.use(express.json())
app.use(express.static(path.join(__dirname, '../../dist')))

// Test API routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

app.post('/api/test/setup', (req, res) => {
  // Setup test data
  res.json({ message: 'Test data setup complete' })
})

app.post('/api/test/cleanup', (req, res) => {
  // Cleanup test data
  res.json({ message: 'Test data cleanup complete' })
})

// Mock API routes for testing
app.get('/api/weight-entries', (req, res) => {
  res.json([
    {
      id: '1',
      weight: 70.5,
      bodyFat: 15.0,
      date: new Date().toISOString(),
      notes: 'Test entry'
    }
  ])
})

app.post('/api/weight-entries', (req, res) => {
  const entry = {
    id: Date.now().toString(),
    ...req.body,
    createdAt: new Date().toISOString()
  }
  res.status(201).json(entry)
})

app.get('/api/goals', (req, res) => {
  res.json([
    {
      id: '1',
      targetWeight: 65.0,
      targetBodyFat: 12.0,
      targetDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
      isActive: true
    }
  ])
})

app.post('/api/goals', (req, res) => {
  const goal = {
    id: Date.now().toString(),
    ...req.body,
    createdAt: new Date().toISOString()
  }
  res.status(201).json(goal)
})

// Error handling
app.use((err, req, res, next) => {
  console.error('Test server error:', err)
  res.status(500).json({ error: 'Internal server error' })
})

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found' })
})

// Start server
app.listen(PORT, () => {
  console.log(`🧪 Test server running on port ${PORT}`)
  console.log(`📡 Health check: http://localhost:${PORT}/api/health`)
})

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🛑 Test server shutting down...')
  process.exit(0)
})

process.on('SIGINT', () => {
  console.log('🛑 Test server shutting down...')
  process.exit(0)
})
