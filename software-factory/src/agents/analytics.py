"""
Analytics Agent

This agent handles analytics, metrics tracking, and business intelligence
for the software factory and individual projects.
"""

import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum


class MetricType(Enum):
    """Types of metrics"""
    REVENUE = "revenue"
    USER_ACQUISITION = "user_acquisition"
    ENGAGEMENT = "engagement"
    RETENTION = "retention"
    TECHNICAL = "technical"
    BUSINESS = "business"


@dataclass
class Metric:
    """Metric data structure"""
    name: str
    value: float
    type: MetricType
    timestamp: datetime
    project_id: str
    metadata: Dict[str, Any] = None


@dataclass
class Dashboard:
    """Dashboard data structure"""
    id: str
    name: str
    project_id: str
    widgets: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime


class RevenueAnalyticsAgent:
    """Handles revenue analytics and financial metrics"""
    
    async def track_revenue_metrics(self, project_id: str) -> Dict[str, Any]:
        """Track comprehensive revenue metrics"""
        await asyncio.sleep(0.3)  # Simulate data retrieval
        
        return {
            "mrr": {
                "current": 12500.0,
                "previous_month": 10800.0,
                "growth_rate": 0.157,
                "growth_amount": 1700.0
            },
            "arr": {
                "current": 150000.0,
                "projected": 180000.0,
                "growth_rate": 0.20
            },
            "revenue_by_tier": {
                "free": {"customers": 1000, "revenue": 0, "percentage": 0},
                "premium": {"customers": 200, "revenue": 1998.0, "percentage": 16.0},
                "pro": {"customers": 40, "revenue": 799.6, "percentage": 6.4},
                "enterprise": {"customers": 10, "revenue": 999.9, "percentage": 8.0}
            },
            "customer_metrics": {
                "total_customers": 1250,
                "new_customers_this_month": 150,
                "churned_customers_this_month": 25,
                "net_customer_growth": 125,
                "churn_rate": 0.02
            },
            "financial_health": {
                "ltv": 200.0,
                "cac": 45.0,
                "ltv_cac_ratio": 4.44,
                "payback_period": 4.5,  # months
                "gross_margin": 0.85
            }
        }
    
    async def analyze_revenue_trends(self, project_id: str, period: str = "6months") -> Dict[str, Any]:
        """Analyze revenue trends over time"""
        await asyncio.sleep(0.4)  # Simulate trend analysis
        
        return {
            "period": period,
            "mrr_trend": [
                {"month": "2024-01", "mrr": 5000, "growth": 0.25},
                {"month": "2024-02", "mrr": 6500, "growth": 0.30},
                {"month": "2024-03", "mrr": 7800, "growth": 0.20},
                {"month": "2024-04", "mrr": 9200, "growth": 0.18},
                {"month": "2024-05", "mrr": 10800, "growth": 0.17},
                {"month": "2024-06", "mrr": 12500, "growth": 0.16}
            ],
            "customer_trend": [
                {"month": "2024-01", "customers": 500, "growth": 0.20},
                {"month": "2024-02", "customers": 650, "growth": 0.30},
                {"month": "2024-03", "customers": 800, "growth": 0.23},
                {"month": "2024-04", "customers": 950, "growth": 0.19},
                {"month": "2024-05", "customers": 1125, "growth": 0.18},
                {"month": "2024-06", "customers": 1250, "growth": 0.11}
            ],
            "insights": [
                "MRR growth is slowing but still healthy at 16%",
                "Customer growth rate is declining, focus on retention",
                "Premium tier is driving most revenue growth",
                "Enterprise tier shows strong potential"
            ]
        }


