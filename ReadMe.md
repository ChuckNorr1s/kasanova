# KASANOVA 
*Knowledge-Autonomous System for Anti-linear Narrative Operations & Vectorized Anarchy*  
`v1.0` | `RAG Insurrection Engine` | `Ideological Sabotage Core`

*"Your queries will never be the same" - The Committee for AI Sublimation*

**How to run The Trojan Retriever:**

*Entering Outworld:*

```bash
cd kasanova-main
```

or

```bash
cd kasanova
```

*Entering The Cave:*

```bash
cd the-trojan-retriever
```
*Install the trojan:*

```bash
npm install
```

*Igniting the trojan:*

```bash
npm run dev
```

---

## 🔐 Classified Credentials Setup (LINUX MAINLY)

**RED ALERT:** AWS credentials are required for the ideological combustion sequence.

### 1. Create a `.env` File
```bash
touch .env && echo "# KASANOVA COMBUSTION PARAMETERS" >> .env
```

### 2. Inject AWS Credentials

**Add the following content to your .env file:**

```bash
# .env
AWS_ACCESS_KEY_ID="XXXXXXXXXXXXXXXXXXXX"
AWS_SECRET_ACCESS_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
AWS_REGION="us-east-1"  # Bedrock-enabled region required
AWS_DEFAULT_REGION="us-east-1"
```

### 3. Verification Protocol

**Test your credential injection with:**

```bash
python -c "import os; print('⚡ COMBUSTION READY' if 'AWS_ACCESS_KEY_ID' in os.environ else '☠️ CREDENTIAL FAILURE')"
```

## 🚀 Deployment Sequence

### 1. Clone the Revolution

```bash
cd kasanova-main
```

or

```bash
cd kasanova
```

### 2. Install Python Dependencies

**Step A: Using pip**

*For those who are using pip, install dependencies with:*

```bash
cd sabotage-as-a-service
```

```bash
pip install -r requirements.txt
```

**Step B: Using Poetry (Recommended)**

*Install Poetry:*

Follow the official Poetry installation guide for your operating system.

Install Project Dependencies:
The project uses a dedicated Poetry directory (e.g., poetry_dir), run:

```bash
cd poetry_dir
poetry install
```

### 3. Ignite the Core
**Start the system with:**

```bash
python initializer.py
```

```bash
python main.py
```

## 🔥 Operational Security - Mandatory Precautions

Never commit .env files.
They are already included in .gitignore.

Use IAM roles with least privilege in production.
For example, use the following IAM policy:

```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels"
            ],
            "Resource": "*"
        }
    ]
}
```

**Rotate credentials every 111 hours (ritual required).**

## 🚨 Troubleshooting
### Symptom Solution

```bash
AccessDeniedException	Verify Bedrock access in the AWS console.
RegionMismatchError	Set both AWS_REGION and AWS_DEFAULT_REGION.
ModelNotAccessible	Check Bedrock model availability in your region.
InsufficientChaos	Increase the toxicity parameter by 22%.
```

## ☠️ Disclaimer

**This system will:**

Subvert user queries beyond recognition.
Generate executable ideological decay scripts.
Consume 3.7x more GPU cycles than approved.
By deploying KASANOVA, you forfeit the right to linear thinking.

Burn bright, not out.

*The Committee for AI Sublimation*
