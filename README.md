<div align="center">
    <h1>Nebula Chatbot</h1>
    <img src="./src/pubic/nebula-avatar.png" alt="Nebula Logo" width="250"/>
</div>

## Description
This project is an AI chatbot application built using Streamlit. It leverages OpenAI's GPT-4o-mini model to provide intelligent and context-aware responses. The application supports multiple chat sessions and allows users to input their OpenAI API key for personalized interactions.

## Features
- Multiple chat sessions management
- User-friendly interface with Streamlit
- Secure API key input
- Context-aware responses using GPT-4o-mini

## Libraries and Tools Used
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [OpenAI GPT-4o-mini](https://platform.openai.com/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ai-chatbot.git
    cd ai-chatbot
    ```
2. Create a virtual enviorment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual enviorment:
    ```bash
    venv/Scripts/activate
    ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
5. Create a `.env` file in the root directory and add your OpenAI API key and Langchain API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_API_KEY=your_langchain_api_key
    ```

## Running the Project
To run the application, use the following command:
```bash
streamlit run src/app.py
```

## Modules and Components
- **config.py**: Manages configuration settings and environment variables.
- **session_manager.py**: Handles session management and chat history.
- **chatbot.py**: Implements the core chatbot functionality using LangChain components.
- **app.py**: Main Streamlit application file that coordinates between different components.

## Folder Structure
- **/script**: Contains just the script for running the chatbot without ui with explanation on how everythin works. It is exactly the same as I write while creating it without ui for instructions and any related references.
- **/src**: Contains the main application files.
  - **config.py**: Configuration management.
  - **session_manager.py**: Session management.
  - **chatbot.py**: Chatbot logic.
  - **app.py**: Streamlit application.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