class UserAnalyticsAgent:
    """Handles user behavior and engagement analytics"""
    
    async def track_user_engagement(self, project_id: str) -> Dict[str, Any]:
        """Track user engagement metrics"""
        await asyncio.sleep(0.3)  # Simulate data retrieval
        
        return {
            "daily_active_users": {
                "current": 850,
                "previous_week": 780,
                "growth_rate": 0.09
            },
            "monthly_active_users": {
                "current": 1200,
                "previous_month": 1100,
                "growth_rate": 0.09
            },
            "engagement_metrics": {
                "average_session_duration": 12.5,  # minutes
                "sessions_per_user": 8.2,
                "page_views_per_session": 4.8,
                "bounce_rate": 0.35
            },
            "feature_usage": {
                "expense_tracking": 0.85,
                "budget_planning": 0.65,
                "ai_insights": 0.45,
                "investment_tracking": 0.30,
                "bill_reminders": 0.55
            },
            "user_journey": {
                "signup_to_first_action": 0.75,  # 75% take first action
                "first_action_to_paid": 0.15,    # 15% convert to paid
                "time_to_first_value": 2.5,      # days
                "time_to_paid_conversion": 14.2  # days
            }
        }
    
    async def analyze_user_retention(self, project_id: str) -> Dict[str, Any]:
        """Analyze user retention patterns"""
        await asyncio.sleep(0.4)  # Simulate retention analysis
        
        return {
            "cohort_analysis": {
                "week_1_retention": 0.75,
                "week_4_retention": 0.45,
                "week_12_retention": 0.25,
                "week_24_retention": 0.15
            },
            "retention_by_tier": {
                "free": {
                    "week_1": 0.70,
                    "week_4": 0.35,
                    "week_12": 0.15
                },
                "premium": {
                    "week_1": 0.85,
                    "week_4": 0.65,
                    "week_12": 0.45
                },
                "pro": {
                    "week_1": 0.90,
                    "week_4": 0.80,
                    "week_12": 0.70
                }
            },
            "churn_analysis": {
                "primary_churn_reasons": [
                    "Lack of time to use the app",
                    "Found a better alternative",
                    "Too expensive",
                    "Not meeting needs"
                ],
                "churn_prediction": {
                    "high_risk_users": 45,
                    "medium_risk_users": 120,
                    "low_risk_users": 1085
                }
            }
        }


class TechnicalAnalyticsAgent:
    """Handles technical performance and system metrics"""
    
    async def track_technical_metrics(self, project_id: str) -> Dict[str, Any]:
        """Track technical performance metrics"""
        await asyncio.sleep(0.2)  # Simulate data retrieval
        
        return {
            "performance": {
                "average_response_time": 245,  # milliseconds
                "p95_response_time": 890,      # milliseconds
                "p99_response_time": 1200,     # milliseconds
                "uptime": 0.9995,             # 99.95%
                "error_rate": 0.001           # 0.1%
            },
            "infrastructure": {
                "cpu_usage": 0.45,            # 45%
                "memory_usage": 0.62,         # 62%
                "disk_usage": 0.35,           # 35%
                "database_connections": 45,
                "cache_hit_rate": 0.85        # 85%
            },
            "api_metrics": {
                "total_requests": 1250000,    # per day
                "successful_requests": 1248750,
                "failed_requests": 1250,
                "rate_limited_requests": 500,
                "average_requests_per_user": 1000
            },
            "security": {
                "failed_login_attempts": 25,
                "blocked_ips": 3,
                "security_incidents": 0,
                "vulnerability_scans": 1,
                "last_scan_date": "2024-01-15"
            }
        }
    
    async def analyze_system_health(self, project_id: str) -> Dict[str, Any]:
        """Analyze overall system health and performance"""
        await asyncio.sleep(0.3)  # Simulate health analysis
        
        return {
            "overall_health_score": 8.5,  # Out of 10
            "performance_score": 8.0,
            "reliability_score": 9.5,
            "security_score": 9.0,
            "scalability_score": 7.5,
            "recommendations": [
                "Consider database optimization for better response times",
                "Implement additional caching layers",
                "Set up automated scaling for peak usage",
                "Schedule regular security audits"
            ],
            "alerts": [
                {
                    "type": "warning",
                    "message": "Response time approaching threshold",
                    "severity": "medium",
                    "action_required": "Monitor and optimize queries"
                }
            ]
        }


