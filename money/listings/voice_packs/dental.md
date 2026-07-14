# I will set up an AI voice agent that answers dental-practice calls 24/7

**Price:** $1500/gig
**Margin:** —%
**Tags:** ai voice agent, dental automation, appointment booking, healthcare ai, virtual receptionist, n8n, hipaa friendly self-host

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- **Basic** ($375, 3 days): Single-line agent; 1 script; Email support
- **Standard** ($1500, 5 days): Full voice agent; Booking/CRM hook; Loom walkthrough; 7-day support
- **Premium** ($3000, 7 days): Multi-line + escalation; Unlimited scripts; Monthly retainer option; Priority support

## Why this works
- Self-hosted stack (n8n + free tools) → 90–99% profit margin
- Every deliverable is generated and delivered automatically
- You own the system; scale to unlimited clients

## FAQ
**Q: Do I need to pay for software?**
A: No. Everything runs on free open-source tools (n8n, Chatwoot, Stirling-PDF, Listmonk).

**Q: Is this a one-time build or ongoing?**
A: Both. One-time setup + optional monthly retainer for monitoring/optimization.

**Q: Can you customize for my niche?**
A: Yes — every package is generated from a template and tuned to your vertical.

## Technical spec (for the build)
```json
{
 "name": "deliver-voice-agent-dental",
 "nodes": [
  {
   "parameters": {},
   "name": "Twilio/Webhook (inbound call)",
   "type": "n8n-nodes-base.webhook",
   "typeVersion": 1,
   "position": [
    0,
    0
   ]
  },
  {
   "parameters": {},
   "name": "Whisper STT + Hermes agent",
   "type": "n8n-nodes-base.code",
   "typeVersion": 1,
   "position": [
    300,
    0
   ]
  },
  {
   "parameters": {},
   "name": "Piper TTS + Chatwoot handoff",
   "type": "n8n-nodes-base.code",
   "typeVersion": 1,
   "position": [
    600,
    0
   ]
  }
 ],
 "connections": {
  "Twilio/Webhook (inbound call)": {
   "main": [
    [
     {
      "node": "Whisper STT + Hermes agent",
      "type": "main",
      "index": 0
     }
    ]
   ]
  },
  "Whisper STT + Hermes agent": {
   "main": [
    [
     {
      "node": "Piper TTS + Chatwoot handoff",
      "type": "main",
      "index": 0
     }
    ]
   ]
  }
 },
 "note": "Tools: Piper + Whisper + Hermes/OpenClaw + Chatwoot + n8n \u2014 all free/self-hosted. Replace code nodes with your STT/LLM/TTS logic."
}
```
