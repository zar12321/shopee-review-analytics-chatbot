# Shopee Review Analysis Chatbot

## Overview

Shopee Review Analysis Chatbot is a Retrieval-Augmented Generation (RAG) application designed to analyze user reviews of the Shopee mobile application collected from Google Play Store. The chatbot enables users to explore customer feedback through natural language queries and provides insights based on review retrieval, sentiment analysis, and statistical analysis.

The system leverages Large Language Models (LLMs), vector databases, and semantic search techniques to deliver context-aware answers grounded in real user reviews.

---

## Features

* Review Retrieval using semantic search
* Sentiment Analysis of user reviews
* Statistical Analysis of review data
* Natural Language Question Answering
* Retrieval-Augmented Generation (RAG) architecture
* Interactive chatbot interface built with Streamlit

---

## Dataset

The dataset consists of user reviews collected from the Shopee application page on Google Play Store using Google Play Scraper.

Data attributes include:

* Review ID
* Username
* Review Text
* Rating
* Review Date
* Developer Reply
* Reply Date

---

## System Architecture

Google Play Reviews

↓

PostgreSQL Database

↓

Document Processing

↓

Embedding Generation

↓

FAISS Vector Database

↓

Retriever

↓

Gemini LLM

↓

Streamlit Chatbot

---

## Technologies Used

* Python
* LangChain
* LangGraph
* FAISS
* PostgreSQL
* Google Play Scraper
* Google Gemini
* Streamlit

---

## Project Structure

```text
project/
│
├── data_pipeline/
│   └── database.py
│
├── rag/
│   ├── documents.py
│   ├── embeddings.py
│   ├── retriever.py
│
├── agent/
│   ├── nodes.py
│   ├── router.py
│   └── state.py
│
├── streamlit_app.py
├── ingest.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
```

Build the vector database:

```bash
python ingest.py
```

Run the application:

```bash
streamlit run streamlit_app.py
```

---

## Usage Examples

Example questions:

* What are the most common user complaints?
* How is the sentiment distribution of Shopee reviews?
* What features do users appreciate the most?
* Summarize recent negative reviews.
* What are the main issues mentioned by users regarding payment services?

---

## Notes

The chatbot is specifically designed to analyze Shopee user reviews from Google Play Store. Responses outside the review-analysis domain may be limited.

---

## Author

Developed as a Retrieval-Augmented Generation (RAG) project for review analytics and conversational intelligence.
