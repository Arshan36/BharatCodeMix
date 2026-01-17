# BharatCodeMix: Demo Video Script (5-8 Minutes)

**Intro (0:00 - 1:00)**
*   **Visual**: Show yourself (webcam) or the Title Slide.
*   **Audio**: "Hello everyone, welcome to the demonstration of **BharatCodeMix**, a dialect and code-mixed translation system designed for Indian languages. My name is [Name], and today I'll show you how we are solving the problem of 'Hinglish' translation."
*   **Problem**: "We all know standard translators fail when we mix Hindi and English, or use slang like 'bindass'. Our goal was to build a privacy-first, local tool to handle this."

**System Overview (1:00 - 2:00)**
*   **Visual**: Show the Architecture Slide (Slide 4).
*   **Audio**: "Before we jump into the demo, here is how it works. We don't just send text to a model. We first pass it through a **Normalization Layer**. This detects if you are using Latin script for Hindi, fixes spelling, detects slang, and converts it to Devanagari. Only THEN does it go to the Neural Network. This ensures high accuracy."

**The Demo - Core Features (2:00 - 5:00)**
*   **Visual**: Switch to Screen Share. Show the VS Code terminal or the Gradio Web Interface running.
*   **Action 1 (Hinglish)**:
    *   Type: "Kya haal hai bro?"
    *   Result: "How are you bro?" (or similar)
    *   **Commentary**: "Notice how I typed in English script, but it understood it was Hindi and gave the English translation."
*   **Action 2 (Slang)**:
    *   Type: "Yeh movie bahot bindass hai."
    *   Result: "This movie is very carefree/cool."
    *   **Commentary**: "Here, 'bindass' is a slang word. Google Translate might struggle, but our system maps it effectively."
*   **Action 3 (Reverse)**:
    *   Type: "Where are you going?"
    *   Result: "Tum kahan ja rahe ho?"
    *   **Commentary**: "It works both ways, English to Hindi."
*   **Action 4 (Confidence)**:
    *   Show the 'Confidence Score' in the output JSON or UI.
    *   **Commentary**: "We also provide a confidence score so the user knows if the translation is reliable."

**Code Walkthrough (5:00 - 6:30)**
*   **Visual**: Open `BharatCodeMix_Submission.ipynb` in VS Code/Jupyter.
*   **Audio**: "The entire project is documented in this Jupyter Notebook. It serves as our source of truth."
*   **Scroll**: Scroll through the sections briefly. "We have the Data Preparation, the Pipeline logic, and our Evaluation metrics all executable right here."

**Result & Conclusion (6:30 - End)**
*   **Visual**: Back to Slides (Conclusion Slide).
*   **Audio**: "In conclusion, BharatCodeMix proves that with the right pre-processing, we can make AI tools much more accessible to vernacular users. It runs locally, respects privacy, and understands how India actually speaks. Thank you!"

---
**Tips for Recording**:
*   Use Zoom to record screen + webcam.
*   Ensure the text font is large enough to read.
*   Speak clearly and relatively slowly.
