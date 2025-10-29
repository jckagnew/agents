#!/usr/bin/env node

const { Anthropic } = require('@anthropic-ai/sdk');
const OpenAI = require('openai');
const fetch = require('node-fetch');

const defaultProvider = process.env.LLM_DEFAULT_PROVIDER || 'claude';

const anthropic = () => {
  if (!process.env.ANTHROPIC_API_KEY) throw new Error('ANTHROPIC_API_KEY missing');
  const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
  return async ({ prompt, maxTokens = 2048 }) => {
    const response = await client.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: maxTokens,
      messages: [{ role: 'user', content: prompt }]
    });
    return response.content?.[0]?.text || '';
  };
};

const openai = () => {
  if (!process.env.OPENAI_API_KEY) throw new Error('OPENAI_API_KEY missing');
  const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  return async ({ prompt, maxTokens = 2048, model = 'gpt-4.1' }) => {
    const response = await client.responses.create({
      model,
      input: prompt,
      max_output_tokens: maxTokens
    });
    return response.output_text;
  };
};

const gemini = () => {
  if (!process.env.GOOGLE_API_KEY) throw new Error('GOOGLE_API_KEY missing');
  const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent';
  return async ({ prompt, maxTokens = 2048 }) => {
    const res = await fetch(`${endpoint}?key=${process.env.GOOGLE_API_KEY}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: prompt }] }],
        generationConfig: { maxOutputTokens: maxTokens }
      })
    });
    const json = await res.json();
    if (json.error) throw new Error(JSON.stringify(json.error));
    return json.candidates?.[0]?.content?.parts?.map(p => p.text).join('\n') || '';
  };
};

const fallbacks = {
  claude: ['openai', 'gemini'],
  openai: ['claude', 'gemini'],
  gemini: ['claude', 'openai'],
  groq: ['openai', 'claude']
};

const factories = {
  claude: anthropic,
  openai,
  gemini
};

const getClient = (provider = defaultProvider, used = new Set()) => {
  const normalized = provider.toLowerCase();
  if (!factories[normalized]) {
    const fallback = fallbacks[normalized]?.find(p => !used.has(p));
    if (fallback) return getClient(fallback, used);
    throw new Error(`No LLM factory found for provider: ${provider}`);
  }
  used.add(normalized);
  return factories[normalized]();
};

module.exports = { getClient };
