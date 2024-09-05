using llamaindex rag-cli: https://docs.llamaindex.ai/en/stable/getting_started/starter_tools/rag_cli/

and ollama https://ollama.com

to do simple rag on a textbook pdf from the cli


# to Run (untill I add it to .bashrc)
1. run `ollama serve`
2. potentially run `ollama run llama3.1:8b`
3. activate venv
4. python3.11 rag_cli.py rag -c -f ../textbook/software_engineering_textbook/
5. profit? learn something? It's all broken so cry?

## Allegedly
From there, you're just a few steps away from being able to use your custom CLI script:

Make sure to replace the python path at the top to the one your virtual environment is using (run $ which python while your virtual environment is activated)

Let's say you saved your file at /path/to/your/script/my_rag_cli.py. From there, you can simply modify your shell's configuration file (like .bashrc or .zshrc) with a line like $ export PATH="/path/to/your/script:$PATH".

After that do $ chmod +x my_rag_cli.py to give executable permissions to the file.
That's it! You can now just open a new terminal session and run $ my_rag_cli.py -h. You can now run the script with the same parameters but using your custom code configurations!
Note: you can remove the .py file extension from your my_rag_cli.py file if you just want to run the command as $ my_rag_cli --chat
