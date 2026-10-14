import json

with open('data_generator.py', 'r', encoding='utf-8') as f:
    dg_code = f.read()

with open('recommender.py', 'r', encoding='utf-8') as f:
    rec_code = f.read()

with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

notebook = {
    'nbformat': 4,
    'nbformat_minor': 0,
    'metadata': {
        'colab': {'name': 'One_Click_Colab_Campus_Recommender_Adarsh_S.ipynb', 'provenance': []},
        'kernelspec': {'name': 'python3', 'display_name': 'Python 3'},
        'language_info': {'name': 'python'}
    },
    'cells': [
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '# Campus Event Recommendation Engine (Assignment No. 32)\n',
                '### **Author: Adarsh S**\n',
                'Click **Runtime -> Run all** (or press Ctrl+F9). In 30 seconds, your live public app will be hosted on Google Colab with an official Cloudflare link!'
            ]
        },
        {
            'cell_type': 'code',
            'metadata': {},
            'execution_count': None,
            'outputs': [],
            'source': [
                '# Step 1: Install dependencies and download Cloudflare Tunnel\n',
                '!pip install -q streamlit pandas numpy scikit-learn\n',
                '!wget -q -O cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64\n',
                '!chmod +x cloudflared\n',
                'print("Dependencies and Cloudflare ready!")'
            ]
        },
        {
            'cell_type': 'code',
            'metadata': {},
            'execution_count': None,
            'outputs': [],
            'source': [
                '%%writefile data_generator.py\n' + dg_code
            ]
        },
        {
            'cell_type': 'code',
            'metadata': {},
            'execution_count': None,
            'outputs': [],
            'source': [
                '%%writefile recommender.py\n' + rec_code
            ]
        },
        {
            'cell_type': 'code',
            'metadata': {},
            'execution_count': None,
            'outputs': [],
            'source': [
                '%%writefile app.py\n' + app_code
            ]
        },
        {
            'cell_type': 'code',
            'metadata': {},
            'execution_count': None,
            'outputs': [],
            'source': [
                '# Step 5: Start Streamlit and Launch Cloudflare Tunnel\n',
                'import subprocess, time, re\n',
                '\n',
                '# Run Streamlit in background\n',
                'subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"])\n',
                'time.sleep(4)\n',
                '\n',
                '# Run Cloudflare Tunnel\n',
                'p = subprocess.Popen(["./cloudflared", "tunnel", "--url", "http://localhost:8501"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)\n',
                'print("Waiting for Cloudflare Tunnel to generate your live public link...")\n',
                '\n',
                'for line in p.stdout:\n',
                '    if "trycloudflare.com" in line:\n',
                '        m = re.search(r"https://[a-zA-Z0-9-]+\\.trycloudflare\\.com", line)\n',
                '        if m:\n',
                '            print("\\n" + "="*65)\n',
                '            print("YOUR LIVE APP IN GOOGLE COLAB IS HOSTED AND READY:")\n',
                '            print(m.group(0))\n',
                '            print("="*65 + "\\n")\n',
                '            break\n'
            ]
        }
    ]
}

with open('ONE_CLICK_COLAB.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print('ONE_CLICK_COLAB.ipynb generated successfully!')
