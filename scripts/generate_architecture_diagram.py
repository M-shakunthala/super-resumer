# -*- coding: utf-8 -*-
"""
Generate Architecture Diagram using ASCII art that can be converted to image
"""

def generate_architecture_diagram():
    """Generate ASCII architecture diagram."""
    
    diagram = """
╔══════════════════════════════════════════════════════════════════════╗
║                    AI JOB AGENT SYSTEM ARCHITECTURE                   ║
╚══════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │
│  │  Streamlit       │  │  Human Review    │  │  Analytics       │    │
│  │  Dashboard       │  │  Interface       │  │  Dashboard       │    │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘    │
│           │                     │                     │               │
│           └─────────────────────┴─────────────────────┘               │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          ORCHESTRATION LAYER                          │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                     Core Orchestrator                           │  │
│  │              Workflow & State Management                         │  │
│  └────────────────────────┬───────────────────────────────────────┘  │
│                           │                                            │
│         ┌─────────────────┴─────────────────┐                        │
│         ▼                                   ▼                        │
│  ┌─────────────┐                     ┌──────────────┐               │
│  │  Scheduler  │                     │ Event Manager │               │
│  └─────────────┘                     └──────────────┘               │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                            AGENT LAYER                                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐      │
│  │ AI Engine  │  │   Job      │  │   Resume   │  │   Apply    │      │
│  │            │  │  Scraper   │  │ Optimizer  │  │   Engine   │      │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘      │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                           MEMORY LAYER                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                    │
│  │  Profile    │  │    Job      │  │   Session   │                    │
│  │   Memory    │  │   Memory    │  │   Memory    │                    │
│  └─────────────┘  └─────────────┘  └─────────────┘                    │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       PLATFORM INTEGRATION                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐      │
│  │  LinkedIn  │  │  Workday   │  │ Greenhouse │  │   Lever    │      │
│  │  Handler   │  │  Handler   │  │  Handler   │  │  Handler   │      │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘      │
└────────────────────────────────────┬───────────────────────────────────┘
                                     ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       INFRASTRUCTURE LAYER                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐      │
│  │  Browser   │  │   Retry    │  │  Circuit   │  │   Logger   │      │
│  │  Manager   │  │    Logic   │  │  Breaker   │  │           │      │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘      │
└──────────────────────────────────────────────────────────────────────┘

═════════════════════════════════════════════════════════════════════════

DATA FLOW:
User Input → Dashboard → Orchestrator → Job Discovery → AI Matching 
    ↓
Resume Tailoring → Application → Platform Integration → Dashboard Update

TECHNOLOGY STACK:
• Frontend: Streamlit (Python)
• Backend: Python 3.8+
• Automation: Selenium WebDriver
• AI/ML: OpenAI GPT-4
• Database: SQLite
• Infrastructure: Docker
"""
    
    return diagram

def save_diagram_to_file():
    """Save diagram to file."""
    diagram = generate_architecture_diagram()
    
    with open("screenshots/architecture_diagram.txt", "w") as f:
        f.write(diagram)
    
    print("✅ Architecture diagram saved to screenshots/architecture_diagram.txt")
    print("\nTo convert to image:")
    print("1. Use online ASCII-to-image converters")
    print("2. Use terminal screenshot tools")
    print("3. Or use diagramming tools like Draw.io, Lucidchart")

if __name__ == "__main__":
    save_diagram_to_file()