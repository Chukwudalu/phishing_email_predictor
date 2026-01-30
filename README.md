# Phishing Email Detection System

## Overview

This project is a **machine-learning–based phishing detection system** that automatically analyzes incoming emails and labels them as **Phishing** or **Safe** *before the user opens them*.

The system integrates with the **Gmail API** to inspect email content in real time and applies security labels directly to the user’s inbox, helping reduce exposure to phishing and social engineering attacks.

---

## Features

* **Automated phishing detection** using machine learning
* **Pre-open email labeling** (“Phishing” / “Safe”) via Gmail labels
* **Secure Gmail API integration** with OAuth 2.0
* **Text analysis of email content** to identify suspicious patterns

---

## How It Works

1. The application connects to a user’s Gmail inbox using the **Gmail API** and OAuth authentication.
2. Incoming emails are retrieved and their content is extracted.
3. Email text is preprocessed
4. A machine learning model makes a prediction.
5. Based on the prediction, the email is automatically labeled:

   * **Phishing** → suspicious or malicious
   * **Safe** → safe or normal
6. Labels appear in the inbox before the email is opened.

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/yourusername/phishing-detection.git
cd phishing-detection
```

2. **Create a virtual environment (optional but recommended)**:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

---

## Running the Project

1. Make sure you have a Gmail account ready and have set up **OAuth credentials**.
2. Run the main script:

```bash
python main.py
```

3. The system will:

   * Connect to your Gmail inbox
   * Analyze incoming emails
   * Apply labels automatically: **Phishing** or **Safe**

4. Check your Gmail inbox to see labels applied before opening emails.

---

## Automation

You will need to host this script on a server of your choice for automation.

## Technologies Used

* **Python**
* **Gmail API**
* **OAuth 2.0**
* **Scikit-learn**
* **Natural Language Processing (NLP)**

---

## Future Improvements
* Introduce additional classifiers for comparison
* Improve false positive/false negative handling
* Expand labeling rules based on sender reputation or metadata

---

## Disclaimer

This project is for **educational and demonstration purposes**.
Users must explicitly authorize Gmail access, and no email data is stored beyond analysis.

---

## Author

**Jeremiah Okwuolisa** - 
Computer Information Technology Student