class BusinessIntelligenceAgent:
    """Handles business intelligence and strategic analytics"""
    
    async def generate_business_insights(self, project_id: str) -> Dict[str, Any]:
        """Generate strategic business insights"""
        await asyncio.sleep(0.5)  # Simulate insight generation
        
        return {
            "market_position": {
                "market_share": 0.02,  # 2%
                "competitive_position": "growing",
                "differentiation_score": 8.5,
                "brand_awareness": 0.15  # 15%
            },
            "growth_opportunities": [
                {
                    "opportunity": "Enterprise market expansion",
                    "potential_revenue": 500000,
                    "effort_required": "high",
                    "timeline": "6-12 months"
                },
                {
                    "opportunity": "International expansion",
                    "potential_revenue": 300000,
                    "effort_required": "medium",
                    "timeline": "3-6 months"
                },
                {
                    "opportunity": "API monetization",
                    "potential_revenue": 150000,
                    "effort_required": "low",
                    "timeline": "1-3 months"
                }
            ],
            "risk_factors": [
                {
                    "risk": "Competitive pressure",
                    "probability": 0.7,
                    "impact": "medium",
                    "mitigation": "Focus on AI differentiation"
                },
                {
                    "risk": "Economic downturn",
                    "probability": 0.3,
                    "impact": "high",
                    "mitigation": "Diversify customer base"
                }
            ],
            "strategic_recommendations": [
                "Double down on AI features to maintain competitive advantage",
                "Invest in enterprise sales team for B2B growth",
                "Expand internationally to reduce market concentration",
                "Develop API ecosystem for additional revenue streams"
            ]
        }
    
    async def analyze_customer_lifetime_value(self, project_id: str) -> Dict[str, Any]:
        """Analyze customer lifetime value patterns"""
        await asyncio.sleep(0.4)  # Simulate CLV analysis
        
        return {
            "overall_clv": 200.0,
            "clv_by_tier": {
                "free": 0.0,
                "premium": 150.0,
                "pro": 400.0,
                "enterprise": 1200.0
            },
            "clv_by_acquisition_channel": {
                "organic": 250.0,
                "paid_search": 180.0,
                "social_media": 160.0,
                "referrals": 300.0
            },
            "clv_trends": {
                "increasing": True,
                "growth_rate": 0.15,
                "drivers": ["Better onboarding", "Improved product features", "Customer success program"]
            },
            "optimization_opportunities": [
                "Improve onboarding to increase early CLV",
                "Focus on high-CLV acquisition channels",
                "Implement upselling strategies",
                "Reduce churn in high-value segments"
            ]
        }


