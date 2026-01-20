# Week 3: Production AI Systems

This week focuses on building production-grade AI systems with advanced agent orchestration, security analysis, and real-world deployments.

## 📚 Projects

### Day 1: AI-Powered Cybersecurity Code Analyzer

**[View Project →](day-1/cyber/)**

An intelligent security analysis tool that combines static analysis (Semgrep) with AI-powered deep analysis using **Ollama's Gemma3 27B** instead of OpenAI's API.

**Key Features:**
- 🤖 AI-powered security analysis with Gemma3 27B via Ollama
- 🔍 Integrated Semgrep static analysis
- 🌉 Custom OpenAI ↔ Ollama translation proxy
- 🎯 CVSS scoring and severity classification
- 📊 Comprehensive vulnerability reporting

**Tech Stack:**
- **Frontend**: Next.js 15.5.9, React, Tailwind CSS
- **Backend**: FastAPI, OpenAI Agents SDK, MCP Protocol
- **AI**: Ollama, Gemma3 27B (Google's open-source model)
- **Translation Layer**: Custom Python proxy (`ollama_proxy.py`)

**Highlights:**
- ✅ **No OpenAI API costs** - Uses self-hosted Gemma3 27B
- ✅ **Advanced tool integration** - Semgrep via Model Context Protocol
- ✅ **Production-ready** - Full error handling and logging
- ✅ **Comprehensive docs** - Architecture diagrams and setup guides

**Reference:** Based on [Week 3 Day 1 Part 0](https://github.com/ed-donner/production/blob/main/week3/day1_part0.md) with Ollama integration.

---

## 🎯 Learning Objectives

- **Agent Orchestration**: Using OpenAI Agents SDK for complex workflows
- **MCP Integration**: Model Context Protocol for tool integration
- **API Translation**: Building compatibility layers between different AI services
- **Security Analysis**: Combining static and AI-powered code analysis
- **Production Deployment**: Running AI systems with custom infrastructure

## 🚀 Getting Started

Each project has its own detailed README with setup instructions. Navigate to the project directory and follow the specific guides.

## 📖 Course Reference

Projects are based on the [AI Engineering Production Course](https://github.com/ed-donner/production) curriculum with modifications for Ollama integration and self-hosted AI models.

---

**Status**: Week 3 Day 1 Complete ✅
