/**
 * Express.js Application Template
 */

const express = require('express');
const cors = require('cors');
require('dotenv').config();

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/', (req, res) => {
    res.json({
        status: 'healthy',
        message: 'API is running',
        project: process.env.PROJECT_NAME || 'Unknown',
        version: process.env.PROJECT_VERSION || '1.0.0'
    });
});

app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        message: 'Service is operational',
        project: process.env.PROJECT_NAME || 'Unknown',
        timestamp: new Date().toISOString()
    });
});

app.post('/items', (req, res) => {
    const { name, description, price, tax } = req.body;
    
    if (!name || !price) {
        return res.status(400).json({
            error: 'Name and price are required'
        });
    }
    
    const item = {
        id: Date.now(),
        name,
        description: description || '',
        price: parseFloat(price),
        tax: tax ? parseFloat(tax) : 0,
        total: parseFloat(price) + (tax ? parseFloat(tax) : 0)
    };
    
    res.json({
        message: `Item ${item.name} created successfully`,
        item
    });
});

app.get('/items/:id', (req, res) => {
    const { id } = req.params;
    
    if (isNaN(id) || parseInt(id) < 1) {
        return res.status(400).json({
            error: 'Item ID must be a positive number'
        });
    }
    
    res.json({
        item_id: parseInt(id),
        message: 'Item retrieved successfully'
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        error: 'Something went wrong!',
        message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
    });
});

// 404 handler
app.use('*', (req, res) => {
    res.status(404).json({
        error: 'Route not found',
        message: `Cannot ${req.method} ${req.originalUrl}`
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
    console.log(`📱 Project: ${process.env.PROJECT_NAME || 'Unknown'}`);
    console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
});

module.exports = app;
