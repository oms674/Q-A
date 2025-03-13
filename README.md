
---

##  Agent Architecture Overview
This project follows an **Agent-Based Design** to ensure modularity and flexibility:

### **Transcription Agent**
- Captures **audio input** via WebSocket.
- Uses **OpenAI's Realtime API** to convert speech to text.
- Ensures accurate transcription with noise handling.

###  **Search Agent**
- Identifies query intent:
   - For general queries, it leverages **Serper API** to fetch reliable Google search results.
- Formats clickable links for improved user experience.

###  **Display Agent**
- Processes and formats data for clear presentation.
- Ensures text results are concise and informative.
- Displays both answers (if available) and clickable links for additional details.

---

##  Frontend Architecture
The frontend is designed for an intuitive and seamless experience:

### **HTML (index.html)**
- Provides a **clean UI** with a “Start Recording” button for audio capture.
- Displays search results with **clickable links**.

### **CSS (style.css)**
- Ensures a **modern layout** with responsive design for optimal user experience.

### **JavaScript (script.js)**
- Manages **WebSocket connections** for real-time interaction.
- Sends audio data to the backend and dynamically updates results on the page.


### Agents follow a modular design, Agents are built using a custom class-based structure with FastAPI for interaction. 

   # Transcription Agent
      Captures audio data via WebSocket.
      Uses the Whisper API for transcription.

   # Search Agent
      Determines if the query is related to Sena.
      Uses Serper API for web search or scrapes https://sena.services/.

   # Display Agent
      Formats and presents the search results in a user-friendly format.

---
