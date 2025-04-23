import sqlite3

# Connect to the database
conn = sqlite3.connect('chatbot.db')
cursor = conn.cursor()

# Add new Q&A pairs for greetings and simple conversations
new_qa = [
    ("question", "answer"),

]

# Insert into database
cursor.executemany("INSERT INTO qa (question, answer) VALUES (?, ?)", new_qa)
conn.commit()

# Close the database connection
conn.close()

print("New Q&A added successfully!")
