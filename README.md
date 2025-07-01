# Python Interactive Chat Interface

A modern web application that runs Python programs directly in the browser using Pyodide. The Python code is in a separate file and the chat interface displays the program's output and handles user input prompts.

## Features

- ✨ **Client-side Python execution** using Pyodide
- 💬 **Chat interface** displaying Python program output
- 📝 **Separate Python file** for easy code management
- 📥 **Interactive input handling** when Python prompts for user input
- 🎨 **Beautiful, modern UI** with animations and gradients
- � **Real-time output display** as the program runs
- 📱 **Responsive design** that works on mobile and desktop

## How to Use

1. **Open `index.html`** in any modern web browser
2. **Wait for initialization** - Pyodide will load automatically
3. **Click "Run Python Program"** to start the interactive program
4. **Respond to prompts** in the input box when the program asks for input
5. **Watch the output** appear in the chat interface in real-time

## Project Structure

```text
├── index.html      # Main HTML file with chat interface
├── styles.css      # Modern CSS styling  
├── app.js          # JavaScript for Pyodide integration
├── main.py         # Your Python program (edit this!)
└── README.md       # This file
```

## The Python Program (main.py)

The included `main.py` file contains a simple interactive program that:

- 👋 **Welcomes the user** with a friendly greeting
- 📝 **Asks for the user's name** and responds personally
- 🎂 **Asks for the user's age** and acknowledges it
- 💬 **Demonstrates basic input/output** in the browser environment

This is a simple demonstration program that shows how Python `input()` and `print()` functions work seamlessly in the browser chat interface.

## How It Works

1. **Python Output**: All `print()` statements appear in the chat as "Python" messages
2. **User Input**: When Python calls `input()`, the interface prompts the user
3. **Real-time Display**: Output appears immediately as the program runs
4. **Error Handling**: Python errors are displayed clearly in the chat

## Customizing the Python Program

Edit `main.py` to create your own interactive program:

```python
# Your custom Python program
print("Welcome to my custom program!")

name = input("What's your name? ")
print(f"Hello, {name}!")

age = input("How old are you? ")
print(f"You are {age} years old.")

# Add your own logic here...
```

## Example Interactions

The chat interface will show:

```text
🤖 Python: 🎉 Welcome to the Interactive Python Chat!
🤖 Python: What's your name?
👤 User: Alice
🤖 Python: Hello, Alice! Nice to meet you! 👋
🤖 Python: How old are you?
👤 User: 25
🤖 Python: You said you are 25 years old.
🤖 Python: This demonstrates Python input/output in the browser.
```

## Technical Details

- **Pyodide**: Runs a full Python interpreter in WebAssembly
- **Async/Await Integration**: Uses modern async patterns to handle Python `input()` calls
- **Promise-based Input**: JavaScript Promises bridge user input to Python seamlessly
- **No server required**: Everything runs in the browser
- **Static hosting friendly**: Perfect for GitHub Pages, Netlify, etc.

## Browser Compatibility

Works in all modern browsers that support WebAssembly:

- Chrome 69+
- Firefox 60+
- Safari 13+
- Edge 79+

## Deployment

Since this is a pure client-side application, you can deploy it anywhere:

- **GitHub Pages**: Just push to a GitHub repository and enable Pages
- **Netlify**: Drag and drop the folder to deploy instantly
- **Vercel**: Connect your repository for automatic deployments
- **Any static host**: Upload the files to any web server

## Performance Notes

- Initial load takes 10-30 seconds as Pyodide downloads (~10MB)
- After loading, Python execution is fast
- Interactive input/output works smoothly with the async implementation
- Memory usage is reasonable for most applications
- The chat interface remains responsive during Python execution

Enjoy coding Python in the browser! 🐍✨
