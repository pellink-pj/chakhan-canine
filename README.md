# PetLink 펫링크

A smart pet services platform that matches dog owners with trained pet sitters, powered by AI-based dog breed matching.

## Features

- 🐾 **Dog MBTI Matching** — Recommends the best dog breed based on your lifestyle using Euclidean distance scoring over `optimized_dogs_master.json`
- 🤝 **Pet Sitter Matching** — Location-based matching between dog owners and certified sitters
- 🚨 **Emergency AI Chatbot** — RAG-based first-aid guide for sitters during walks
- 🏅 **AI-Verified Profiles** — Dog temperament profiling and sitter certification

## Tech Stack

- **Frontend**: Next.js 16 (App Router), React, TypeScript, Tailwind CSS v4
- **Data**: `public/data/optimized_dogs_master.json` — 20 dog breeds with 8 trait scores (1–5)

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) and click **강아지 찾기** to take the lifestyle quiz.

## Project Structure

```
src/
  app/
    page.tsx              # Landing page
    quiz/page.tsx         # 8-question lifestyle quiz
    results/
      page.tsx            # Results page (Suspense wrapper)
      ResultsContent.tsx  # Client component — runs matching algorithm
  components/
    Header.tsx            # Sticky navigation header
    DogCard.tsx           # Dog breed result card
    SliderInput.tsx       # 1–5 slider input for quiz
  lib/
    matching.ts           # Euclidean distance matching algorithm
    quizData.ts           # Quiz question dataset
  types/
    dog.ts                # TypeScript interfaces for all data models
public/
  data/
    optimized_dogs_master.json  # 20 dog breeds with traits_score
```
