# 🛡️ AI SOC Analyst: Intelligent Security Monitoring System

This project is an **AI-powered Security Operations Center (SOC) Agent** that monitors server logs (`server_logs.txt`) in real-time. It doesn't just look for keywords; it acts like a **Senior Security Analyst** to evaluate suspicious activities and take autonomous actions.

By leveraging **Llama 3.3 (via Groq)** and **LangGraph**, the system analyzes the logic behind attacks such as SQL Injection (SQLi), Cross-Site Scripting (XSS), Brute Force, and Directory Traversal.


---

### System Execution & Logic Flow

Below is the end-to-end execution flow of the agent. The LangSmith traces demonstrate the internal decision-making logic for both benign and malicious scenarios.

|  1. Benign Analysis |  2. Malicious Analysis |  3. Server/DB Logs |  4. Threat Alert |
| :---: | :---: | :---: | :---: |
| **Safe Path** | **Threat Path** | **Input Source** | **Response Output** |
| ![](images/images-2.png) | ![](images/images-3.png) | ![](images/image-4.png) | ![](images/images-1.jpeg) |
| *LangSmith trace showing immediate termination for safe logs.* | *LangSmith trace showing research and tool execution.* | *MySQL Database view of recorded security incidents.* | *Instant notification sent to the admin via Telegram.* |

---

## ✨ Key Features

* **🔍 Intelligent Analysis:** Uses Llama 3.3 to understand the intent and severity of log entries.
* **🌐 Live Threat Intelligence:** Automatically researches suspicious IPs and payloads using **Tavily Search**.
* **🚨 Multi-Channel Response:**
    * Sends instant alerts to the administrator via **Telegram** for confirmed threats.
    * Logs all incident details and AI-generated summaries into **MySQL**.
* **🔄 Advanced Decision Logic:** Managed by a **LangGraph** state machine to ensure a reliable and traceable analysis flow.

📋 How It Works
Ingestion: The agent monitors server_logs.txt for new entries.

Reasoning: The AI analyst evaluates the log. If it's safe (Benign), the process ends.

Investigation: If suspicious, the agent triggers a search for the IP reputation or payload signatures using Tavily.

Decision & Action: If a threat is confirmed, it executes two parallel actions: sends a Telegram alert and writes to the MySQL database.

## 🛠️ Tech Stack

* **Frameworks:** LangChain & LangGraph
* **LLM:** Groq (Llama-3.3-70b-versatile)
* **Data & Tools:** MySQL, Telegram Bot API, Tavily Search API
* **Language:** Python 3.x
