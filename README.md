🚀 Overview

This project is a multi-agent research system powered entirely by LLMs. It performs end-to-end automated research—from web search to report generation—by coordinating multiple specialized LLM agents.
The system retrieves real online data, validates every answer against retrieved evidence, and outputs a fully grounded research report with 0% hallucinations.

🔍 Key Features
1. Automated Web Research

LLM agent formulates optimized search queries

Fetches real web pages, PDFs, and articles

Runs ingestion + text extraction using scrapers and PDF parsers

2. Intelligent Chunking & Vector Retrieval

Splits documents into meaningful chunks

Embeds them using high-quality embedding models

Stores vectors in pgvector

Retrieves the most relevant evidence for answering the query

3. Strict No-Hallucination RAG

A specialized LLM-based validator agent cross-checks every generated answer.

Rejects any content not present in retrieved chunks

Ensures 100% grounded, verifiable answers

Guarantees 0% hallucination RAG workflow

4. Multi-Agent Architecture

The system uses LLMs as coordinated agents performing different roles:

Agent Role	Responsibility
Query Optimizer	Improves user question for better web search
Web Ingestion Agent	Fetches and cleans online data
Chunker + Embedder	Splits, embeds, and stores chunks in pgvector
RAG Generator	Creates answer grounded in retrieved data
Validator	Checks if the answer exists in evidence
Graph Summarizer	Converts retrieved data into structured insights
Report Writer	Produces a final polished research report

This demonstrates LLMs as a full autonomous pipeline, not just a single chat interface.

🧠 Why This Project Matters

Traditional RAG systems often hallucinate. This project solves that using:

Strict validator agent

Evidence-only answer enforcement

Multi-step reasoning across RAG stages

It showcases how LLMs can collaborate as a research team—searching, verifying, and reporting like human analysts.

🏗️ Tech Stack

Python

LLMs (OpenAI / Groq / Anthropic compatible)

pgvector + PostgreSQL

BeautifulSoup / Playwright / PDF extraction tools

Custom multi-agent controller

📁 Project Flow Diagram

User Query

Query Optimization

Web Search

URL Fetch + PDF/Text Extraction

Chunking & Embedding

pgvector Retrieval

LLM-based RAG Answer Generation

Validator Agent Approval

Final Research Report
