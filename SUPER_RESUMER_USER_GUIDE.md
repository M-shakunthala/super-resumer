# 🤖 Super Resumer - Simple User Guide for Non-Technical Users

## 🎯 What is Super Resumer?

Super Resumer is an **automatic job application helper** that finds jobs for you and applies to them automatically. Think of it as a personal assistant that searches for jobs, checks if they match your skills, and applies to the good ones for you.

---

## 🚀 How to Run the Application (Step-by-Step)

### Step 1: Get Your API Key

- **What you need**: An OpenRouter API key (similar to a password for using AI features)
- **How to get it**:
  1. Go to [OpenRouter.ai](https://openrouter.ai)
  2. Sign up for a free account
  3. Go to "API Keys" section
  4. Copy your API key (it looks like a long string of random characters)

### Step 2: Prepare Your Resumes

- **What you need**: Two resume files
  1. C# Developer resume (for .NET/C# jobs)
  2. Python AI Developer resume (for Python/Machine Learning jobs)
- **File formats**: PDF files work best
- **Where to put them**: In the `resumes` folder inside the application

### Step 3: Set Up the Application

1. **Find the application folder**: Look for the folder named "Super resumer" on your computer
2. **Open the folder**: You should see various files and folders
3. **Create a text file**:
   - Right-click in the folder
   - Choose "New Text File" or "New Document"
   - Name it `.env` (yes, it starts with a dot)
4. **Edit the .env file**:
   - Open the `.env` file with a text editor (Notepad, TextEdit, etc.)
   - Paste your API key after `OPENROUTER_API_KEY=`
   - It should look like: `OPENROUTER_API_KEY=sk-your-actual-key-here`
   - Save and close the file

### Step 4: Install Required Software (One-Time Setup)

1. **Open Terminal/Command Prompt**:
   - Windows: Press Windows key, type "cmd", press Enter
   - Mac: Press Command + Space, type "Terminal", press Enter
2. **Navigate to the application folder**:
   - Type: `cd "path/to/Super resumer"` (replace with actual path)
   - Example: `cd "C:\Users\YourName\Desktop\Super resumer"`
3. **Install the requirements**:
   - Type: `pip install -r requirements.txt`
   - Press Enter
   - Wait for installation to complete (this may take a few minutes)

### Step 5: Run the Application

1. **Keep the Terminal open**
2. **Type the command**:
   - Type: `streamlit run run_super_resumer.py`
   - Press Enter
3. **Wait for the application to start**
4. **You'll see a message**: "You can now view your Streamlit app in your browser"
5. **Open your web browser** (Chrome, Edge, Safari, etc.)
6. **Go to the address**: `http://localhost:8501`

---

## 🤖 How the Workflow Works (In Simple Terms)

### What Happens Automatically:

1. **🔍 It Searches for Jobs**
   - The application automatically looks for jobs on LinkedIn, Indeed, Naukri, and company websites
   - It searches specifically for C# Developer and Python AI jobs in Bangalore
   - It only looks for jobs paying 7+ LPA salary

2. **🧠 It Matches Your Skills**
   - For each job found, it checks which of your resumes fits better
   - C# jobs → Uses your C# resume
   - Python/AI jobs → Uses your Python AI resume
   - It gives each job a "match score" from 0-100%

3. **✅ It Automatically Applies**
   - If a job matches your skills 85% or better, it automatically marks it as "Applied"
   - If a job doesn't match well (below 85%), it automatically rejects it
   - You only see the good jobs that match your skills

4. **🔄 It Keeps Running**
   - Every 5 minutes, it automatically searches for new jobs
   - It automatically applies to new matching jobs
   - You don't need to do anything - it works in the background

### What You See in the Application:

**Job List Table**:

- **Title**: Job name (e.g., "Senior C# Developer")
- **Company**: Company name (e.g., "Microsoft India")
- **Location**: Where the job is (e.g., "Bangalore")
- **Salary**: Salary range (e.g., "15-20 LPA")
- **Match Score**: How well it matches your skills (e.g., "92%")
- **Source**: Where it found the job (e.g., "LinkedIn", "Indeed")
- **Status**: "Applied", "Pending", or "Rejected"
- **Resume**: Which resume it used (e.g., "C# Developer", "Python AI Developer")

**Job Details**:

- When you click on a job, you see:
  - Full job description
  - Why it matched your skills
  - A direct link to the job application page

**Job Application Link**:

- Click the "Apply to this Job" link to open the actual job application page
- This takes you to the real application form on the company's website
- You manually complete the application on the job site

---

## 🎮 What You Need to Do (Very Simple)

### Daily Workflow:

1. **Start the application** (once per day or keep it running):
   - Open Terminal
   - Navigate to the folder
   - Type: `streamlit run run_super_resumer.py`
   - Open browser to `http://localhost:8501`

2. **Check the jobs** (optional):
   - Look at the job list in your browser
   - Review jobs and their match scores
   - Click "Apply to this Job" link on jobs you want to apply to

3. **Let it run** (recommended):
   - Keep the application running in the background
   - It will automatically find and apply to new jobs every 5 minutes
   - Check back whenever you want to see new applications

---

## ⚙️ What You Can Customize (Optional)

### In the Sidebar:

- **Location**: Change from "Bangalore" to your preferred city
- **Min Salary**: Change from "7 LPA" to your minimum salary requirement
- **Match Threshold**: Change from "85%" to be stricter or more lenient
- **Job Sources**: Enable/disable specific job boards

### To Change Settings:

1. Open the file: `core/config.py`
2. Edit the values (e.g., change `LOCATION = "Bangalore"` to `LOCATION = "Mumbai"`)
3. Save the file
4. Restart the application

---

## 🔧 Troubleshooting (If Something Goes Wrong)

### Application Won't Start:

- **Make sure you installed requirements**: Run `pip install -r requirements.txt`
- **Check your API key**: Ensure it's correctly entered in the `.env` file
- **Check Terminal location**: Make sure you're in the correct folder

### No Jobs Showing:

- **Wait a few minutes**: The application needs time to search for jobs
- **Check your internet connection**: Ensure you're connected to the internet
- **Try manual search**: Use the "Search Jobs" button in the sidebar

### Application Shows Errors:

- **Check the Terminal**: Look for error messages in the Terminal window
- **Restart the application**: Close and start again
- **Check your API key**: Make sure it's valid and has credits

---

## 📞 Getting Help

If you need help:

1. **Check the logs**: Look at the Terminal window for error messages
2. **Restart**: Try closing and starting the application again
3. **Check your setup**: Ensure API key and resumes are properly configured

---

## 🎉 Summary

**You only need to do 3 things:**

1. **Get an OpenRouter API key** (one-time setup)
2. **Put your resumes** in the resumes folder (one-time setup)
3. **Run the application** by typing one command (daily or keep running)

**Everything else happens automatically!**

- 🔍 It searches for jobs automatically
- 🧠 It matches your skills automatically
- ✅ It applies to good jobs automatically
- 🔄 It keeps running in the background automatically

**Think of it as having a personal job application assistant that works 24/7 without breaks!**
