from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import defaultdict
from selenium.common.exceptions import TimeoutException

# Load the word list
with open('possible_words.txt', 'r') as file:
    words = [line.strip() for line in file.readlines()]


# Function to set up the WebDriver
def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--incognito')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    return driver


# Function to handle initial navigation and pop-ups
def navigate_to_wordle(driver):
    driver.get('https://www.nytimes.com/games/wordle/index.html')

    try:
        cookie_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept']"))
        )
        cookie_button.click()
    except Exception as e:
        print("No cookie popup found or error:", e)

    try:
        play_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='Play']"))
        )
        play_button.click()
    except Exception as e:
        print("Error finding or clicking the play button:", e)

    try:
        close_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
        )
        close_button.click()
    except TimeoutException:
        print("Error finding or clicking the close button of the pop-up.")

    try:
        hint_close_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'Tooltip-module_close__coDA6')]"))
        )
        hint_close_button.click()
    except TimeoutException:
        print("No hint pop-up found or timed out.")


# Function to input a word and retrieve feedback
def input_word_and_get_feedback(driver, word, tries):
    for letter in word:
        try:
            key_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[@data-key='{letter}']"))
            )
            key_button.click()
        except Exception as e:
            print(f"Error finding or clicking the key '{letter}':", e)

    try:
        enter_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-key='↵']"))
        )
        enter_button.click()
    except Exception as e:
        print("Error finding or clicking the enter button:", e)

    time.sleep(2)

    feedback = []
    try:
        row_tiles = driver.find_elements(By.XPATH, f"//div[@aria-label='Row {tries}']//div[contains(@class, 'Tile-module_tile__')]")
        for tile in row_tiles:
            feedback.append(tile.get_attribute('data-state'))
    except Exception as e:
        print("Error fetching feedback:", e)

    return feedback


# Function to filter words list based on feedback
def filter_words(words, guess, feedback):
    filtered_words = []
    
    for word in words:
        letter_counts = defaultdict(int)
        for letter in guess:
            letter_counts[letter] += 1

        match = True
        for i, (letter, fb) in enumerate(zip(guess, feedback)):
            if fb == 'correct':
                if word[i] != letter:
                    match = False
                    break
                letter_counts[letter] -= 1
            elif fb == 'present':
                if letter not in word or word[i] == letter or letter_counts[letter] <= 0:
                    match = False
                    break
                letter_counts[letter] -= 1
            elif fb == 'absent':
                if word.count(letter) > guess.count(letter) - (letter_counts[letter] - word[:i].count(letter)):
                    match = False
                    break

        if match:
            filtered_words.append(word)

    return filtered_words


# Function to calculate letter frequencies
def calculate_letter_frequencies(words):
    letter_frequencies = defaultdict(int)
    for word in words:
        for letter in word:
            letter_frequencies[letter] += 1
    return letter_frequencies


# Function to score words based on letter frequencies
def score_words_by_frequency(words, letter_frequencies):
    word_scores = {}
    for word in words:
        score = sum(letter_frequencies[letter] for letter in set(word))
        word_scores[word] = score
    return word_scores


# Function to choose the best next word based on frequency scores
def choose_best_word_by_frequency(words):
    if words:
        letter_frequencies = calculate_letter_frequencies(words)
        word_scores = score_words_by_frequency(words, letter_frequencies)
        return max(word_scores, key=word_scores.get)


# Main function to execute the process
def main():
    driver = setup_driver()
    navigate_to_wordle(driver)
    time.sleep(5)

    tries = 0
    current_word = 'salet'

    while tries < 6:
        tries += 1
        feedback = input_word_and_get_feedback(driver, current_word, tries)
        print(f"Feedback on the entered word '{current_word}':", feedback)

        if all(f == 'correct' for f in feedback):
            print(f"Word '{current_word}' is correct! Solved in {tries} tries.")
            break

        global words
        words = filter_words(words, current_word, feedback)
        current_word = choose_best_word_by_frequency(words)
        print("Next word to guess:", current_word)

    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    main()
