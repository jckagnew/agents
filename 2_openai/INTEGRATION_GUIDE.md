# 🔧 Integration Guide: Enhanced Structured Outputs for Lab 3

## 🎯 What This Guide Does

This guide will help you integrate all the enhanced structured outputs we created into your existing `3_lab3.ipynb` notebook, step by step.

## 📋 Step-by-Step Integration

### Step 1: Update the Pydantic Models (Cell 1)

**Replace your existing models with these enhanced versions:**

```python
# Enhanced structured output models for email generation
class EmailSubject(BaseModel):
    """Enhanced structured output for email subject generation"""
    subject: str = Field(..., description="A compelling email subject line that will increase open rates")
    reasoning: str = Field(..., description="Brief explanation of why this subject line is effective")
    tone: str = Field(..., description="The tone of the subject line (professional, casual, urgent, etc.)")
    urgency_level: str = Field(..., description="How urgent the subject line conveys (low, medium, high)")
    a_b_test_variants: list[str] = Field(..., description="Alternative subject lines for A/B testing")
    compliance_check: bool = Field(..., description="Whether the subject line complies with email best practices")

class HTMLEmailBody(BaseModel):
    """Enhanced structured output for HTML email body conversion"""
    html_body: str = Field(..., description="Complete HTML email body with proper formatting and styling")
    text_version: str = Field(..., description="Plain text fallback version of the email")
    styling_notes: str = Field(..., description="Notes about the styling and layout choices made")
    responsive_design: bool = Field(..., description="Whether the HTML is mobile-responsive")

class EmailSendResult(BaseModel):
    """Enhanced structured output for email sending results"""
    status: str = Field(..., description="Success or failure status of the email send")
    message_id: str = Field(..., description="SendGrid message ID if successful")
    error_details: str = Field(default="", description="Error details if the send failed")
    recipient: str = Field(..., description="Email address the email was sent to")
    timestamp: str = Field(..., description="When the email was sent")
    delivery_status: str = Field(..., description="Current delivery status")
    bounce_status: str = Field(default="", description="Bounce status if applicable")
    spam_score: float = Field(default=0.0, description="Spam score (0-100, lower is better)")

class SalesEmail(BaseModel):
    """Enhanced structured output for sales email generation"""
    subject: str = Field(..., description="Compelling subject line for the cold sales email")
    body: str = Field(..., description="Professional cold sales email body")
    tone: str = Field(..., description="The tone used in the email (professional, casual, urgent, etc.)")
    target_role: str = Field(..., description="The target role this email is designed for")
    call_to_action: str = Field(..., description="Clear call to action for the recipient")
    follow_up_strategy: str = Field(..., description="Suggested follow-up strategy")
    pain_points_addressed: list[str] = Field(..., description="List of pain points this email addresses")
    value_proposition: str = Field(..., description="Clear value proposition for the recipient")
    personalization_opportunities: list[str] = Field(..., description="Areas where personalization could be added")
    compliance_notes: str = Field(..., description="Notes about regulatory compliance considerations")

class EmailAnalysis(BaseModel):
    """New structured output for email analysis and optimization"""
    open_rate_prediction: float = Field(..., description="Predicted open rate (0-100%)")
    response_rate_prediction: float = Field(..., description="Predicted response rate (0-100%)")
    strengths: list[str] = Field(..., description="List of email strengths")
    areas_for_improvement: list[str] = Field(..., description="Areas that could be improved")
    a_b_test_suggestions: list[str] = Field(..., description="A/B testing suggestions")
    compliance_score: float = Field(..., description="Compliance score (0-100%)")
    personalization_score: float = Field(..., description="Personalization effectiveness score (0-100%)")
```

### Step 2: Update Sales Agent Instructions (Cell 4)

**Add structured output requirements to your instructions:**

```python
instructions1 = "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails. Always structure your response according to the SalesEmail schema."

instructions2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response. Always structure your response according to the SalesEmail schema."

instructions3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails. Always structure your response according to the SalesEmail schema."
```

