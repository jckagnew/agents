// Enhanced Market Research Script
// Supports multiple market categories and interactive updates

const fs = require('fs');
const path = require('path');

// --- CONFIGURATION ---
const CONFIG_FILE = path.join(__dirname, 'market_config.json');
const YOUR_PRODUCT_NAME = "jckagnew-agents";
// --- END CONFIGURATION ---

const SERPER_API_KEY = process.env.SERPER_API_KEY;
const XAI_API_KEY = process.env.XAI_API_KEY;
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;

// Load market configuration
function loadMarketConfig() {
  try {
    const configData = fs.readFileSync(CONFIG_FILE, 'utf8');
    return JSON.parse(configData);
  } catch (error) {
    console.error('Error loading market config:', error);
    return { markets: [] };
  }
}

// Save market configuration
function saveMarketConfig(config) {
  config.lastUpdated = new Date().toISOString();
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

async function fetchSerper(query) {
  const response = await fetch("https://google.serper.dev/search", {
    method: "POST",
    headers: { "X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({ q: query }),
  });
  const data = await response.json();
  return data.organic ? data.organic.map((r) => r.snippet).join("\n") : "";
}

async function fetchGrok(snippets, query) {
  if (!snippets || snippets.trim().length === 0) {
    return "No recent information found for this query.";
  }

  const response = await fetch("https://api.x.ai/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${XAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "grok-1",
      messages: [
        {
          role: "system",
          content:
            "You are a market analyst. I will give you a list of search snippets and a query. Summarize the real-time public sentiment based *only* on these snippets. Be concise and focus on trends, opportunities, and concerns.",
        },
        {
          role: "user",
          content: `Query: ${query}\n\nSnippets:\n${snippets}`,
        },
      ],
    }),
  });
  const data = await response.json();
  return data.choices?.[0]?.message?.content || "Unable to analyze sentiment.";
}

async function fetchClaude(marketReports) {
  const marketsSection = marketReports.map((report, idx) => 
    `### ${report.market.name}\n${report.sentiment}\n`
  ).join('\n');

  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "x-api-key": ANTHROPIC_API_KEY,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: "claude-3-haiku-20240307",
      max_tokens: 4096,
      messages: [
        {
          role: "user",
          content: `You are a business strategist. Write a comprehensive "Daily Market Intelligence Report" based on the following market research across ${marketReports.length} market categories.

## Market Research Summary

${marketsSection}

---

## Report Structure

Please provide:

1. **Executive Summary** (2-3 bullet points)
2. **Market-by-Market Analysis** (for each market):
   - Key trends
   - Top opportunities
   - Potential threats
   - Notable competitor activity
3. **Cross-Market Insights** (patterns across markets)
4. **Strategic Recommendations** (top 3-5 actionable insights)
5. **Research Configuration** (list current markets being tracked)

Be concise but thorough. Focus on actionable intelligence.`,
        },
      ],
    }),
  });
  const data = await response.json();
  return data.content?.[0]?.text || "Unable to generate report.";
}

async function researchMarket(market) {
  console.error(`Researching market: ${market.name}...`);
  
  // Search for market trends and competitor activity
  const marketQuery = `${market.keywords.join(' OR ')} trends OR news OR updates`;
  const competitorQuery = market.competitors.length > 0 
    ? `${market.competitors.join(' OR ')} user feedback OR reviews OR complaints`
    : `${market.keywords[0]} user feedback`;

  const marketSnippets = await fetchSerper(marketQuery);
  const competitorSnippets = await fetchSerper(competitorQuery);
  
  const combinedSnippets = [marketSnippets, competitorSnippets]
    .filter(s => s && s.trim().length > 0)
    .join('\n\n');

  const sentiment = await fetchGrok(
    combinedSnippets,
    `What are the latest trends, opportunities, and concerns in ${market.name}? Focus on: ${market.description}`
  );

  return {
    market,
    sentiment,
    searchResults: {
      market: marketSnippets.substring(0, 500),
      competitors: competitorSnippets.substring(0, 500)
    }
  };
}

async function generateInteractivePrompt(config) {
  const marketsList = config.markets.map((m, idx) => 
    `${idx + 1}. **${m.name}** - ${m.description}\n   Competitors: ${m.competitors.join(', ')}`
  ).join('\n\n');

  return `## 📊 Current Research Configuration

We are currently tracking **${config.markets.length} markets**:

${marketsList}

---

## 💬 Interactive Updates

**To modify this research:**

1. **Add a new market**: Comment with \`/add-market [name] [description]\`
2. **Remove a market**: Comment with \`/remove-market [market-id]\`
3. **Update competitors**: Comment with \`/update-competitors [market-id] [competitor1, competitor2, ...]\`
4. **Add keywords**: Comment with \`/add-keywords [market-id] [keyword1, keyword2, ...]\`

**Examples:**
- \`/add-market "AI Tutoring" "AI-powered educational tutoring platforms"\`
- \`/remove-market software-factory\`
- \`/update-competitors enterprise-sales "Salesforce, HubSpot, Outreach, Gong"\`

---

*This configuration will be updated automatically based on your comments.*`;
}

async function main() {
  try {
    const config = loadMarketConfig();
    
    if (config.markets.length === 0) {
      console.error("No markets configured. Please check market_config.json");
      process.exit(1);
    }

    console.error(`Starting research for ${config.markets.length} markets...`);

    // Research each market
    const marketReports = [];
    for (const market of config.markets) {
      try {
        const report = await researchMarket(market);
        marketReports.push(report);
        // Small delay to avoid rate limits
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error(`Error researching ${market.name}:`, error);
        marketReports.push({
          market,
          sentiment: `Error: ${error.message}`,
          searchResults: {}
        });
      }
    }

    // Generate comprehensive report with Claude
    const finalReport = await fetchClaude(marketReports);

    // Generate interactive prompt
    const interactivePrompt = await generateInteractivePrompt(config);

    // Combine report with interactive section
    const fullReport = `${finalReport}\n\n---\n\n${interactivePrompt}`;

    // Save updated config
    saveMarketConfig(config);

    // Print report to stdout for GitHub Action to catch
    console.log(fullReport);
  } catch (error) {
    console.error("Error generating report:", error);
    process.exit(1);
  }
}

main();