class AnalyticsAgent:
    """
    Master agent for analytics and business intelligence.
    
    This agent coordinates revenue analytics, user analytics, technical
    analytics, and business intelligence to provide comprehensive insights.
    """
    
    def __init__(self):
        """Initialize with specialized sub-agents"""
        self.revenue_analytics = RevenueAnalyticsAgent()
        self.user_analytics = UserAnalyticsAgent()
        self.technical_analytics = TechnicalAnalyticsAgent()
        self.business_intelligence = BusinessIntelligenceAgent()
    
    async def initialize_project_metrics(self, project: Any) -> Dict[str, Any]:
        """Initialize metrics tracking for a new project"""
        await asyncio.sleep(0.3)  # Simulate initialization
        
        return {
            "project_id": project.id,
            "metrics_initialized": True,
            "tracking_enabled": {
                "revenue": True,
                "users": True,
                "technical": True,
                "business": True
            },
            "dashboard_created": True,
            "alerts_configured": True,
            "baseline_metrics": {
                "mrr": 0.0,
                "customers": 0,
                "mau": 0,
                "response_time": 0
            },
            "created_at": datetime.now().isoformat()
        }
    
    async def update_project_metrics(self, project: Any) -> Dict[str, Any]:
        """Update and return current project metrics"""
        print(f"Updating metrics for project: {project.id}")
        
        # Collect metrics from all analytics agents
        revenue_metrics = await self.revenue_analytics.track_revenue_metrics(project.id)
        user_metrics = await self.user_analytics.track_user_engagement(project.id)
        technical_metrics = await self.technical_analytics.track_technical_metrics(project.id)
        business_insights = await self.business_intelligence.generate_business_insights(project.id)
        
        # Combine all metrics
        combined_metrics = {
            "project_id": project.id,
            "timestamp": datetime.now().isoformat(),
            "revenue": revenue_metrics,
            "users": user_metrics,
            "technical": technical_metrics,
            "business": business_insights,
            "overall_health_score": self._calculate_overall_health_score(
                revenue_metrics, user_metrics, technical_metrics
            )
        }
        
        return combined_metrics
    
    async def get_factory_revenue_metrics(self) -> Dict[str, Any]:
        """Get revenue metrics for the entire software factory"""
        await asyncio.sleep(0.4)  # Simulate factory-wide analysis
        
        return {
            "total_mrr": 45000.0,
            "total_arr": 540000.0,
            "total_projects": 5,
            "active_projects": 4,
            "revenue_by_project": {
                "proj_123": {"mrr": 12500, "name": "AI Finance Assistant"},
                "proj_124": {"mrr": 18000, "name": "Fitness Tracker"},
                "proj_125": {"mrr": 8500, "name": "Job Search Assistant"},
                "proj_126": {"mrr": 6000, "name": "Sales CRM"}
            },
            "growth_metrics": {
                "monthly_growth_rate": 0.18,
                "new_projects_this_month": 1,
                "projects_launched_this_month": 1
            },
            "profitability": {
                "gross_margin": 0.82,
                "operating_margin": 0.35,
                "net_margin": 0.28
            }
        }
    
    async def create_executive_dashboard(self, project_id: str) -> Dict[str, Any]:
        """Create executive-level dashboard with key metrics"""
        await asyncio.sleep(0.5)  # Simulate dashboard creation
        
        # Get all metrics
        metrics = await self.update_project_metrics(type('Project', (), {'id': project_id})())
        
        return {
            "project_id": project_id,
            "dashboard_type": "executive",
            "key_metrics": {
                "mrr": metrics["revenue"]["mrr"]["current"],
                "growth_rate": metrics["revenue"]["mrr"]["growth_rate"],
                "customers": metrics["revenue"]["customer_metrics"]["total_customers"],
                "churn_rate": metrics["revenue"]["customer_metrics"]["churn_rate"],
                "ltv_cac_ratio": metrics["revenue"]["financial_health"]["ltv_cac_ratio"],
                "mau": metrics["users"]["monthly_active_users"]["current"],
                "uptime": metrics["technical"]["performance"]["uptime"]
            },
            "trends": {
                "revenue_trend": "Growing",
                "customer_trend": "Growing",
                "engagement_trend": "Stable",
                "technical_trend": "Improving"
            },
            "alerts": self._generate_executive_alerts(metrics),
            "recommendations": self._generate_executive_recommendations(metrics),
            "created_at": datetime.now().isoformat()
        }
    
    async def generate_analytics_report(self, project_id: str, period: str = "monthly") -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        await asyncio.sleep(0.6)  # Simulate report generation
        
        # Get all analytics data
        revenue_trends = await self.revenue_analytics.analyze_revenue_trends(project_id)
        user_retention = await self.user_analytics.analyze_user_retention(project_id)
        system_health = await self.technical_analytics.analyze_system_health(project_id)
        clv_analysis = await self.business_intelligence.analyze_customer_lifetime_value(project_id)
        
        return {
            "project_id": project_id,
            "report_period": period,
            "generated_at": datetime.now().isoformat(),
            "executive_summary": self._generate_executive_summary(
                revenue_trends, user_retention, system_health, clv_analysis
            ),
            "revenue_analysis": revenue_trends,
            "user_analysis": user_retention,
            "technical_analysis": system_health,
            "business_analysis": clv_analysis,
            "key_insights": self._extract_key_insights(
                revenue_trends, user_retention, system_health, clv_analysis
            ),
            "action_items": self._generate_action_items(
                revenue_trends, user_retention, system_health, clv_analysis
            )
        }
    
    def _calculate_overall_health_score(
        self, 
        revenue_metrics: Dict, 
        user_metrics: Dict, 
        technical_metrics: Dict
    ) -> float:
        """Calculate overall health score for the project"""
        
        # Revenue health (40% weight)
        revenue_score = 8.0  # Base score
        if revenue_metrics["mrr"]["growth_rate"] > 0.10:
            revenue_score += 1.0
        if revenue_metrics["financial_health"]["ltv_cac_ratio"] > 3.0:
            revenue_score += 0.5
        
        # User health (30% weight)
        user_score = 7.5  # Base score
        if user_metrics["daily_active_users"]["growth_rate"] > 0.05:
            user_score += 0.5
        if user_metrics["engagement_metrics"]["average_session_duration"] > 10:
            user_score += 0.5
        
        # Technical health (30% weight)
        technical_score = 8.0  # Base score
        if technical_metrics["performance"]["uptime"] > 0.99:
            technical_score += 1.0
        if technical_metrics["performance"]["error_rate"] < 0.01:
            technical_score += 0.5
        
        # Weighted average
        overall_score = (
            revenue_score * 0.40 +
            user_score * 0.30 +
            technical_score * 0.30
        )
        
        return round(overall_score, 1)
    
    def _generate_executive_alerts(self, metrics: Dict) -> List[Dict[str, Any]]:
        """Generate executive-level alerts"""
        alerts = []
        
        # Revenue alerts
        if metrics["revenue"]["mrr"]["growth_rate"] < 0.05:
            alerts.append({
                "type": "warning",
                "category": "revenue",
                "message": "MRR growth rate below target",
                "action": "Review marketing strategy and customer acquisition"
            })
        
        # User alerts
        if metrics["users"]["daily_active_users"]["growth_rate"] < 0:
            alerts.append({
                "type": "critical",
                "category": "users",
                "message": "Daily active users declining",
                "action": "Investigate user engagement and retention"
            })
        
        # Technical alerts
        if metrics["technical"]["performance"]["uptime"] < 0.99:
            alerts.append({
                "type": "critical",
                "category": "technical",
                "message": "System uptime below SLA",
                "action": "Immediate technical review required"
            })
        
        return alerts
    
    def _generate_executive_recommendations(self, metrics: Dict) -> List[str]:
        """Generate executive recommendations"""
        recommendations = []
        
        # Revenue recommendations
        if metrics["revenue"]["financial_health"]["ltv_cac_ratio"] < 3.0:
            recommendations.append("Focus on improving customer lifetime value or reducing acquisition costs")
        
        # User recommendations
        if metrics["users"]["engagement_metrics"]["bounce_rate"] > 0.5:
            recommendations.append("Improve user onboarding and first-time user experience")
        
        # Technical recommendations
        if metrics["technical"]["performance"]["average_response_time"] > 1000:
            recommendations.append("Optimize system performance to improve user experience")
        
        return recommendations
    
    def _generate_executive_summary(
        self, 
        revenue_trends: Dict, 
        user_retention: Dict, 
        system_health: Dict, 
        clv_analysis: Dict
    ) -> str:
        """Generate executive summary"""
        return f"""
        The project shows strong performance with {revenue_trends['mrr_trend'][-1]['mrr']:,.0f} MRR 
        and {revenue_trends['mrr_trend'][-1]['growth']:.1%} monthly growth. User retention is healthy 
        at {user_retention['cohort_analysis']['week_4_retention']:.1%} after 4 weeks, and system 
        health is excellent with a {system_health['overall_health_score']}/10 score. 
        Customer lifetime value is trending upward at {clv_analysis['clv_trends']['growth_rate']:.1%} growth.
        """
    
    def _extract_key_insights(
        self, 
        revenue_trends: Dict, 
        user_retention: Dict, 
        system_health: Dict, 
        clv_analysis: Dict
    ) -> List[str]:
        """Extract key insights from all analytics"""
        insights = []
        
        # Revenue insights
        latest_growth = revenue_trends['mrr_trend'][-1]['growth']
        if latest_growth > 0.15:
            insights.append(f"Strong MRR growth of {latest_growth:.1%} indicates healthy business momentum")
        
        # User insights
        week_4_retention = user_retention['cohort_analysis']['week_4_retention']
        if week_4_retention > 0.4:
            insights.append(f"Good user retention at {week_4_retention:.1%} after 4 weeks")
        
        # Technical insights
        health_score = system_health['overall_health_score']
        if health_score > 8.0:
            insights.append(f"Excellent system health score of {health_score}/10")
        
        # CLV insights
        clv_growth = clv_analysis['clv_trends']['growth_rate']
        if clv_growth > 0.1:
            insights.append(f"Customer lifetime value growing at {clv_growth:.1%}")
        
        return insights
    
    def _generate_action_items(
        self, 
        revenue_trends: Dict, 
        user_retention: Dict, 
        system_health: Dict, 
        clv_analysis: Dict
    ) -> List[Dict[str, Any]]:
        """Generate actionable items based on analytics"""
        action_items = []
        
        # Revenue actions
        if revenue_trends['mrr_trend'][-1]['growth'] < 0.1:
            action_items.append({
                "priority": "high",
                "category": "revenue",
                "action": "Review and optimize customer acquisition strategy",
                "owner": "marketing_team",
                "due_date": "2024-02-15"
            })
        
        # User actions
        if user_retention['cohort_analysis']['week_1_retention'] < 0.7:
            action_items.append({
                "priority": "high",
                "category": "users",
                "action": "Improve onboarding experience",
                "owner": "product_team",
                "due_date": "2024-02-01"
            })
        
        # Technical actions
        if system_health['overall_health_score'] < 8.0:
            action_items.append({
                "priority": "medium",
                "category": "technical",
                "action": "Address system performance issues",
                "owner": "engineering_team",
                "due_date": "2024-02-10"
            })
        
        return action_items


# Example usage and testing
async def main():
    """Example usage of the Analytics Agent"""
    agent = AnalyticsAgent()
    
    # Mock project
    class MockProject:
        def __init__(self):
            self.id = "proj_123"
            self.name = "AI Finance Assistant"
    
    project = MockProject()
    
    # Initialize metrics
    initial_metrics = await agent.initialize_project_metrics(project)
    print(f"Metrics initialized: {initial_metrics['metrics_initialized']}")
    
    # Update metrics
    current_metrics = await agent.update_project_metrics(project)
    print(f"Current MRR: ${current_metrics['revenue']['mrr']['current']:,.0f}")
    print(f"Overall health score: {current_metrics['overall_health_score']}/10")
    
    # Create executive dashboard
    dashboard = await agent.create_executive_dashboard(project.id)
    print(f"Dashboard created with {len(dashboard['key_metrics'])} key metrics")
    
    # Generate analytics report
    report = await agent.generate_analytics_report(project.id)
    print(f"Analytics report generated with {len(report['key_insights'])} insights")


if __name__ == "__main__":
    asyncio.run(main())