### Step 3: Update Sales Agents (Cell 8)

**Add structured outputs to your sales agents:**

```python
# Create sales agents with structured outputs for consistent email generation
sales_agent1 = Agent(
    name="DeepSeek Sales Agent", 
    instructions=instructions1, 
    model=deepseek_model,
    output_type=SalesEmail  # ← Enhanced structured output!
)
sales_agent2 = Agent(
    name="Gemini Sales Agent", 
    instructions=instructions2, 
    model=gemini_model,
    output_type=SalesEmail  # ← Enhanced structured output!
)
sales_agent3 = Agent(
    name="Llama3.3 Sales Agent",
    instructions=instructions3,
    model=llama3_3_model,
    output_type=SalesEmail  # ← Enhanced structured output!
)
```

### Step 4: Update Email Sending Function (Cell 10)

**Enhance your email function with structured output:**

```python
@function_tool
def send_html_email(subject: str, html_body: str, recipient: str = "john_d_agnew@yahoo.com") -> EmailSendResult:
    """Send out an email with the given subject and HTML body to the specified recipient"""
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("jack@clevelsalesguy.com")
        to_email = To(recipient)
        content = Content("text/html", html_body)
        mail = Mail(from_email, to_email, subject, content).get()
        response = sg.client.mail.send.post(request_body=mail)
        
        return EmailSendResult(
            status="success",
            message_id=response.headers.get('X-Message-Id', 'unknown'),
            recipient=recipient,
            timestamp=response.headers.get('Date', 'unknown'),
            delivery_status="sent"
        )
    except Exception as e:
        return EmailSendResult(
            status="failed",
            message_id="",
            error_details=str(e),
            recipient=recipient,
            timestamp="",
            delivery_status="failed"
        )
```

### Step 5: Update Email Tools (Cell 11)

**Add structured outputs to your email tools:**

```python
subject_instructions = "You can write a subject for a cold sales email. \
You are given a message and you need to write a subject for an email that is likely to get a response. \
Always structure your response according to the EmailSubject schema."

html_instructions = "You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design. \
Always structure your response according to the HTMLEmailBody schema."

# Create agents with structured outputs
subject_writer = Agent(
    name="Email subject writer", 
    instructions=subject_instructions, 
    model="gpt-4o-mini",
    output_type=EmailSubject  # ← Enhanced structured output!
)
subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold sales email")

html_converter = Agent(
    name="HTML email body converter", 
    instructions=html_instructions, 
    model="gpt-4o-mini",
    output_type=HTMLEmailBody  # ← Enhanced structured output!
)
html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")
```

### Step 6: Add Email Analysis Agent (NEW CELL)

**Add this new cell after your existing email tools:**

```python
# NEW: Email analysis agent with structured output
analysis_instructions = "You are an email optimization expert. \
Analyze the given email and provide insights on how to improve open rates and response rates. \
Always structure your response according to the EmailAnalysis schema."

email_analyzer = Agent(
    name="Email Analyzer",
    instructions=analysis_instructions,
    model="gpt-4o-mini",
    output_type=EmailAnalysis  # ← NEW structured output!
)

analyzer_tool = email_analyzer.as_tool(tool_name="email_analyzer", tool_description="Analyze and optimize email performance")

print("✅ NEW: Email analyzer agent created with structured output!")
```

### Step 7: Update Tools List (Cell 12)

**Add the analyzer tool to your tools:**

```python
tools = [tool1, tool2, tool3, analyzer_tool]  # ← Added analyzer tool!
handoffs = [emailer_agent]

print(f"🛠️  Total tools available: {len(tools)} (including new email analyzer!)")
```

### Step 8: Update Sales Manager Instructions (Cell 15)

**Add email analysis capability to your sales manager:**

