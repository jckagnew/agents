// Test Code Examples for Claude Integration Testing
// C-Level Sales Guy LLC - Claude Integration Test

import React, { useState } from 'react';
import { createClient } from '@supabase/supabase-js';

// Test Component 1: Basic Contact Form (Needs Improvement)
export function ContactForm() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // Submit logic
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <button type="submit">Submit</button>
    </form>
  );
}

// Test Component 2: Business Expense Tracker (Needs TypeScript)
export function ExpenseTracker() {
  const [expenses, setExpenses] = useState([]);
  
  const addExpense = (expense) => {
    setExpenses([...expenses, expense]);
  };
  
  return (
    <div>
      <h2>Business Expenses</h2>
      {expenses.map(expense => (
        <div key={expense.id}>
          <span>{expense.description}</span>
          <span>${expense.amount}</span>
        </div>
      ))}
    </div>
  );
}

// Test Component 3: AI Integration (Needs Error Handling)
export function AIIntegration() {
  const [response, setResponse] = useState('');
  
  const callHuggingFace = async () => {
    const response = await fetch('/api/ai/generate', {
      method: 'POST',
      body: JSON.stringify({ prompt: 'Generate sales content' })
    });
    const data = await response.json();
    setResponse(data.text);
  };
  
  return (
    <div>
      <button onClick={callHuggingFace}>Generate Content</button>
      <div>{response}</div>
    </div>
  );
}

// Test API Route (Needs Security)
export async function POST(request) {
  const { prompt } = await request.json();
  
  const response = await fetch('https://api-inference.huggingface.co/models/gpt2', {
    headers: {
      'Authorization': `Bearer ${process.env.HF_TOKEN}`,
    },
    method: 'POST',
    body: JSON.stringify({ inputs: prompt }),
  });
  
  const result = await response.json();
  return Response.json({ text: result[0].generated_text });
}

// Test Database Query (Needs RLS)
export async function getBusinessData() {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  );
  
  const { data, error } = await supabase
    .from('business_expenses')
    .select('*');
    
  return data;
}

// Test Business Logic (Needs Validation)
export function calculateBusinessMetrics(expenses) {
  const total = expenses.reduce((sum, expense) => sum + expense.amount, 0);
  const average = total / expenses.length;
  
  return {
    total,
    average,
    count: expenses.length
  };
}

// Test AI Model Integration (Needs Error Handling)
export class HuggingFaceClient {
  constructor(token) {
    this.token = token;
  }
  
  async generateText(prompt) {
    const response = await fetch('https://api-inference.huggingface.co/models/gpt2', {
      headers: {
        'Authorization': `Bearer ${this.token}`,
      },
      method: 'POST',
      body: JSON.stringify({ inputs: prompt }),
    });
    
    return response.json();
  }
}

// Test Business Context (Needs Proper Structure)
export const businessContext = {
  name: 'C-Level Sales Guy LLC',
  type: 'Texas LLC',
  services: ['AI Development', 'Sales Consulting'],
  targetMarket: 'C-Level Executives'
};

// Test Error Handling (Needs Improvement)
export function handleAPIError(error) {
  console.log('Error occurred:', error);
  return 'Something went wrong';
}

// Test Security (Needs Validation)
export function validateUserInput(input) {
  if (input.length > 100) {
    return false;
  }
  return true;
}

// Test Performance (Needs Optimization)
export function processLargeDataset(data) {
  const results = [];
  for (let i = 0; i < data.length; i++) {
    results.push(processItem(data[i]));
  }
  return results;
}

function processItem(item) {
  // Simulate processing
  return item * 2;
}
