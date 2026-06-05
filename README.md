# iQ-Online-Unit2-Study

Study application for iQ Online Unit 2 vocabulary

🚀 **[Open Application](https://iqonline2study.streamlit.app/)** - Click here to start studying!

## Overview

This is a Streamlit-based TOEIC Vocabulary Trainer application that helps users study Unit 2 vocabulary through interactive quizzes and scanning exercises.

## Features

### Q1: Meaning (意味問題)
- Multiple choice questions to identify the correct meaning of vocabulary words
- 4 randomly selected options including the correct answer

### Q2: Synonyms (類語問題)
- Checkbox-based synonym selection exercise
- Users must select all correct synonyms for a word
- Random distractor options from the vocabulary pool

### Q3: Scanning (スキャニング)
- Timed speed-reading exercise
- Users find a target synonym within a passage
- Tracks and displays completion time
- Real-time timer display

## Results Dashboard

After completing exercises, view your performance metrics:
- **Q1 & Q2 Accuracy**: Overall correct answer statistics
- **Scanning Times**: Individual and average completion times
- **Rating System**: Achievements based on accuracy and scanning speed
  - 👑 TOEIC Level 990: < 3 sec average, ≥ 90% accuracy
  - ⚡ TOEIC Level 900: < 4 sec average, ≥ 80% accuracy
  - 🔥 TOEIC Level 800: < 6 sec average
  - 📚 TOEIC Level 700: < 7 sec average
  - 🌱 Keep Practicing: > 7 sec average

## How to Use

1. Select a word from the sidebar
2. Answer Q1 (meaning question)
3. Select synonyms for Q2
4. Start and complete the Q3 scanning exercise
5. Click "この回答でOK" to save your answers
6. View results by clicking "結果を見る" in the sidebar

## Files

- `app.py` - Main Streamlit application
- `data.py` - Vocabulary data and choices

## Requirements

- Streamlit
- streamlit-javascript
- Python 3.x