```python
sales_manager_instructions = """You are a sales manager working for ComplAI. You use the tools given to you to generate cold sales emails. 
You never generate sales emails yourself; you always use the tools. 
You try all 3 sales agent tools at least once before choosing the best one. 
You can use the tools multiple times if you're not satisfied with the results from the first try. 
You select the single best email using your own judgement of which email will be most effective. 
After picking the email, you handoff to the Email Manager agent to format and send the email.
You can also use the email_analyzer tool to get insights on email performance."""
```

### Step 9: Update Guardrail (Cell 17)

**Enhance your guardrail with structured output:**

```python
class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str
    risk_level: str = Field(..., description="Risk level: low, medium, high")  # ← Enhanced!

guardrail_agent = Agent( 
    name="Name check",
    instructions="Check if the user is including someone's personal name in what they want you to do.",
    output_type=NameCheckOutput,  # ← Enhanced structured output!
    model="gpt-4o-mini"
)
```

### Step 10: Update Guardrail Function (Cell 18)

**Enhance your guardrail function:**

```python
@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    risk_level = result.final_output.risk_level  # ← Enhanced risk assessment!
    
    print(f"⚠️  Guardrail triggered: {risk_level} risk level")
    
    return GuardrailFunctionOutput(
        output_info={"found_name": result.final_output},
        tripwire_triggered=is_name_in_message
    )
```

## 🧪 Testing Your Integration

### Test 1: Enhanced Sales Email Generation
```python
message = "Send out a cold sales email addressed to Dear CEO from our sales team"

print("🚀 Testing Enhanced Automated SDR with Structured Outputs...")
print("📊 This will now generate emails with detailed pain points, value propositions, and analysis!")

with trace("Enhanced Automated SDR"):
    result = await Runner.run(sales_manager, message)
    
print("✅ Enhanced sales email generated and sent with structured outputs!")
print("📈 You can now access detailed data like pain_points_addressed, value_proposition, etc.")
```

### Test 2: Email Analysis Capability
```python
print("🔍 Testing NEW Email Analysis with Structured Outputs...")

sample_email = """
Subject: Transform Your SOC2 Compliance Process

Hi there,

Are you struggling with SOC2 compliance audits? Our AI-powered platform can help you prepare in half the time.

Let's discuss how we can streamline your compliance process.

Best regards,
The ComplAI Team
"""

analysis_result = await Runner.run(email_analyzer, f"Analyze this email: {sample_email}")

print("📈 Email Analysis Results (Structured Output):")
print(f"   - Predicted Open Rate: {analysis_result.final_output.open_rate_prediction}%")
print(f"   - Predicted Response Rate: {analysis_result.final_output.response_rate_prediction}%")
print(f"   - Strengths: {', '.join(analysis_result.final_output.strengths)}")
print(f"   - Areas for Improvement: {', '.join(analysis_result.final_output.areas_for_improvement)}")
print(f"   - A/B Testing Suggestions: {', '.join(analysis_result.final_output.a_b_test_suggestions)}")
print(f"   - Compliance Score: {analysis_result.final_output.compliance_score}%")
print(f"   - Personalization Score: {analysis_result.final_output.personalization_score}%")

print("\n🎉 Email analysis working with structured outputs!")
```

## 🎯 What You'll Get After Integration

1. **Enhanced Data Quality** - Consistent, validated outputs across all agents
2. **Email Analysis** - Performance predictions and optimization suggestions
3. **Better Error Handling** - Detailed error tracking and delivery status
4. **Compliance Tracking** - Regulatory compliance scoring and notes
5. **A/B Testing Support** - Variant suggestions for optimization
6. **Performance Metrics** - Open rate and response rate predictions

## 🚀 Quick Integration Command

If you want to quickly test the enhanced version, you can also run:

```bash
python3 enhanced_structured_outputs.py
```

This will run the complete enhanced implementation and show you all the new capabilities in action!

## ❓ Need Help?

If you run into any issues during integration, check:
1. All imports are correct
2. Pydantic models are properly defined
3. Agent `output_type` parameters are set correctly
4. All required dependencies are installed

The enhanced structured outputs will make your Lab 3 much more powerful and professional! 🎉
