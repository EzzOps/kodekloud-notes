# Best practice: Store your API key in an environment variable
api_key = os.getenv("OPENAI_API_KEY")  # e.g., export OPENAI_API_KEY="sk-..."

client = OpenAI(api_key=api_key)

# Open the audio file in binary mode
file_path = "/full/path/to/your/audio.mp3"
with open(file_path, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print("Transcribed Text:")
print(transcription.text)
```

Be sure to:

* Replace `"/full/path/to/your/audio.mp3"` with your file’s actual path.
* Set the `OPENAI_API_KEY` environment variable instead of hardcoding sensitive credentials.

> **triangle-alert** Never commit your API key to version control. Use environment variables or a secrets manager to keep your key secure.

## 3. Run the Script

Execute the script in your terminal:

```bash theme={null}
python speech_to_text.py
```

You should see output similar to:

```bash theme={null}
Transcribed Text:
Here is an example of me talking.
```

Congratulations! You’ve successfully converted speech from an audio file into text using OpenAI’s Whisper model.

## References & Further Reading

* [OpenAI Python SDK][openai-python]
* [OpenAI Audio Transcriptions Documentation][openai-audio]
* [Environment Variables Guide][env-guide]

[openai-api]: https://platform.openai.com/account/api-keys

[openai-python]: https://github.com/openai/openai-python

[openai-audio]: https://platform.openai.com/docs/guides/speech-to-text

[env-guide]: https://12factor.net/config

- [Watch Video](https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/73d9ede4-094f-437c-a376-4a8ce0ea3f26)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/introduction-to-openai/module/b6b7bec7-ed21-47d5-afbb-663df59f5e97/lesson/ac1df626-9557-4a62-a758-9f958f1aef79)


# Text to Speech

Source: https://notes.kodekloud.com/docs/Introduction-to-OpenAI/Text-Generation/Text-to-Speech/page

Build a text-to-speech pipeline in Python using OpenAI’s Chat API and Google’s gTTS library for generating and playing spoken responses.

Build a seamless **text-to-speech** pipeline in Python by combining [OpenAI’s Chat API](https://platform.openai.com/docs/guides/chat) with Google’s [gTTS library](https://pypi.org/project/gTTS/). Generate natural language responses from an LLM and have them spoken aloud automatically.

## Prerequisites

### 1. Install Dependencies

| Package                | Purpose                                                       | Install Command                                    |
| ---------------------- | ------------------------------------------------------------- | -------------------------------------------------- |
| gTTS                   | Google Text-to-Speech Python client                           | `pip install gTTS`                                 |
| OpenAI Python client   | Official OpenAI API SDK                                       | `pip install openai`                               |
| Audio playback utility | Play MP3 files (macOS: `afplay`; Linux: `mpg123` or `mpg321`) | `brew install mpg123` or `sudo apt install mpg123` |

> **lightbulb** This example is tested on Python 3.7+. If you use a different version, adjust commands as needed.

### 2. Set Your OpenAI API Key

```bash theme={null}
export OPENAI_API_KEY="your_openai_api_key"
```

> **triangle-alert** Never commit your API key to public repositories. Use a secure vault or environment manager in production.

***

## Imports and Client Initialization

Begin by importing standard libraries, gTTS, and initializing the OpenAI client:

```python theme={null}
import os
from gtts import gTTS
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

***

## 1. Define the Prompt

Decide what you want the model to say. For example:

```python theme={null}
prompt = "Tell me a story about a brave knight who loves basketball."
```

***

## 2. Text-to-Speech Function

Convert text to speech and play the resulting MP3:

```python theme={null}
def text_to_speech(text: str, lang: str = "en", slow: bool = False) -> None:
    """
    Generate speech from text using gTTS, save as MP3, and play it.
    """
    tts = gTTS(text=text, lang=lang, slow=slow)
    filename = "tts_output.mp3"
    tts.save(filename)
    # macOS uses 'afplay'; Linux users can install 'mpg123' or 'mpg321'
    os.system(f"afplay {filename}")
```

> **triangle-alert** Adjust the playback command (`afplay`, `mpg123`, or `mpg321`) based on your operating system.

***

## 3. Generate Text from OpenAI

Send the prompt to the Chat API and retrieve the response:

```python theme={null}
def generate_text(
    prompt: str,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.8,
    max_tokens: int = 150
) -> str:
    """
    Generate a chat completion for the given prompt.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content
```

***

## 4. Combine Generation and Speech

Create a helper that prints the generated text, then speaks it:

```python theme={null}
def gen_and_speak(prompt: str) -> None:
    """
    Generate text from the prompt, display it, and play the speech.
    """
    text = generate_text(prompt)
    print("Generated Text:\n")
    print(text, "\n")
    text_to_speech(text)
```

***

## 5. Entry Point

Run the full pipeline with your defined prompt:

```python theme={null}
if __name__ == "__main__":
    gen_and_speak(prompt)
```

***

## Example Console Output

```bash theme={null}
$ python3 text_to_speech_pipeline.py
Generated Text:

Once upon a time in the kingdom of Eldoria, there lived a brave knight named Sir Cedric...
