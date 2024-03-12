const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");

let userMessage = null; // Variable to store user's message
const API_KEY = "AIzaSyBdb1Jwz9j8s8PkOxa0FXkmzN2V7wNCifc"; 
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi; // return chat <li> element
}

//
// function runPythonScript(chatElement) {
//     var userInput = userMessage;
//     // Send user input to the server-side script using AJAX
//     var xhr = new XMLHttpRequest();
//     xhr.open("POST", "/run_script", true);
//     xhr.setRequestHeader("Content-Type", "application/json");
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState === 4 && xhr.status === 200) {
//             var response = JSON.parse(xhr.responseText);
//             chatElement.innerHTML = response.output;
//         }
//     };
//     xhr.send(JSON.stringify({ input: userInput }));
//     console.log(xhr.send(JSON.stringify({ input: userInput })))
// }
//

const generateResponse = (chatElement) => {

    // runPythonScript(chatElement)

    const messageElement = chatElement.querySelector("p");
    // const API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + API_KEY;
    const API_URL = "http://127.0.0.1:5000/bot"

    /*
    const requestOptions = {
        method: 'POST',
        // method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            contents: [{
                parts: [{
                    text: `${userMessage}`
                }]
            }],
            safetySettings: [{
                category: "HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold: "BLOCK_ONLY_HIGH"
            }],
            generationConfig: {
                stopSequences: [
                    "Title"
                ],
                temperature: 0.7,
                maxOutputTokens: 200,
                topP: 0.8,
                topK: 10
            }
        })
    }
    // Send POST request to API, get response and set the reponse as paragraph text
    fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
        // console.log(data)
        messageElement.textContent = data.candidates[0].content.parts[0].text;
    }).catch(() => {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
    }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
    */
    fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userMessage)
      })
        .then(response => response.json())
        .then(result => {
          // Update UI with the result
          console.log('Result:', result);
          messageElement.textContent = result
        })
        .catch(error => {
          console.error('Error:', error);
          messageElement.classList.add("error");
          messageElement.textContent = "Oops! Something went wrong. Please try again.";
        }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

const handleChat = () => {
    userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
    if(!userMessage) return;

    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);
    
    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("Thinking...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        generateResponse(incomingChatLi);
    }, 600);
}

chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);
closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));