# Monday: A Python Text Adventure in Your Browser

This project brings the classic, comedic text adventure **"Monday"** to the web! Play through a wild, unpredictable school day full of choices, jokes, and bizarre outcomes—all running in your browser thanks to Pyodide.

## Features

- 🎮 **Play "Monday"—a full-length, branching text adventure**
- 🤣 **Humorous writing and unpredictable outcomes**
- 🏫 **Navigate a day in the life of a high school student**
- 💬 **Interactive chat interface for game narration and choices**
- ✨ **Runs entirely in your browser—no server needed**
- 💾 **(Optional) Save/load support if cryptography is available**
- 📱 **Responsive design** that works on mobile and desktop

## How to Play

1. **Open `index.html`** in any modern web browser
2. **Wait for initialization** — Pyodide will load automatically
3. **Click "Run Python Program"** to start "Monday"
4. **Make choices** as prompted to guide your character through the day
5. **See the story unfold** in the chat interface

## Project Structure

```text
├── index.html      # Main HTML file with chat interface
├── styles.css      # Modern CSS styling  
├── app.js          # JavaScript for Pyodide integration
├── main.py         # A Python test program (can edit this!)
├── monday.py       # The "Monday" text adventure game
└── README.md       # This file
```

## About the Game (monday.py)

The included `monday.py` file is a full-featured, branching text adventure. You play as a high school student trying to survive the world’s worst Monday. Make choices, explore different paths, and try to reach a good ending—if you can!

- 🛏️ **Wake up and face the chaos of Monday**
- 🚌 **Navigate school, social situations, and bizarre events**
- 💀 **Many ways to lose, a few ways to win!**
- 🤪 **Packed with jokes, pop culture, and absurd scenarios**

## Example Interaction

```text
🤖 Python: YOU'RE IN BED, ASLEEP.
🤖 Python: IT'S 5:15 A.M.
🤖 Python: YOUR STEREO TURNS ON AND A LOCAL RADIO STATION IS PLAYING A SONG BY PRINCE.
🤖 Python: WHAT A BAD WAY TO START A DAY!
🤖 Python:   YOU WAKE UP
  1. SNOOZE
  2. GET UP
  3. SMASH STEREO
👤 User: 2
🤖 Python: YOU GET UP AND STRETCH. AS YOU TAKE A DEEP BREATH, FOULNESS INVADES YOUR NOSTRILS...
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

Enjoy surviving Monday in the browser! 🐍🎮
