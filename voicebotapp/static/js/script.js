 // Append a new message to the chat log
      //function appendMessage(message) {
      //var chatLog = $('#chat-log');
      //var messageElement = $('<p>').text(message);
     // chatLog.append(messageElement);
    //}


    setTimeout(function() {
      var chatLog = document.getElementById('chat-log');
      //chatLog.innerHTML += `<img class="botchatimg" src="{% static 'images/botchatimg.png' %}" alt="">`;
      chatLog.innerHTML += `<p class="bot-text">Hi! 👋 it's great to see you!</p>`;
      //chatLog.appendChild(chatLog);
    }, 3500);



      document.getElementById("chat-form").addEventListener("submit", function(event) {
          event.preventDefault();
          var formData = new FormData(event.target);
          var csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
          formData.append('csrfmiddlewaretoken', csrftoken);


          var conversation = document.getElementById('conversation');

          var userMessage = document.getElementById('entry-box').value;
          var chatLog = document.getElementById('chat-log');

          // Clear input field
          document.getElementById('entry-box').value = '';
          const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: "2-digit" });

          //chatLog.innerHTML += 'You: ' + userMessage + '\n';
          //chatLog.innerHTML += '<p class="user-message">You: ' + userMessage + '</p>\n';
          //chatLog.innerHTML += '<p class="bot-text">You: ' + userMessage + '</p>\n';

          let chatLog1 = document.createElement('div');
          //chatLog1.classList.add('chat-log', 'user-message');
          //chatLog1.innerHTML += `<img class="userchatimg" src="{% static 'images/userchatimg.png' %}" alt="">`;
          chatLog1.innerHTML += `<p class="user-message" sentTime="${currentTime}">${userMessage}</p>`;
          conversation.appendChild(chatLog1);
          chatLog1.scrollTop = chatLog.scrollHeight;



          $.ajax({
              type: 'POST',
              url: 'chatbot',
              data: formData,
              processData: false,
              contentType: false,

              //chatLog1 = document.createElement('div');
              //chatLog1.innerHTML += '<div class="loading">...</div>';
              //conversation.appendChild(chatLog1);

              success: function(response) {

                  chatLog1 = document.createElement('div');
                  
                  //chatLog1.classList.add('chat-log','bot-text');
                  //chatLog.innerHTML += 'Bot: ' + response.response + '\n';
                  //chatLog.innerHTML += '<p class="bot-message">Bot: ' + response.response + '</p>\n';
                  //chatLog1.innerHTML += `<p class="bot-text" sentTime="${currentTime}">${response.response}</p>`;
        
                  //if (response.results.length === 3) {
                    //  chatLog.innerHTML += ` 
                      //<p class="bot-text" sentTime="${currentTime}">${response.results[0]}</p> 
                      //<p class="bot-text" sentTime="${currentTime}">${response.results[1]}</p> 
                      //<p class="bot-text" sentTime="${currentTime}">${response.results[2]}</p> `; } 
                      
                      
                      //else if (response.results.length === 1) { 
                          //chatLog1.innerHTML += `<img class="botchatimg" src="{% static 'images/botchatimg.png' %}" alt="">`;
                          chatLog1.innerHTML += `<p class="bot-text" sentTime="${currentTime}">${response.response}</p>`; 
                      //}
                              
              
                  
                  conversation.appendChild(chatLog1);
                  //message.scrollIntoView({behavior: "smooth"});
                  chatLog1.scrollTop = chatLog.scrollHeight;
                  chatLog1.scrollIntoView({behavior: "smooth"});

              },
              error: function() {
                  console.log('Error occurred.');
              }
          });
      });


      var audiobutton = document.getElementById('audiobutton');
      let micImageOff = document.getElementById("micoff");
      let micImageOn = document.createElement("micon");

      function toggleMic() {
          var audiobutton = document.getElementById('audiobutton');
          let micImageOff = document.getElementById("micoff");
          let micImageOn = document.createElement("micon");
          micImageOff.remove(micImageOff);
          audiobutton.innerHTML += `<img id="micon" onclick="stopVoiceInput()" class="mic-iconOn" src="{% static 'images/mic-blue.png' %}" alt="">`;
          //audiobutton.appendChild(micImageOn);
          
            
      }


      function startVoiceInput() {
          var recognition = new webkitSpeechRecognition();
          recognition.continuous = false;
          recognition.interimResults = false;

          toggleMic();

          var conversation = document.getElementById('conversation');
    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: "2-digit" });

          recognition.onresult = function(event) {
              var result = event.results[event.results.length - 1];
              var voiceText = result[0].transcript;


              audiobutton = document.getElementById('audiobutton');
              micImageOff = document.getElementById("micoff");
              //let micImageOn = document.createElement("micon");
              micImageOn = document.getElementById("micon");
              micImageOn.remove(micImageOn);
              audiobutton.innerHTML += `<img id="micoff" class="mic-icon" src="{% static 'images/mic-blue.png' %}" alt="">`;
              //audiobutton.appendChild(micImageOff);

              let chatLog1 = document.createElement('div');
              //chatLog.innerHTML += 'You: ' + voiceText + '\n';
              //chatLog.innerHTML += '<p class="user-message">You: ' + voiceText + '</p>\n';
              //chatLog1.innerHTML += `<img class="userchatimg" src="{% static 'images/userchatimg.png' %}" alt="">`;
              chatLog1.innerHTML += `<p class="user-message" sentTime="${currentTime}">${voiceText}</p>`;
              
              conversation.appendChild(chatLog1);
              //chatLog1.scrollTop = chatLog.scrollHeight;


              $.ajax({
                  type: 'POST',
                  url: 'chatbot',
                  data: { 'voice_data': voiceText },
                  beforeSend: function(xhr, settings) {
                      xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
                  },
                  success: function(response) {
                      //let chatLog1 = document.createElement('div');
                      //chatLog.innerHTML += 'You: ' + voiceText + '\n';
                      //chatLog.innerHTML += '<p class="user-message">You: ' + voiceText + '</p>\n';
                      //chatLog1.innerHTML += `<p class="user-message"sentTime="${currentTime}">${voiceText}</p>`;
          
          //conversation.appendChild(chatLog1);
                      
                      //chatLog.innerHTML += 'Bot: ' + response.response + '\n';

                      //chatLog.innerHTML += '<p class="bot-message">Bot: ' + response.response + '</p>\n';
                      chatLog1 = document.createElement('div');
                      //chatLog1.innerHTML += `<img class="botchatimg" src="{% static 'images/botchatimg.png' %}" alt="">`;
                      chatLog1.innerHTML += `<p class="bot-text" sentTime="${currentTime}">${response.response}</p>`;

                    conversation.appendChild(chatLog1);
                      chatLog1.scrollIntoView({behavior: "smooth"});
                      chatLog1.scrollTop = chatLog1.scrollHeight;
                  },
                  error: function() {
                      console.log('Error during voice input.');
                  }
              });
          };


          
          recognition.start();
          
      }
      function stopVoiceInput() {
          var recognition = new webkitSpeechRecognition();
          recognition.stop();
      }