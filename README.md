# Wordle Bot

This project is a bot that automatically plays the Wordle game using Selenium.

## Requirements

- Python 3.12.2
- Google Chrome (make sure the version is up-to-date)
- ChromeDriver (must match the version of Google Chrome installed)

## Setup

1. **Clone the repository**:

   ```sh
   git clone https://github.com/hobbiesmarlon/Wordle-Bot.git
   cd Wordle-Bot
   ```

2. **Create a virtual environment**:

   - **Windows**:
     ```sh
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install the required packages**:

   ```sh
   pip install -r requirements.txt
   ```

4. **Download ChromeDriver**:

   - Visit the [ChromeDriver download page](https://sites.google.com/chromium.org/driver/downloads).
   - Download the version that matches your installed version of Google Chrome.
   - You can check your Chrome version by typing `chrome://version` in the address bar of your browser.
   - Extract the downloaded file to a directory and add that directory to your system’s PATH environment variable.

   For example, on Windows, you can add ChromeDriver to your PATH by placing it in a directory like `C:\chromedriver` and then adding `C:\chromedriver` to your PATH environment variable.

## Running the Bot

1. **Run the bot**:
   ```sh
   python wordle.py
   ```

## Important Notes

- **ChromeDriver and Chrome Version Compatibility**:
  - You must manually download the version of ChromeDriver that matches your installed version of Google Chrome.
  - If you encounter issues, make sure your Chrome browser is updated to the latest version and that you have downloaded the corresponding version of ChromeDriver.
  - To check your Chrome version, type `chrome://version` in the address bar of your Chrome browser.

## File Descriptions

- `wordle.py`: The main script containing the bot logic.
- `requirements.txt`: Lists the dependencies for the project.
- `possible_words.txt`: A file containing a list of words that can be the target word.
- `allowed_words.txt`: A file containing a list of words that are accepted as guesses but not all can be the target word.

## Gallery


https://github.com/hobbiesmarlon/Wordle-Bot/assets/172140958/c0dea8a9-1ee9-41da-aa71-f43bdb0a92c7



## License

This project is not licensed and is provided as-is, without any warranty. You are free to use, modify, and distribute the code for personal use only. Commercial use or redistribution without permission is prohibited.

## Contributing

Contributions are welcome!
