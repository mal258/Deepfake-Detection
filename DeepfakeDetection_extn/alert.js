

'use strict';


document.addEventListener('DOMContentLoaded', function () {


    var btn1 = document.getElementById('info');
    btn1.addEventListener('click', function() {
        chrome.windows.create({'url': 'http://35.184.128.190:5008/static/pred_video.mp4', 'type': 'popup'}, function(window) {
   });
    });
     var btn2 = document.getElementById('cache');
    btn2.addEventListener('click',function(){
        chrome.storage.local.clear();
    });
});

function showPopupWindow(){
  chrome.windows.create({'url': 'http://35.184.128.190:5008/static/pred_video.mp4', 'type': 'popup'}, function(window) {
   });
   }
function showMainResults(result) {

  document.getElementById('loader').style.display = "none";

  document.getElementById('progress').textContent = "";
  document.getElementById('predictionResult').textContent = "Prediction:";

  if (result[0]>result[1]){
   document.getElementById('real').style.display = "block";
  document.getElementById('real').textContent=result[0]+"% real";
  }
  else
  {   document.getElementById('fake').style.display = "block";

  document.getElementById('fake').textContent=result[1]+"% fake";
  }



  document.getElementById('info').style.display = "block";

}

function showCachedResults(result) {

  document.getElementById('loader').style.display = "none";

  document.getElementById('progress').textContent = "";
  document.getElementById('predictionResult').textContent = "Prediction(Cached):";

  if (result[0]>result[1]){
   document.getElementById('real').style.display = "block";
  document.getElementById('real').textContent=result[0]+"% real";
  }
  else
  {   document.getElementById('fake').style.display = "block";

  document.getElementById('fake').textContent=result[1]+"% fake";
  }



  document.getElementById('cache').style.display = "block";

}

function getModelResults(urlModelRestAPI, youtubeURL) {

    return new Promise(function(resolve, reject) {

    var xhr = new XMLHttpRequest();
    xhr.open("POST", urlModelRestAPI, true);


     xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

    xhr.onreadystatechange = function() {
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200)
      {

          resolve(xhr.responseText);
      }
    }


    xhr.send("url=" + youtubeURL);
  });
}


const urlModelRestAPI ="http://35.184.128.190:5008/work_ext" ;



chrome.tabs.query({"active": true, "lastFocusedWindow": true}, function (tabs) {

var search=false;
    var youtubeURL = tabs[0].url;


        if (youtubeURL != undefined || youtubeURL != '') {
            var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
            var match = youtubeURL.match(regExp);
            if (match && match[2].length == 11) {


     document.getElementById('info').style.display = "none";
     document.getElementById('cache').style.display = "none";



 chrome.storage.local.get("youtubeURLs", function (result) {


    var youtubeURLs = result.youtubeURLs;
    console.log("youTubeURLs"+youtubeURLs);
if(youtubeURLs){
  for(var i=0; i<youtubeURLs.length; i++){
	if(youtubeURLs[i].hasOwnProperty(youtubeURL)){

    showCachedResults(youtubeURLs[i][youtubeURL]);
    search=true;
    break;
    }
}}
else{
youtubeURLs=[];
}


   if(!search){





console.log("Model API and youtube URL: "+urlModelRestAPI+"+"+youtubeURL);


    getModelResults(urlModelRestAPI, youtubeURL).then(function(result) {


  const modelResults = result;
  console.log('result = ' + result);


  const jsonObj = JSON.parse(modelResults);

console.log("result json object"+jsonObj);
    showMainResults(jsonObj);


    youtubeURLs.push({[youtubeURL]: jsonObj});

    chrome.storage.local.set({youtubeURLs: youtubeURLs}, function () {

        chrome.storage.local.get('youtubeURLs', function (result) {
            console.log(result.youtubeURLs)
        });
    });


})
.catch(function(error) {

  console.log('error from getModelResults'+error);
});


    }
})
            }
            else {
               alert("Currently this extension works only on valid YouTube URL");
               window.close();

            }
        }

});







