'use strict';
 
const functions = require('firebase-functions');
const { WebhookClient } = require('dialogflow-fulfillment');
const { Card, Suggestion } = require('dialogflow-fulfillment');
const { dialogflow } = require('actions-on-google');
const app = dialogflow({ debug: true });
var repromptIndex = 0;
var repromptIndex2 = 0;
var lastIntent= null;

process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

const repromptMessagesAppName = [
  'Please provide the Application Name.',
  'Please choose the relevant Application Name.',
  'Kindly provide the Application Name to proceed further.',
  'Please reach out to the System Administrator to find the correct Application Name value and try again later. GoodBye!'
];

const repromptMessagesSeverity = [
  'Please provide Issue Severity',    
  'Please choose a relevant Issue Severity',   
  'Please provide the correct Issue Severity from - Showstopper, High, Medium, Low, or Trivial.',
  'Please provide the correct Issue Severity from - Showstopper, High, Medium, Low, or Trivial.',
  'Sorry, this is not the correct value of Severity. Please retry.',
];
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function welcome(agent) {
    agent.add('Welcome to my agent!');
         repromptIndex = 0;
         repromptIndex2 = 0;
  }
 
  function fallback(agent) {
    agent.add("I didn't understand");
    agent.add("I'm sorry, can you try again?");
         repromptIndex = 0;
         repromptIndex2 = 0;
  }
 
  function ReturnResponse(agent) {
    const appname = agent.parameters.ApplicationName;
    const severity = agent.parameters.Severity;
    console.log('appname is: ' + appname);
    
    if (severity ) {        
         repromptIndex2 = 0;
      } 
    
    if (appname) {
      console.log('appname is: ' + appname);
      repromptIndex = 0; 
     
      if (severity) {
        console.log('severity is: ' + severity);
        //agent.add(`Ok, noted. Confirming issue Application - ${appname} and Severity as ${severity}`);
         agent.add(`Thanks for sharing all the required information. Please wait a moment while I process the details.`);
         repromptIndex = 0;
         repromptIndex2 = 0;
      } 
      
      else if  (!severity) {
       const repromptMessage2 = repromptMessagesSeverity[repromptIndex2];
       repromptIndex2 = (repromptIndex2 + 1) % repromptMessagesSeverity.length;
      // agent.add(`Ok, noted. Please provide issue Severity.`);
        agent.add(repromptMessage2);
        console.log('repromptIndex2 58- ' + repromptIndex2);
        console.log('repromptMessage2 58- ' + repromptMessage2);
       
      }
      
    } 
    else {
      const repromptMessage = repromptMessagesAppName[repromptIndex];
      repromptIndex = (repromptIndex + 1) % repromptMessagesAppName.length;
      agent.add(repromptMessage);
      console.log('repromptMessage-' + repromptMessage);
    }
    
   
    
  }
  
   
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('CreateTicket-getDetails', ReturnResponse);  
 // intentMap.set('CreateTicket-getdetails-getseverity', ReturnSeverityResponse);
  agent.handleRequest(intentMap);
 
 
});
